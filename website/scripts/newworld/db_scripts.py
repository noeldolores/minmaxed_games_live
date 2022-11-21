from datetime import datetime
import pytz
from ... import db
from ...models import Market, Item, ItemData
import json
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
                    item_dict[item_name] = float(item.price)

            market_dict['name'] = server.name
            market_dict['last_update'] = datetime_to_str(server.last_update)
            market_dict['items'] = item_dict

    except Exception as e:
        print(e)
        db.session.remove()
    finally:
        return market_dict
    
# Run each time new items are loaded
def import_itemdata_to_table():
    try:
        path = '/home/noeldolores/minmaxed_games/website/static/newworld/json/item_data_master.json'
        with open(path) as f:
            master_dict = json.load(f)
        
        count = 0
        for item_id, item_data in master_dict.items():
            item_check = ItemData.query.filter_by(ItemID=item_id).first()
            if not item_check:
                new_item = ItemData(
                    ItemType = item_data['ItemType'], 
                    ItemClass = item_data['ItemClass'], 
                    Tier = item_data['Tier'], 
                    ItemID = item_data['ItemID'], 
                    Name = item_data['Name'], 
                    ItemTypeDisplayName = item_data['ItemTypeDisplayName'], 
                    Description = item_data['Description'], 
                    TradingCategory = item_data['TradingCategory'], 
                    TradingFamily = item_data['TradingFamily'], 
                    TradingGroup = item_data['TradingGroup'], 
                    BindOnPickup = item_data['BindOnPickup'], 
                    BindOnEquip = item_data['BindOnEquip'], 
                    GearScoreOverride = item_data['GearScoreOverride'], 
                    MinGearScore = item_data['MinGearScore'], 
                    MaxGearScore = item_data['MaxGearScore'], 
                    ItemStatsRef = item_data['ItemStatsRef'], 
                    CanHavePerks = item_data['CanHavePerks'], 
                    CanReplaceGem = item_data['CanReplaceGem'], 
                    Perk1 = item_data['Perk1'], 
                    Perk2 = item_data['Perk2'], 
                    Perk3 = item_data['Perk3'], 
                    Perk4 = item_data['Perk4'], 
                    Perk5 = item_data['Perk5'], 
                    ForceRarity = item_data['ForceRarity'], 
                    RequiredLevel = item_data['RequiredLevel'], 
                    UseTypeAffix = item_data['UseTypeAffix'], 
                    UseMaterialAffix = item_data['UseMaterialAffix'], 
                    UseMagicAffix = item_data['UseMagicAffix'], 
                    IconCaptureGroup = item_data['IconCaptureGroup'], 
                    UiItemClass = item_data['UiItemClass'], 
                    ArmorAppearanceM = item_data['ArmorAppearanceM'], 
                    ArmorAppearanceF = item_data['ArmorAppearanceF'], 
                    WeaponAppearanceOverride = item_data['WeaponAppearanceOverride'], 
                    IconPath = item_data['IconPath'], 
                    CraftingRecipe = item_data['CraftingRecipe'], 
                    IngredientCategories = item_data['IngredientCategories'], 
                    Durability = item_data['Durability'], 
                    Weight = item_data['Weight'], 
                    AttributionId = item_data['AttributionId'], 
                    CraftedAt = item_data['CraftedAt']
                )
                db.session.add(new_item)
                count += 1
        db.session.commit()
        print(f'Added {count} items.')
        return True
    
    except Exception as e:
        print(e)
        return False
    
    
def rename_default_groups():
    try:
        items = ItemData.query.all()
        for item in items:
            if item.TradingCategory == "Resources":
                if item.TradingFamily == "RawResources":
                    if item.TradingGroup == "Ore":
                        item.TradingGroup = "rawOre"
                    elif item.TradingGroup == "Wood":
                        item.TradingGroup = "rawWood"
                    elif item.TradingGroup == "Fiber":
                        item.TradingGroup = "rawFiber"
                    elif item.TradingGroup == "Cloth":
                        item.TradingGroup = "rawCloth"
                    elif item.TradingGroup == "Stone":
                        item.TradingGroup = "rawStone"
                    elif item.TradingGroup == "Flint":
                        item.TradingGroup = "rawFlint"
                    elif item.TradingGroup == "Ore":
                        item.TradingGroup = "rawOre"
                    elif item.TradingGroup == "Oil":
                        item.TradingGroup = "rawOil"
                        
                elif item.TradingFamily == "CookingIngredients":
                    if item.TradingGroup == "Meat":
                        item.TradingGroup = "cookingMeat"
                    elif item.TradingGroup == "Vegetable":
                        item.TradingGroup = "cookingVegetable"
                    elif item.TradingGroup == "Fruit":
                        item.TradingGroup = "cookingFruit"
                    elif item.TradingGroup == "Berry":
                        item.TradingGroup = "cookingBerry"
                    elif item.TradingGroup == "Grain":
                        item.TradingGroup = "cookingGrain"
                    elif item.TradingGroup == "Nut":
                        item.TradingGroup = "cookingNut"
                    elif item.TradingGroup == "Honey":
                        item.TradingGroup = "cookingHoney"
                    elif item.TradingGroup == "Water":
                        item.TradingGroup = "cookingWater"
                        
                elif item.TradingFamily == "RefinedResources":
                    if item.TradingGroup == "Cloth":
                        item.TradingGroup = "refinedCloth"
                    if item.TradingGroup == "Leather":
                        item.TradingGroup = "refinedLeather"
                               
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False