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

def retrieve_itemdata_for_tradingpost(server_name):
    if server_name:
        items = ItemData.query.all()
        
        item_dict = {}
        for item in items:
            if item.TradingCategory is not None:
                if item.TradingCategory not in ["Weapons", "Tools", "Apparel"]:
                    item_id = item.ItemID.lower()
                    item_dict[item_id] = {
                        'Name': item.Name,
                        'Category': item.TradingCategory,
                        'Family': item.TradingFamily,
                        'Group': item.TradingGroup,
                        'Price': 0,
                        'Avail': 0
                    }
        
        server = Market.query.filter_by(name=server_name).first()
        if server:
            added_items = 0
            for item in server.items:
                if item.item_id in item_dict:
                    item_dict[item.item_id]['Price'] = round(item.price, 2)
                    item_dict[item.item_id]['Avail'] = item.availability
                else:
                    try:
                        item_name = item.name.replace("_"," ").title()
                        filters = add_custom_category_family_group(item.item_id, item_name)
                        item_dict[item.item_id] = {
                            'Name': item_name,
                            'Category': filters['Category'],
                            'Family': filters['Family'],
                            'Group': filters['Group'],
                            'Price': round(item.price, 2),
                            'Avail': item.availability
                        }
                        added_items += 1
                    except Exception as e:
                        print(e)
            if added_items > 0:
                print(f'Added {added_items} items')
                db.session.commit()
                    

            for key in list(item_dict.keys()):
                if item_dict[key]['Price'] == 0:
                    item_dict.pop(key)
            
            item_list_dicts = []
            for value in item_dict.values():
                item_list_dicts.append(value)
                
        else:
            print('Server not Found')
        return item_list_dicts
    return None


