import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timezone
import pytz
from website import app, db, models
import time
from website.scripts.newworld import player_data


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


def request_server_data(stopwatch, server_name_num):
    # Retrieve server name/id dictionary
    server_dict = {}
    server_name, api_id = server_name_num.lower().split(",")
    server_dict[server_name] = {
        'api_id' : api_id,
        'items' : {}
        }
    
    for server_name, server_data in server_dict.items():
        api_id = server_data['api_id']
        url = f"https://nwmarketprices.com/api/latest-prices/{api_id}/"
        try:
            my_timeout = 300
            response = requests.request(method='GET', url=url, timeout=my_timeout)
        except Exception as e:
            if response:
                print(response.status_code, e)
            else:
                print(e)
            continue
        
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
            else:
                stopwatch = timer(stopwatch, None)
                continue
        else:
            stopwatch = timer(stopwatch, None)
            continue
        
    # Push data to db
    for server_name, server_data in server_dict.items():
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
            
            latest_date = server_dict[server_name]['latest_date']
            if latest_date:
                server.last_update = latest_date
                update_percentage = round((item_update_count / total_item_count)*100,1)
                stopwatch = timer(stopwatch, f'{server_name} : {update_percentage}% ({item_update_count}) to {datetime_to_str(latest_date)}')
        else:
            stopwatch = timer(stopwatch, f'{server_name} : Unable to connect.')
            
        db.session.commit()
    return True


def main():
    with app.app_context():
        stopwatch = timer()
        try:
            server_name_num = 'Castle of Steel,11'
            full_pull = request_server_data(stopwatch, server_name_num)
        except Exception as e:
            full_pull = False
            db.session.rollback()
            print(full_pull, e)
        stopwatch = timer(stopwatch, f'Task completed...{full_pull}')
    
if __name__ == "__main__":
    main()