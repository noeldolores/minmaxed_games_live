from datetime import datetime
import pytz
from ... import db
from ...models import Market, Item



def datetime_to_str(date_time):
    _local = pytz.utc.localize(date_time, is_dst=None).astimezone()
    _date = datetime.strftime(_local, '%m/%d %I:%M %p')
    return _date



def load_market_server(server_id):
    server = None
    market_dict = {}
    tries = 0
    try:
        while server is None:
            if tries > 5:
                break
            server = Market.query.filter_by(server_id=server_id).first()
            tries += 1
        
        item_dict = {}
        if server: 
            for item in server.items:
                item_name = item.name
                item_dict[item_name] = float(item.price)

            market_dict['name'] = server.name
            market_dict['last_update'] = datetime_to_str(server.last_update)
            market_dict['items'] = item_dict

    except Exception as e:
        print(e)

    finally:
        db.session.remove()
        return market_dict