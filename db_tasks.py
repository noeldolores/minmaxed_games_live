import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timezone
import pytz
from website import app, db, models
import time
from website.scripts.newworld import player_data, db_scripts
from dateutil.parser import parse


def print_stderr(output=str):
  try:
    print(output, flush=True)
    return True
  except Exception as e:
    print(f"print_stderr: {e}", flush=True)
    return False


def timer(time_history=None, to_print=None):
    if not time_history:
        base = time.time()
        time_history = [('Beginning task...', base, 0)]
        print_stderr(time_history[0])
        return time_history

    stamp = time.time()
    lap_num = len(time_history) - 1
    total_time = round(stamp - time_history[0][1], 4)
    lap_time = round(total_time - time_history[lap_num][2], 4)
    lap_data = (str(to_print), lap_time, total_time)
    time_history.append(lap_data)
    if to_print:
        print_stderr(f'{lap_data} : {round(total_time/60,2)} min')
    return time_history


def str_to_datetime(date_string):
    try:
        if '.' in date_string:
            _date = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%f')
        else:
            _date = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S')
        return _date.astimezone(pytz.utc)
    except Exception as e:
        print_stderr(f'{e} str_to_datetime: {date_string}')
        return None


def datetime_to_str(date_time):
    _date = datetime.strftime(date_time, '%m/%d %I:%M %p')
    return _date


def fetch_servers_status():
    server_status = db_scripts.update_server_status()
    if server_status:
        return server_status
    return None


def request_server_data(stopwatch, server_name_num, update_results):
    # Retrieve server name/id dictionary
    server_dict = {}
    server_name, api_id = server_name_num.lower().split(",")
    server_dict[server_name] = {
        'api_id' : api_id,
        'items' : {}
        }
    
    server_status = fetch_servers_status()
    age_minimum = 60 * 10 # 10 minutes
    server_update = {}
    for server_name, server_data in server_dict.items():
        try:
            status_server = models.ServerStatus.query.filter_by(name=server_name).first()
            
            age = (server_status[server_name]['nwmarketprices_update'] - server_status[server_name]['db_update']).total_seconds()
            server_update[server_name] = {
                'update': age > age_minimum,
                'age': age
            }
            
            if server_update[server_name]['update'] == True:
                status_server.update_status = "Pending Scan"
            else:
                status_server.update_status = "Up-to-Date"
        except Exception as e:
            print(server_name, e)
            server_update[server_name] = {
                'update': True,
                'age': 0
            }
    db.session.commit()
    
    for server_name, server_data in server_dict.items():
        if server_update[server_name]['update'] == True:
            api_id = server_data['api_id']
            url = f"https://nwmarketprices.com/api/latest-prices/{api_id}/"
            try:
                status_server = models.ServerStatus.query.filter_by(name=server_name).first()
                status_server.update_status = "Scanning"
                db.session.commit()
                
                my_timeout = 300
                response = requests.request(method='GET', url=url, timeout=my_timeout)
            except Exception as e:
                print(e)
            
            if response:
                if response.status_code == 200:
                    stopwatch = timer(stopwatch, None)
                    
                    soup = BeautifulSoup(response.content, "html.parser")
                    item_list = json.loads(str(soup))
                    
                    total_item_count = max(len(item_list),1)
                    
                    dates_list=[]
                    for item in item_list:
                        name = item['ItemName'].replace("'","").replace(" ","_").lower()
                        _date = str_to_datetime(item['LastUpdated'])
                        dates_list.append(_date)
                        server_dict[server_name]['items'][name] = {
                            'Name': name,
                            'ID': item['ItemId'],
                            'Price' : item['Price'],
                            'Availability' : item['Availability'],
                            'LastUpdated' : _date,
                        }

                    if len(dates_list) > 0:
                        latest_date = max(dates_list)
                        server_dict[server_name]['latest_date'] = latest_date
                    else:
                        server_dict[server_name]['latest_date'] = None
                    
                    status_server = models.ServerStatus.query.filter_by(name=server_name).first()
                    status_server.update_status = "Pending Update"
                    db.session.commit()
                else:
                    stopwatch = timer(stopwatch, None)
                    continue
            else:
                stopwatch = timer(stopwatch, None)
                continue
        else:
            update_results['update_not_required'] += 1
            
            status_server = models.ServerStatus.query.filter_by(name=server_name).first()
            status_server.update_status = "Up-to-Date"
            db.session.commit()
        
    # Push data to db
    for server_name, server_data in server_dict.items():
        if server_update[server_name]['update'] == True:
            status_server = models.ServerStatus.query.filter_by(name=server_name).first()
            status_server.update_status = "Updating"
            db.session.commit()
            
            server = models.Market.query.filter_by(name=server_name).first()
            
            if server is None:
                server = models.Market(name=server_name, server_id=server_data['api_id'])
                db.session.add(server)
                db.session.commit()
                server = models.Market.query.filter_by(name=server_name).first()
            
            item_data = server_data['items']
            item_update_count = 0
            if len(item_data) > 0:
                for item, item_info in item_data.items():
                    item_check = models.Item.query.filter_by(market_id=server.id).filter_by(item_id=item_info['ID']).first()
                    if item_check:
                        if float(item_info['Price']) > 0:
                            item_check.price = item_info['Price']
                            item_check.availability = item_info['Availability']
                            item_check.last_update = item_info['LastUpdated']
                            item_update_count += 1 
                    else:
                        new_item = models.Item(last_update=item_info['LastUpdated'], item_id=item_info['ID'], name=item_info['Name'], price=item_info['Price'], availability=item_info['Availability'], market_id=server.id)
                        db.session.add(new_item)
                        item_update_count += 1 
                
                latest_date = server_status[server_name]['nwmarketprices_update']
                if latest_date:
                    server.last_update = latest_date
                    update_percentage = round((item_update_count / total_item_count)*100,1)
                    stopwatch = timer(stopwatch, f'{server_name} : {update_percentage}% ({item_update_count}) to {datetime_to_str(latest_date)}')
                
                update_results['servers_updated'] += 1
                status_server = models.ServerStatus.query.filter_by(name=server_name).first()
                status_server.update_status = "Up-to-Date"
            else:
                stopwatch = timer(stopwatch, f'{server_name} : Unable to connect.')
                update_results['server_update_errors'] += 1
                status_server = models.ServerStatus.query.filter_by(name=server_name).first()
                status_server.update_status = "Error"
                
            db.session.commit()

    return update_results


def main():
    with app.app_context():
        stopwatch = timer()
        update_results = {
            'update_not_required': 0,
            'servers_updated': 0,
            'server_update_errors': 0
        }
        
        try:
            server_list_file = '/home/noeldolores/minmaxed_games/website/static/newworld/txt/api_server_list.txt'
            with open(server_list_file) as file:
                lines = file.readlines()
                for line in lines:
                    server_name_num = line.rstrip().lower()
                    update_results = request_server_data(stopwatch, server_name_num, update_results)
            full_pull = True
        except Exception as e:
            full_pull = False
            db.session.rollback()
            print_stderr(e)
            
        stopwatch = timer(stopwatch, f'Task completed...{full_pull}')
        print_stderr(update_results)
    time.sleep(60 * 10) # 10 minute rest
    
if __name__ == "__main__":
    main()