from datetime import datetime
import pytz
from ... import db
from ...models import Market, Item
from . import player_data


def datetime_to_str(date_time):
    _local = pytz.utc.localize(date_time, is_dst=None).astimezone()
    _date = datetime.strftime(_local, '%m/%d %I:%M %p')
    return _date



def load_market_server(server_id):
    server = None
    market_dict = None
    tries = 0
    
    material_source = player_data.trade_post_order()
    trophy_source = player_data.trade_post_trophy_order()
    full_item_check_list = []
    for material_list in material_source:
        full_item_check_list.extend(material_list[1:])
    for trophy_list in trophy_source:
        category = trophy_list[0]
        if category != "components":
            for item in trophy_list[1:]:
                if item in ['minor', 'basic', 'major']:
                    full_item_check_list.append(f'{item}_{category}_trophy')
                else:
                    full_item_check_list.append(item)
        else:
            full_item_check_list.extend(trophy_list[1:])
    print(full_item_check_list)
    try:
        while server is None:
            if tries > 20:
                break
            server = Market.query.filter_by(server_id=server_id).first()
            tries += 1
        
        item_dict = {}
        if server: 
            market_dict = {}
            for item in server.items:
                item_name = item.name.lower()
                if item_name in full_item_check_list:
                    #item_name = item.name
                    item_dict[item_name] = float(item.price)

            market_dict['name'] = server.name
            market_dict['last_update'] = datetime_to_str(server.last_update)
            market_dict['items'] = item_dict

    except Exception as e:
        print(e)
        db.session.remove()
    finally:
        print(market_dict)
        return market_dict