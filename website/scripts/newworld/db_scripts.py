from datetime import datetime
import pytz
from ... import db
from ...models import Market, Item



def datetime_to_str(date_time):
    _local = pytz.utc.localize(date_time, is_dst=None).astimezone()
    _date = datetime.strftime(_local, '%m/%d %I:%M %p')
    return _date



def load_market_server(server_id):
    try:
        server = Market.query.filter_by(server_id=server_id).first()
    except Exception as e:
        server = None
        print(e)
        db.session.rollback()
        db.session.remove()
        
    market_dict = {}
    item_dict = {}
    if server: 
        for item in server.items:
            if server.name == 'delos':
                print(item.name)
            item_name = item.name
            item_dict[item_name] = float(item.price)

        market_dict['name'] = server.name
        market_dict['last_update'] = datetime_to_str(server.last_update)
        market_dict['items'] = item_dict

        return market_dict
    else:
        return None