def add_custom_category_family_group(itemID, itemName):
    filters = {
        'Category': "",
        'Family': "",
        'Group': ""
    }
    
    ## Furnishings
    if "house" in itemID:
        filters['Category'] = "Furnishings"
        #Miscellaneous
        if "plant" in itemID or "vegetation" in itemID or "flowerpot" in itemID or "floral" in itemID:
            filters['Family'] = "houseMisc"
            filters['Group'] = "decorVegetation"
        elif "storage" in itemID:
            filters['Family'] = "houseMisc"
            filters['Group'] = "decorStorage"
        elif "chimes" in itemID or "cask" in itemID or "cairn" in itemID or "weaponrack" in itemID or "wheelbarrow" in itemID or "pirate_decor_water" in itemID:
            filters['Family'] = "houseMisc"
            filters['Group'] = "decorMisc"
        
        #Decorations
        elif "decor" in itemID:
            filters['Family'] = "houseDecorations"
            if "painting" in itemID:
                filters['Group'] = "decorPaintings"
                
        elif "lighting" in itemID:
            filters['Family'] = "houseDecorations"
            filters['Group'] = "decorLighting"
        elif "urtain" in itemID or "urtain" in itemName:
            filters['Family'] = "houseDecorations"
            filters['Group'] = "decorCurtains"
        elif "rug" in itemID:
            filters['Family'] = "houseDecorations"
            filters['Group'] = "decorRugs"
        elif "dish" in itemID or "demijohn" in itemID or "cookware" in itemID or "potsandpans" in itemID or "vase_" in itemID or "placesetting" in itemID or "Amphora" in itemName or "Pot" in itemName or "jar" in itemID or "tea" in itemID or "drinkset" in itemID or "drinkcrate" in itemID or "jug" in itemID or "Rum Crate" in itemName or "Tea Set" in itemName:
            filters['Family'] = "houseDecorations"
            filters['Group'] = "decorDishes"
        elif "paper" in itemID or "writing" in itemID or "Writing" in itemName or "oldbook" in itemID or "Map" in itemName or "Fireplace Books" in itemName or "scroll0" in itemID:
            filters['Family'] = "houseDecorations"
            filters['Group'] = "decorBooksPapers"
        elif "Wreath" in itemName:
            filters['Family'] = "houseDecorations"
            filters['Group'] = "decorOther"
            
        #Trophies
        elif "Trophy" in itemName:
            filters['Family'] = "houseTrophy"
            if "Combat" in itemName:
                filters['Group'] = "combatBuffs"
            elif "Crafting" in itemName:
                filters['Group'] = "craftingBuffs"
            elif "Gathering" in itemName:
                filters['Group'] = "gatheringBuffs"
            else: 
                filters['Group'] = "otherBuffs"
        
        #Furniture
        elif "chair" in itemID or "stool" in itemID:
            filters['Family'] = "houseFurniture"
            filters['Group'] = "decorChairs"
        elif "table_" in itemID or "wallwaves" in itemID:
            filters['Family'] = "houseFurniture"
            filters['Group'] = "decorTables"
        elif "shelf0" in itemID or "bookcase" in itemID:
            filters['Family'] = "houseFurniture"
            filters['Group'] = "decorShelves"
        elif "Stove" in itemName:
            filters['Family'] = "houseFurniture"
            filters['Group'] = "decorStoves"
        elif "bed_" in itemID:
            filters['Family'] = "houseFurniture"
            filters['Group'] = "decorBeds"
        elif "cabinet" in itemID or "Cabinet" in itemName or "armoire" in itemID or "Armoire" in itemName or "dresser" in itemID:
            filters['Family'] = "houseFurniture"
            filters['Group'] = "decorCabinets"
        
        # Final pass
        elif "dynasty_decor" in itemID or "settler_decor" in itemID or "pirate_decor" in itemID:
            filters['Family'] = "houseDecorations"
            filters['Group'] = "decorOther"
        elif "legion_decor" in itemID:
            filters['Family'] = "houseFurniture"
            filters['Group'] = "decorTables"
        elif "pirate" in itemID:
            filters['Family'] = "houseMisc"
            filters['Group'] = "decorMisc"
        else:
            filters['Family'] = "houseDecorations"
            filters['Group'] = "decorOther"

    ## Utilities  
    elif "Sheet Music" in itemName:
        filters['Category'] = "Utilities"
        filters['Family'] = "musicSheets"
        if "azothflute" in itemID:
            filters['Group'] = "sheetsFlute"
        elif "guitar" in itemID:
            filters['Group'] = "sheetsGuitar"
        elif "mandolin" in itemID:
            filters['Group'] = "sheetsMandolin"
        elif "urbass" in itemID:
            filters['Group'] = "sheetsUrbass"
        elif "drums" in itemID:
            filters['Group'] = "sheetsDrums"
    elif "repairkit" in itemID:
        filters['Category'] = "Utilities"
        filters['Family'] = "repairKits"
        filters['Group'] = "repairKits"
    elif "summermedley_" in itemID or "wcconsumable_" in itemID:
        filters['Category'] = "Utilities"
        filters['Family'] = "EventConsumables"
        filters['Group'] = "FoodAttribute"
    elif "rabbitseasontotem" in itemID:
        filters['Category'] = "Utilities"
        filters['Family'] = "EventConsumables"
        filters['Group'] = "FoodLuck"
        
    ## Resources 
    elif "Pattern:" in itemName:
        filters['Category'] = "Resources"
        filters['Family'] = "raw"
        filters['Group'] = "CraftingPatterns"
    elif "seal_" in itemID:
        filters['Category'] = "Resources"
        filters['Family'] = "raw"
        filters['Group'] = "CraftingComponents"
    elif "perfectsalvage" in itemID:
        filters['Category'] = "Resources"
        filters['Family'] = "raw"
        filters['Group'] = "perfectSalvage"
    
    if filters["Category"] != "":
        new_item = ItemData(
            ItemType = filters["Category"], 
            ItemClass = filters["Family"], 
            Tier = "", 
            ItemID = itemID, 
            Name = itemName, 
            ItemTypeDisplayName = "", 
            Description = "", 
            TradingCategory = filters["Category"], 
            TradingFamily = filters["Family"], 
            TradingGroup = filters["Group"], 
            BindOnPickup = 0, 
            BindOnEquip = 0, 
            GearScoreOverride = "", 
            MinGearScore = "", 
            MaxGearScore = "", 
            ItemStatsRef = "", 
            CanHavePerks = -1, 
            CanReplaceGem = -1, 
            Perk1 = "", 
            Perk2 = "", 
            Perk3 = "", 
            Perk4 = "", 
            Perk5 = "", 
            ForceRarity = 0, 
            RequiredLevel = 0, 
            UseTypeAffix = 0, 
            UseMaterialAffix = 0, 
            UseMagicAffix = 0, 
            IconCaptureGroup = 0, 
            UiItemClass = "", 
            ArmorAppearanceM = "", 
            ArmorAppearanceF = "", 
            WeaponAppearanceOverride = "", 
            IconPath = "", 
            CraftingRecipe = "", 
            IngredientCategories = "", 
            Durability = -1, 
            Weight = -1, 
            AttributionId = "", 
            CraftedAt = ""
        )
        db.session.add(new_item)
            
    return filters


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