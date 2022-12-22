import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import pytz
from website import app, db, models
from dateutil.parser import parse
import time


def print_stderr(output=str):
  try:
    print(output, flush=True)
    return True
  except Exception as e:
    print(f"print_stderr: {e}", flush=True)
    return False


def str_to_datetime(date_string):
    try:
        if '.' in date_string:
            _date = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S.%f')
        else:
            _date = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
        return _date.astimezone(pytz.utc)
    except Exception as e:
        print(f'{e} str_to_datetime: {date_string}')
        return None


def datetime_to_str(date_time):
    _date = datetime.strftime(date_time, '%m/%d %I:%M %p')
    return _date


def fetch_nwmarketprices_updates():
    server_updates = {}
    url = f"https://nwmarketprices.com/api/servers_updated/"
    try:
        my_timeout = 300
        response = requests.request(method='GET', url=url, timeout=my_timeout)
    except Exception as e:
        response = None
        print(e)
    
    if response:
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            server_data = json.loads(str(soup))
            
            if 'server_last_updated' in server_data:
                for server in server_data['server_last_updated']:
                    name = server[1].lower()
                    updated = server[2]
                    server_updates[name] = {
                        'updated': updated
                    }
        return server_updates
    return None


def fetch_database_updates(server_dict):
    for server in server_dict.keys():
        market = models.Market.query.filter_by(name=server).first()
        if market:
            updated = datetime_to_str(market.last_update)
            server_dict[server]['updated'] = updated
    return server_dict


def update_server_status():
    server_dict = {}
    server_list_file = '/home/noeldolores/minmaxed_games/website/static/newworld/txt/api_server_list.txt'
    with open(server_list_file) as file:
        lines = file.readlines()
        for line in lines:
            server_name, api_id = line.rstrip().lower().split(",")
            server_dict[server_name] = {
                'api_id': api_id
            }
            
    nwmarketprices = fetch_nwmarketprices_updates()
    database = fetch_database_updates(server_dict)
    
    server_count = max(len(list(server_dict.keys())), 1)
    server_success = 0
    error_count = 0
    for server_name, server_data in server_dict.items():
        update_required = False
        
        server = models.ServerStatus.query.filter_by(name=server_name).first()
        
        db_datetime = parse(database[server_name]['updated']).replace(tzinfo=pytz.utc)
        nwmarketprices_datetime = parse(nwmarketprices[server_name]['updated']).replace(tzinfo=pytz.utc)
        
        db_age = (nwmarketprices_datetime- db_datetime).seconds
        db_freshness = 0
        if db_age > 60 * 60 * 24: # 24 hours
            db_freshness = 5
        elif db_age > 60 * 60 * 12: # 12 hours
            db_freshness = 4
        elif db_age > 60 * 60 * 6: # 6 hours
            db_freshness = 3
        elif db_age > 60 * 60 * 3: # 3 hours
            db_freshness = 2
        elif db_age > 60 * 60 * 1: # 1 hour
            db_freshness = 1
        
        
        nwmarketprices_age = (datetime.now(pytz.utc) - nwmarketprices_datetime).seconds
        nwmarketprices_freshness = 0
        if nwmarketprices_age > 60 * 60 * 24: # 24 hours
            nwmarketprices_freshness = 5
        elif nwmarketprices_age > 60 * 60 * 12: # 12 hours
            nwmarketprices_freshness = 4
        elif nwmarketprices_age > 60 * 60 * 6: # 6 hours
            nwmarketprices_freshness = 3
        elif nwmarketprices_age > 60 * 60 * 3: # 3 hours
            nwmarketprices_freshness = 2
        elif nwmarketprices_age > 60 * 60 * 1: # 1 hour
            nwmarketprices_freshness = 1
        
        if server_name == "abaton" or server_name == "apophis":
            print_stderr(server_name, db_datetime, db_age, db_freshness, nwmarketprices_datetime, nwmarketprices_age, nwmarketprices_freshness)
            
        if server is None:
            server = models.ServerStatus(  name=server_name, 
                                    server_id=server_data['api_id'],
                                    update_status=None,
                                    db_update=db_datetime,
                                    db_freshness=db_freshness,
                                    nwmarketprices_update=nwmarketprices_datetime,
                                    nwmarketprices_freshness=nwmarketprices_freshness   )
            update_required = True
            
        else:
            if server.db_update != db_datetime:
                server.db_update = db_datetime
                update_required = True
            if server.db_freshness != db_freshness:
                server.db_freshness = db_freshness
                update_required = True
            if server.nwmarketprices_update != nwmarketprices_datetime:
                server.nwmarketprices_update = nwmarketprices_datetime
                update_required = True
            if server.nwmarketprices_freshness != nwmarketprices_freshness:
                server.nwmarketprices_freshness = nwmarketprices_freshness
                update_required = True
                
        if update_required:
            try:
                db.session.add(server)
                db.session.commit()
                server_success += 1
            except Exception as e:
                error_count += 1
                print(server_name, e)
                continue
    
    result = (server_success, server_count, round(server_success/server_count * 100, 2), error_count)
    return result


def main():
    with app.app_context():
        try:
            result = update_server_status()
            print_stderr(f'{result[2]}% of servers updated [{result[0]}/{result[1]}]. {result[3]} errors occured')
            time.sleep(60 * 10)
        except Exception as e:
            db.session.rollback()
            print_stderr('update_server_status: ', e)

if __name__ == "__main__":
    main()