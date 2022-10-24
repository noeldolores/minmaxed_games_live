import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import pytz
from website import app, db, models
import sys
import time


def print_stderr(output=str):
  try:
    print(output)
    return True
  except Exception as e:
    print(f"print_stderr: {e}")
    return False


def timer(time_history=None, function=None):
  if not time_history:
    base = time.time()
    time_history = [('Beginning task...', base, 0)]
    print_stderr(time_history[0])
    return time_history

  if function:
    stamp = time.time()
    lap_num = len(time_history) - 1
    total_time = round(stamp - time_history[0][1], 4)
    lap_time = round(total_time - time_history[lap_num][2], 4)
    lap_data = ((str(function), lap_time, total_time))
    time_history.append(lap_data)
    print_stderr(lap_data)
    return time_history


def str_to_datetime(date_string):
    _date = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S.%f')
    return _date.astimezone(pytz.utc)


def datetime_to_str(date_time):
    _local = pytz.utc.localize(date_time, is_dst=None).astimezone()
    _date = datetime.strftime(_local, '%m/%d %I:%M %p')
    return _date


def request_nwmarketprices(stopwatch):
    # Retrieve server name/id dictionary
    server_dict = {}

    server_list_file = '/home/noeldolores/minmaxed_games/website/static/newworld/txt/api_server_list.txt'
    with open(server_list_file) as file:
        lines = file.readlines()
        for line in lines:
            name, num = line.rstrip().lower().split(",")
            server_dict[name] = num

    stopwatch = timer(stopwatch, f'Prepared {len(server_dict)} servers from API Server List.')
    # Iterate through each server and retrieve data
    for key, value in server_dict.items():
        stopwatch = timer(stopwatch, f'Init: {key}')
        
        server = models.Market.query.filter_by(name=key).first()

        if not server:
            stopwatch = timer(stopwatch, f'Creating new table: {key}')
            # Create new market table
            server = models.Market(name=key, server_id=value)
            db.session.add(server)
            db.session.commit()
        else:
            stopwatch = timer(stopwatch, f'Found existing table: {key}')
            
        # Retrieve Data
        stopwatch = timer(stopwatch, f'Starting API request: {key}')
        url = f"https://nwmarketprices.com/api/latest-prices/{value}/"
        try:
            response = requests.request(method='GET', url=url)
        except Exception as e:
            print(response.status_code, e)
            continue
        if response.status_code == 200:
            stopwatch = timer(stopwatch, f'Response Success {response.status_code}: {key}')
            
            soup = BeautifulSoup(response.content, "html.parser")
            item_list = json.loads(str(soup))
            dates_list=[]
            
            for item in item_list:
                item_check = models.Item.query.filter_by(market_id=server.server_id).filter_by(item_id=item['ItemId']).first()
                if item_check:
                    item_check.price = item['Price']
                    item_check.availability = item['Availability']
                    item_check.last_update = str_to_datetime(item['LastUpdated'])
                else:
                    new_item = models.Item(last_update=str_to_datetime(item['LastUpdated']), item_id=item['ItemId'], name=item['ItemName'], price=item['Price'], availability=item['Availability'], market_id=server.id)
                    db.session.add(new_item)
                    
                dates_list.append(str_to_datetime(item['LastUpdated']))

            if len(dates_list) > 0:
                latest_date = max(dates_list)
                server.last_update = latest_date
                stopwatch = timer(stopwatch, f'Updated {key} with {len(dates_list)} items to {latest_date}')
            else:
                stopwatch = timer(stopwatch, f'Updated 0 items: {key}')
                  
            db.session.commit()
        else:
            stopwatch = timer(stopwatch, f'Unable to connect to {key}. Response from server: {response.status_code}')
            continue
    return True


def main():
    with app.app_context():
        stopwatch = timer()
        try:
            full_pull = request_nwmarketprices(stopwatch)
        except Exception as e:
            full_pull = False
            db.session.rollback()
            print(e)
        stopwatch = timer(stopwatch, f'Task completed...{full_pull}')
        
if __name__ == "__main__":
  main()