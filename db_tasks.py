import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
import pytz
from website import app, db, models


def str_to_datetime(date_string):
    _date = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S.%f')
    return _date.astimezone(pytz.utc)


def datetime_to_str(date_time):
    _local = pytz.utc.localize(date_time, is_dst=None).astimezone()
    _date = datetime.strftime(_local, '%m/%d %I:%M %p')
    return _date


def request_nwmarketprices():

    # Retrieve server name/id dictionary
    server_dict = {}
    basedir = os.path.abspath(os.path.dirname(__file__))
    print(basedir)
    server_list_file = os.path.join(basedir, '../../static/newworld/txt/api_server_list.txt')
    with open(server_list_file) as file:
        lines = file.readlines()
        for line in lines:
            name, num = line.rstrip().lower().split(",")
            server_dict[name] = num
    
    # Iterate through each server and retrieve data
    for key, value in server_dict.items():
        server = models.Market.query.filter_by(name=key).first()
        
        if not server:
            # Create new market table
            server = models.Market(name=key, server_id=value)
            models.Market.session.add(server)
            models.Market.session.commit()
        
        # Retrieve Data
        url = f"https://nwmarketprices.com/api/latest-prices/{value}/"
        response = requests.request(method='GET', url=url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            item_list = json.loads(str(soup))
            
            for item in item_list:
                item_check = models.Item.query.filter_by(item_id=item['ItemId']).first()
                if item_check:
                    item_check.price = item['Price']
                    item_check.availability = item['Availability']
                    item_check.last_update = str_to_datetime(item['LastUpdated'])
                else:
                    new_item = models.Item(last_update=str_to_datetime(item['LastUpdated']), item_id=item['ItemId'], name=item['ItemName'], price=item['Price'], availability=item['Availability'], market_id=server.id)
                    db.session.add(new_item)
            db.session.commit()
        else:
            return False
    return True


def main():
    with app.app_context():
        try:
            full_pull = request_nwmarketprices()
        except Exception as e:
            full_pull = False
            print(f"create_id_query_list: {e}", flush=True)
        print(full_pull)    
    
if __name__ == "__main__":
  main()