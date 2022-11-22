from flask import Blueprint, request, flash, render_template, redirect, url_for, escape, session
import random
from ..scripts.newworld import player_data, calculations as calcs, db_scripts
import os
import copy


newworld = Blueprint('newworld', __name__)


def init_session():
    if 'first_visit' not in session:
        session.permanent = True
        session['first_visit'] = True
        session['skill_levels'] = player_data.init_skill_levels()
        session['gear_sets'] = player_data.init_gear_sets()
        session['price_list'] = player_data.init_price_list()
        session['taxes_fees'] = player_data.init_taxes_and_fees()
        
        session['server_api'] = {
            'server_name': None,
            'server_id': None,
            'last_update': None,
            'force_load': False
        }
        session.pop('_flashes', None)
        flash("We use only the necessary cookies to store the data you provide so it is available for your next visit. No data is shared with any third party. By continuing, you agree to this use of cookies.", category='success')


def strip_leading_zeros(is_float, number):
    if number != "0":
        if is_float:
            return float(number.lstrip('0'))
        return int(number.lstrip('0'))
    return 0


def validate_search(search):
    basedir = os.path.abspath(os.path.dirname(__file__))
    primary_ingredients = os.path.join(basedir, '../static/newworld/txt/primary_ingredients.txt')
    secondary_ingredients = os.path.join(basedir, '../static/newworld/txt/secondary_ingredients.txt')
    components = os.path.join(basedir, '../static/newworld/txt/components.txt')
    arcana = os.path.join(basedir, '../static/newworld/txt/arcana.txt')
    trophies = os.path.join(basedir, '../static/newworld/txt/trophies.txt')
    primary_list = []
    secondary_list = []
    components_list = []
    arcana_list = []
    trophies_list = []
    
    search_list = []

    with open(primary_ingredients) as file:
        lines = file.readlines()
        search_list += [line.rstrip().lower() for line in lines]

    with open(secondary_ingredients) as file_2:
        lines = file_2.readlines()
        search_list += [line.rstrip().lower() for line in lines]

    with open(components) as file_3:
        lines = file_3.readlines()
        search_list += [line.rstrip().lower() for line in lines]
        
    with open(arcana) as file_4:
        lines = file_4.readlines()
        search_list += [line.rstrip().lower() for line in lines]
    
    with open(trophies) as file_5:
        lines = file_5.readlines()
        search_list += [line.rstrip().lower() for line in lines]
        
    if search in search_list:
        return search
    return None


def search_function():
    search = None
    if request.method == "GET":
        if 'search' in request.args:
            search = str(escape(request.args['search'])).strip().lower()
            search_result = validate_search(search)
            if search_result is not None:
                return search_result.replace(" ","_")
    return None


def determine_material_category(material):
    basedir = os.path.abspath(os.path.dirname(__file__))
    primary_ingredients = os.path.join(basedir, '../static/newworld/txt/primary_ingredients.txt')
    secondary_ingredients = os.path.join(basedir, '../static/newworld/txt/secondary_ingredients.txt')
    components = os.path.join(basedir, '../static/newworld/txt/components.txt')
    arcana = os.path.join(basedir, '../static/newworld/txt/arcana.txt')
    trophies = os.path.join(basedir, '../static/newworld/txt/trophies.txt')
    
    primary_list = []
    with open(primary_ingredients) as file:
        lines = file.readlines()
        primary_list = [line.rstrip().lower() for line in lines]

    secondary_list = []
    with open(secondary_ingredients) as file_2:
        lines = file_2.readlines()
        secondary_list = [line.rstrip().lower() for line in lines]

    components_list = []
    with open(components) as file_3:
        lines = file_3.readlines()
        components_list = [line.rstrip().lower() for line in lines]
        
    arcana_list = []
    with open(arcana) as file_4:
        lines = file_4.readlines()
        arcana_list = [line.rstrip().lower() for line in lines]
        
    trophies_list = []
    with open(trophies) as file_5:
        lines = file_5.readlines()
        trophies_list = [line.rstrip().lower() for line in lines]

    if material in primary_list:
        return "primary"
    elif material in secondary_list:
        return "secondary"
    elif material in components_list or material in arcana_list or material in trophies_list:
        return "component"
    return None


def random_material():
    datalist = []
    basedir = os.path.abspath(os.path.dirname(__file__))
    primary_file = os.path.join(basedir, '../static/newworld/txt/primary_ingredients.txt')
    with open(primary_file) as file:
        lines = file.readlines()
        datalist = [line.rstrip().lower().replace(" ","_") for line in lines]

    # secondary_file = os.path.join(basedir, '../static/newworld/txt/secondary_ingredients.txt')
    # with open(secondary_file) as file_2:
    #     lines = file_2.readlines()
    #     datalist.extend([line.rstrip().lower() for line in lines])

    # components_file = os.path.join(basedir, '../static/newworld/txt/components.txt')
    # with open(components_file) as file_3:
    #     lines = file_3.readlines()
    #     datalist.extend([line.rstrip().lower() for line in lines])

    random_number = random.randint(0, len(datalist)-1)
    random_material = datalist[random_number]

    return random_material


def dictionary_key_replacements():
    if 'price_list' in session:
        if 'refining_components' in session['price_list']:
            session['price_list']['refining_component'] = session['price_list']['refining_components']
            print("Rename: " + str(session['price_list'].pop('refining_components', None)))
            
        if 'smelting_precious' not in session['price_list']:
            session['price_list']['smelting_precious'] = {
                "silver_ore" : 0,
                "silver_ingot" : 0,
                "gold_ore" : 0,
                "gold_ingot" : 0,
                "platinum_ore" : 0,
                "platinum_ingot" : 0,
                "charcoal" : 0,
                "orichalcum_ore" : 0,
                "orichalcum_ingot_platinum" : 0
            }
        
        if 'loot_luck' not in session['price_list']:
            trophy_order = player_data.trade_post_trophy_order()
            for items in trophy_order:
                category = items[0]
                category_list = items[1:]
                if category not in session['price_list']:
                    session['price_list'][category] = {}
                    for item in category_list:
                        if item in ['minor','basic','major']:
                            trophy = f'{item}_{category}_trophy'
                            session['price_list'][category][trophy] = 0
                        else:
                            session['price_list'][category][item] = 0
                
    if 'taxes_fees' not in session:
        session['taxes_fees'] = player_data.init_taxes_and_fees()
    elif 'weavers_fen' not in session['taxes_fees']['territory']:
            session['taxes_fees']['territory']['weavers_fen'] = False
    if 'crafting' not in session['taxes_fees']:
        session['taxes_fees']['crafting'] = {
            'station': 0
        }
    
    if 'server_api' not in session: 
        server_name = None    
        server_id = None    
        last_update = None
        force_load = False
        if 'server_data' in session:
            server_dict = {}
            basedir = os.path.abspath(os.path.dirname(__file__))
            server_list_file = os.path.join(basedir, '../static/newworld/txt/api_server_list.txt')
            with open(server_list_file) as file:
                lines = file.readlines()
                lines.sort()
                for line in lines:
                    name, num = line.rstrip().lower().split(",")
                    server_dict[name] = num
                    
            server_name = session['server_data']['name']
            last_update = session['server_data']['last_update']
            server_id = server_dict[server_name]
        
        if 'api_loaded' in session:
            if session['api_loaded']:
                force_load = True
            session.pop('api_loaded')
                
        session['server_api'] = {
            'server_name': server_name,
            'server_id': server_id,
            'last_update': last_update,
            'force_load': force_load
        }
    
    if 'server_data' in session:
        session.pop('server_data')


def load_api_server_data(server_name):
    server_dict = {}
    basedir = os.path.abspath(os.path.dirname(__file__))
    server_list_file = os.path.join(basedir, '../static/newworld/txt/api_server_list.txt')
    with open(server_list_file) as file:
        lines = file.readlines()
        lines.sort()
        for line in lines:
            name, num = line.rstrip().lower().split(",")
            server_dict[name] = num
            
    server_id = server_dict[server_name]
    try:
        market_dict = db_scripts.load_market_server(server_id)

        if market_dict:
            item_dict = market_dict['items']
    
            server_price_list = copy.deepcopy(session['price_list'])
            for key, value in server_price_list.items():
                for mat in value.keys():
                    if mat in item_dict:
                        server_price_list[key][mat] = item_dict[mat]
                     
            server_data = {
                'name' : market_dict['name'],
                'last_update': market_dict['last_update'],
                'items': server_price_list
            }
            
            session['server_api'] = {
                'server_name': market_dict['name'],
                'server_id': server_id,
                'last_update': market_dict['last_update'],
                'force_load': True
            }
            return server_data
    except Exception as e:
        print(e)
        session['server_api']['force_load'] = False
        return None


def force_load_server_api_check():
    if 'server_api' in session:
        if session['server_api']['force_load'] == True:
            server_name = session['server_api']['server_name']
            if server_name:
                server_data = load_api_server_data(server_name)
                if server_data:
                    if 'items' in server_data:
                        return server_data['items']
    return None


@newworld.route('/', methods=['GET', 'POST'])
def home():
    init_session()
    dictionary_key_replacements()
    
    search = search_function()
    
    if search:
        return redirect(url_for("newworld.material", material=search))

    return render_template('newworld/base.html')


@newworld.route('/trade_skills_refining', methods=['GET', 'POST'])
def trade_skills_refining():
    init_session()
    dictionary_key_replacements()
    
    search = search_function()
    if search:
        return redirect(url_for("newworld.material", material=search))

    return render_template('newworld/trade_skills_refining.html')


@newworld.route('/skills', methods=['GET', 'POST'])
def skills():
    init_session()
    dictionary_key_replacements()
    
    search = search_function()
    if search:
        return redirect(url_for('newworld.material', material=search))

    return render_template('newworld/skills.html', skill_levels=session['skill_levels'])


@newworld.route('/skills_hx', methods=['GET', 'POST'])
def skills_hx():
    
    if request.method == 'POST':
        if "save" in request.form:
            session['skill_levels'] = {
                "crafting" : {
                    "arcana": strip_leading_zeros(False, request.form['arcana_level']),
                    "armoring": strip_leading_zeros(False, request.form['armoring_level']),
                    "cooking": strip_leading_zeros(False, request.form['cooking_level']),
                    "engineering": strip_leading_zeros(False, request.form['engineering_level']),
                    "furnishing" : strip_leading_zeros(False, request.form['furnishing_level']),
                    "jewelcrafting": strip_leading_zeros(False, request.form['jewelcrafting_level']),
                    "weaponsmithing": strip_leading_zeros(False, request.form['weaponsmithing_level'])
                },
                "refining" : {
                    "leatherworking": strip_leading_zeros(False, request.form['leatherworking_level']),
                    "smelting": strip_leading_zeros(False, request.form['smelting_level']),
                    "stone_cutting": strip_leading_zeros(False, request.form['stone_cutting_level']),
                    "weaving": strip_leading_zeros(False, request.form['weaving_level']),
                    "woodworking": strip_leading_zeros(False, request.form['woodworking_level'])
                },
                "gathering" : {
                    "fishing" : strip_leading_zeros(False, request.form['fishing_level']),
                    "harvesting" : strip_leading_zeros(False, request.form['harvesting_level']),
                    "logging" : strip_leading_zeros(False, request.form['logging_level']),
                    "mining" : strip_leading_zeros(False, request.form['mining_level']),
                    "skinning" : strip_leading_zeros(False, request.form['skinning_level'])
                }
            }
            
    return render_template('newworld/skills_hx.html', skill_levels=session['skill_levels'])


@newworld.route('/gearsets', methods=['GET', 'POST'])
def gearsets():
    init_session()
    dictionary_key_replacements()
    
    search = search_function()
    if search:
        return redirect(url_for('newworld.material', material=search))

    return render_template('newworld/gearsets.html', gear_sets=session['gear_sets'])


@newworld.route('/gearsets_hx', methods=['GET', 'POST'])
def gearsets_hx():

    if request.method == 'POST':
        if "save" in request.form:
            for i in session['gear_sets'].keys():
                for j in session['gear_sets'][i].keys():
                    if j in request.form:
                        session['gear_sets'][i][j] = True
                    else:
                        session['gear_sets'][i][j] = False

    return render_template('newworld/gearsets_hx.html', gear_sets=session['gear_sets'])


@newworld.route('/user_prices', methods=['GET', 'POST'])
def user_prices():
    init_session()
    dictionary_key_replacements()
    
    search = search_function()
    if search:
        return redirect(url_for('newworld.material', material=search))

    template_order = player_data.trade_post_order()
    trophy_order = player_data.trade_post_trophy_order()
    
    return render_template('newworld/user_prices.html', price_list=session['price_list'], template_order=template_order, trophy_order=trophy_order)


@newworld.route('/user_prices_hx', methods=['GET', 'POST'])
def user_prices_hx():
    template_order = player_data.trade_post_order()
    trophy_order = player_data.trade_post_trophy_order()
                    
    if request.method == 'POST':
        if "save" in request.form:
            for category, items in session['price_list'].items():
                for item in items.keys():
                    if item in request.form:
                        session['price_list'][category][item] = strip_leading_zeros(True, request.form[item])
                    else:
                        if item == "orichalcum_ingot_platinum":
                            session['price_list'][category][item] = strip_leading_zeros(True, request.form["orichalcum_ingot"])     
            
    return render_template('newworld/user_prices_hx.html', price_list=session['price_list'], template_order=template_order, trophy_order=trophy_order)


@newworld.route('/refining', methods=['GET', 'POST'])
def refining():
    init_session()
    dictionary_key_replacements()
    
    search = search_function()
    if search:
        return redirect(url_for('newworld.material', material=search))

    return render_template('newworld/refining.html')


@newworld.route('/refining_hx', methods=['GET', 'POST'])
def refining_hx():
    init_session()
    
    template_order = player_data.refining_order()

    if 'price_list' in session:
        price_dict = session['price_list']
    force_load = force_load_server_api_check()
    if force_load is not None:
        price_dict = force_load

    taxes_fees = session['taxes_fees']
    
    all_tiers_all_routes, financial_data = calcs.tp_cost_to_refine_all_routes_all_tiers(price_dict, session['skill_levels']['refining'], session['gear_sets'], taxes_fees)
    cheapest_route = calcs.cheapest_tp_cost_route_to_refine_each_tier(price_dict, all_tiers_all_routes, taxes_fees, financial_data)
    
    return render_template('newworld/refining_hx.html', cheapest_route=cheapest_route, template_order=template_order)


@newworld.route('/material/<material>', methods=['GET', 'POST'])
def material(material):
    init_session()
    dictionary_key_replacements()

    search = search_function()
    if search:
        return redirect(url_for('newworld.material', material=search))

    category = determine_material_category(material.replace("_"," "))
    material_display = material.replace("_"," ").lower().title()

    discipline = calcs.determine_discipline(material)
    material_list = player_data.material_navbar()
    
    material_nav_items = []
    for item in material_list:
        if item[0] == discipline:
            material_nav_items = item[1:]
    
    if 'elemental_lodestone' in material_nav_items:
        material_nav_items.remove('elemental_lodestone')
    
    tier = calcs.determine_tier(material)

    if category == "primary":
        return render_template('newworld/material.html', material=material_display, material_nav_items=material_nav_items, tier=tier)
    
    if category == "component" or category == "secondary":
        return render_template('newworld/material_component.html', material=material_display)


@newworld.route('/material_primary/<material>', methods=['GET', 'POST'])
def material_primary(material):
    init_session()
    dictionary_key_replacements()
    
    material_display = material.replace("_"," ").lower().title()
    tier = calcs.determine_tier(material)
    
    return render_template('newworld/material_primary.html', material=material_display, tier=tier)


@newworld.route('/material_primary_hx/<material>', methods=['GET', 'POST'])
def material_table(material):
    init_session()
    
    if 'price_list' in session:
        price_dict = session['price_list']
    force_load = force_load_server_api_check()
    if force_load is not None:
        price_dict = force_load

    material_check = material.replace(" ","_").lower()
    discipline = calcs.determine_discipline(material_check)
    if "update_quantity" in request.args:
        if request.args['update_quantity'] == "":
            quantity = 1
        else:
            quantity = max(int(request.args['update_quantity']), 1)
    else:
        quantity = 1
    
    if discipline == "smelting_precious":
        skill_level = session['skill_levels']['refining']['smelting']
        gear_set = session['gear_sets']['smelting']
    else:
        skill_level = session['skill_levels']['refining'][discipline]
        gear_set = session['gear_sets'][discipline]
    
    taxes_fees = session['taxes_fees']
    
    _data, specific_elemental_lodestone = calcs.ingredients_needed_to_refine(discipline, material_check, quantity, skill_level, gear_set, price_dict, taxes_fees)
    
    material_display = material.replace("_"," ").lower().title()
    
    return render_template('newworld/material_primary_hx.html', quantity=quantity, material=material_display, ele_lodestone=specific_elemental_lodestone, _data=_data)


@newworld.route('/material_raw/<material>', methods=['GET', 'POST'])
def material_raw(material):
    init_session()
    dictionary_key_replacements()
    
    material_display = material.replace("_"," ").lower().title()
    tier = calcs.determine_tier(material)
    
    return render_template('newworld/material_raw.html', material=material_display, tier=tier)


@newworld.route('/material_raw_hx/<material>', methods=['GET', 'POST'])
def material_raw_hx(material):
    init_session()
    
    if 'price_list' in session:
        price_dict = session['price_list']
    force_load = force_load_server_api_check()
    if force_load is not None:
        price_dict = force_load

    material_check = material.replace(" ","_").lower()
    discipline = calcs.determine_discipline(material_check)
    if "quantity_have" in request.args:
        if request.args['quantity_have'] == "":
            quantity = 1
        else:
            quantity = max(int(request.args['quantity_have']), 1)
    else:
        quantity = 1
    
    if discipline == "smelting_precious":
        skill_level = session['skill_levels']['refining']['smelting']
        gear_set = session['gear_sets']['smelting']
    else:
        skill_level = session['skill_levels']['refining'][discipline]
        gear_set = session['gear_sets'][discipline]
    
    taxes_fees = session['taxes_fees']
    
    data = calcs.refining_up_profitability_table(discipline, material_check, quantity, skill_level, gear_set, price_dict, taxes_fees)
    
    material_display = material.replace("_"," ").lower().title()

    return render_template('newworld/material_raw_hx.html', data=data, quantity=quantity, material=material_display)


@newworld.route('/material_price_hx/<material>', methods=['GET', 'POST'])
def material_price_hx(material):
    init_session()
    dictionary_key_replacements()
    
    if 'price_list' in session:
        price_dict = session['price_list']
    force_load = force_load_server_api_check()
    if force_load is not None:
        price_dict = force_load
    
    material_check = material.replace(" ","_").lower()
    discipline = calcs.determine_discipline(material_check)
    
    if material_check == "orichalcum_ingot_platinum":
        material_price = price_dict["smelting"]["orichalcum_ingot"]
    else:
        material_price = price_dict[discipline][material_check]
    
    return render_template('newworld/material_price_hx.html', material_price=material_price)
    

@newworld.route('/server_api', methods=['GET', 'POST'])
def server_api():
    init_session()
    dictionary_key_replacements()
    
    search = search_function()
    if search:
        return redirect(url_for('newworld.material', material=search))

    server_dict = {}
    basedir = os.path.abspath(os.path.dirname(__file__))
    server_list_file = os.path.join(basedir, '../static/newworld/txt/api_server_list.txt')
    with open(server_list_file) as file:
        lines = file.readlines()
        lines.sort()
        for line in lines:
            name, num = line.rstrip().lower().split(",")
            server_dict[name] = num

    if 'price_list' in session:
        price_dict = session['price_list']
        
    copy_available = False
    if 'server_api' in session:
        server_name = session['server_api']['server_name']
        if server_name:
            copy_available = True
            server_data = load_api_server_data(server_name)
            if server_data:
                if 'items' in server_data:
                    price_dict = server_data['items']
                    
    if "load_server" in request.form:
        if "servers" in request.form:
            server_id = request.form["servers"]
            market_dict = db_scripts.load_market_server(server_id)

            if market_dict:
                item_dict = market_dict['items']
                price_dict = copy.deepcopy(session['price_list'])
                for key, value in price_dict.items():
                    for mat in value.keys():
                        if mat in item_dict:
                            price_dict[key][mat] = item_dict[mat]

                copy_available = True
                session['server_api'] = {
                    'server_name': market_dict['name'],
                    'server_id': server_id,
                    'last_update': market_dict['last_update'],
                    'force_load': True
                }

    # if "load_all" in request.form:
    #     stopwatch = db_scripts.timer()
    #     full_server = db_scripts.request_nwmarketprices(stopwatch)
        
    template_order = player_data.trade_post_order()
    trophy_order = player_data.trade_post_trophy_order()
    
    return render_template('newworld/server_api.html', server_dict=server_dict, price_list=price_dict, template_order=template_order, trophy_order=trophy_order,copy_available=copy_available)


@newworld.route('/copy_server_data',methods=['GET', 'POST'])
def copy_server_data():
    if 'server_api' in session:
        server_name = session['server_api']['server_name']
        if server_name:
            server_data = load_api_server_data(server_name)
            if server_data:
                if 'items' in server_data:
                    session['price_list'] = server_data['items']

    return """
    <button class="btn btn-outline-light loadMarket" type="submit" hx-post="/newworld/copy_server_data" hx-target="#copy_server_div" hx-confirm="This will override your Trade Post prices"> Copy All</button>
    """
    
    
@newworld.route('/server_api_hx', methods=['GET', 'POST'])
def server_api_hx():
    init_session()
    dictionary_key_replacements()
    
    template_order = player_data.trade_post_order()
    trophy_order = player_data.trade_post_trophy_order()

    if 'price_list' in session:
        price_dict = session['price_list']
    if 'server_api' in session:
        server_name = session['server_api']['server_name']
        if server_name:
            server_data = load_api_server_data(server_name)
            if server_data:
                if 'items' in server_data:
                    price_dict = server_data['items']

    return render_template('newworld/server_api_hx.html', price_list=price_dict, template_order=template_order, trophy_order=trophy_order)


@newworld.route('/navbar_api_hx', defaults={'material':None}, methods=['GET', 'POST'])
@newworld.route('/navbar_api_hx/<material>', methods=['GET', 'POST'])
def navbar_api_hx(material):
    material_hx = None
    if material:
        material_hx = material.lower().replace(" ","_") 

    force_load = session['server_api']['force_load']
    
    if force_load:
        session['server_api']['force_load'] = False
        status = 'Load API'
        css_class = "btn-outline-secondary"

    else:
        session['server_api']['force_load'] = True
        status = 'API Active'
        css_class = "btn-outline-success"

    return render_template('newworld/navbar_api_hx.html', status=status, css_class=css_class, material=material_hx)


@newworld.route('/taxes_and_bonuses', methods=['GET', 'POST'])
def taxes_and_bonuses():
    init_session()
    dictionary_key_replacements()

    search = search_function()
    if search:
        return redirect(url_for('newworld.material', material=search))
    
    taxes_fees = session['taxes_fees']              
                        
    return render_template('newworld/taxes_and_bonuses.html', taxes_fees=taxes_fees)
    

@newworld.route('/taxes_and_bonuses_hx', methods=['GET', 'POST'])
def taxes_and_bonuses_hx():
    search = search_function()
    if search:
        return redirect(url_for('newworld.material', material=search))
    
    if request.method == 'POST':
        if "save" in request.form:
            for i in session['taxes_fees'].keys():
                if i == "territory":
                    for j in session['taxes_fees'][i].keys():
                        if j in request.form:
                            session['taxes_fees'][i][j] = True
                        else:
                            session['taxes_fees'][i][j] = False
                else:
                    for j in session['taxes_fees'][i].keys():
                        if j == 'duration':
                            session['taxes_fees'][i][j] = request.form[j]
                        elif j == 'tax':
                            session['taxes_fees'][i][j] = 2.5
                        else:
                            session['taxes_fees'][i][j] = float(request.form[j])   
    
    taxes_fees = session['taxes_fees']              
                
    return render_template('newworld/taxes_and_bonuses_hx.html', taxes_fees=taxes_fees)


@newworld.route('/datalist', methods=['GET', 'POST'])
def datalist():
    basedir = os.path.abspath(os.path.dirname(__file__))
    primary_file = os.path.join(basedir, '../static/newworld/txt/primary_ingredients.txt')
    with open(primary_file) as file:
        lines = file.readlines()
        datalist = [line.rstrip().lower() for line in lines]

    secondary_file = os.path.join(basedir, '../static/newworld/txt/secondary_ingredients.txt')
    with open(secondary_file) as file_2:
        lines = file_2.readlines()
        datalist.extend([line.rstrip().lower() for line in lines])

    components_file = os.path.join(basedir, '../static/newworld/txt/components.txt')
    with open(components_file) as file_3:
        lines = file_3.readlines()
        datalist.extend([line.rstrip().lower() for line in lines])
        
    arcana_file = os.path.join(basedir, '../static/newworld/txt/arcana.txt')
    with open(arcana_file) as file_4:
        lines = file_4.readlines()
        datalist.extend([line.rstrip().lower() for line in lines])
    
    trophies_file = os.path.join(basedir, '../static/newworld/txt/trophies.txt')
    with open(trophies_file) as file_5:
        lines = file_5.readlines()
        datalist.extend([line.rstrip().lower() for line in lines])

    parsed_list=[]
    return_length = 0
    if request.method == "GET":
        if 'search' in request.args:
            if len(request.args['search']) > 0:
                datalist_search = request.args['search'].lower()

                parsed_list = [line.title() for line in datalist if datalist_search == line[0:len(datalist_search)]]

                if len(parsed_list) == 0:
                    parsed_list = [line.title() for line in datalist if datalist_search in line]

                parsed_list.sort()
                return_length = min(5, len(parsed_list))
                
                if len(parsed_list) > 0:
                    return render_template('newworld/datalist.html', datalist=parsed_list[0:return_length])
    return render_template('newworld/datalist.html', datalist=parsed_list)


@newworld.route('/market_calculator', methods=['GET', 'POST'])
def market_calculator():
    init_session()
    dictionary_key_replacements()

    search = search_function()
    if search:
        return redirect(url_for('newworld.material', material=search))

    return render_template('newworld/market_calculator.html')
    
    
@newworld.route('/market_calculator_hx', methods=['GET', 'POST'])
def market_calculator_hx():
    if 'taxes_fees' in session:
        taxes_fees = session['taxes_fees']
    
    purchase_price, purchase_quant, sell_price, sell_quant = 1,1,1,1
    p_price, p_quant, s_price, s_quant = False, False, False, False
    only_purchase = False
    blank_form = False
    if 'purchase_price' in request.form:
        try:
            purchase_price = float(request.form['purchase_price'])
            p_price = True
        except:
            p_price = False
    if 'purchase_quant' in request.form:
        try:
            purchase_quant = int(request.form['purchase_quant'])
            p_quant = True
        except:
            p_quant = False
    if 'sell_price' in request.form:
        try:
            sell_price = float(request.form['sell_price'])
            s_price = True
        except:
            s_price = False
    if 'sell_quant' in request.form:
        try:
            sell_quant = int(request.form['sell_quant'])
            s_quant = True
        except:
            s_quant = False
            
    if s_price == False or s_quant == False and p_price == True and p_quant == True:
        only_purchase = True
    else:
        only_purchase = False
    if s_price == False and s_quant == False and p_price == False and p_quant == False: 
        blank_form = True
        only_purchase = False
    
    if blank_form == False:
        base_purchase = round(purchase_price * purchase_quant, 2)
        buy_tax = round(calcs.apply_trade_post_tax_buy(base_purchase, taxes_fees), 2)
        final_price = round(base_purchase + buy_tax, 2)
        
        base_value = round(sell_price * sell_quant, 2)
        sell_tax = round(calcs.determing_trade_post_sell_fee(base_value, taxes_fees), 2)
        transaction_charge = round(base_value * (taxes_fees['trade_post']['tax'] / 100), 2)
        final_value = round(base_value - transaction_charge - sell_tax, 2)
        
        total_profit = round(final_value - final_price, 2)
        profit_per_item = round(total_profit / sell_quant, 2)
        profit_margin = round((final_value - final_price) / final_price * 100, 2)
        
        break_even = calcs.determine_break_even(purchase_price, purchase_quant, taxes_fees)
        break_one = round(break_even['break_even_one'], 2)
        break_quant = round(break_even['break_even_quant'], 2)
        
    elif blank_form == True and only_purchase == True:
        base_purchase = round(purchase_price * purchase_quant, 2)
        buy_tax = round(calcs.apply_trade_post_tax_buy(base_purchase, taxes_fees), 2)
        final_price = round(base_purchase + buy_tax, 2)
        
        base_value, sell_tax , transaction_charge, final_value = 0, 0, 0, 0
        total_profit, profit_per_item, profit_margin = 0, 0, 0
        
        break_even = calcs.determine_break_even(purchase_price, purchase_quant, taxes_fees)
        break_one = break_even['break_even_one']
        break_quant = break_even['break_even_quant']
        
    else:
        base_purchase, buy_tax, final_price = 0, 0, 0
        base_value, sell_tax , transaction_charge, final_value = 0, 0, 0, 0
        total_profit, profit_per_item, profit_margin = 0, 0, 0
        break_one, break_quant = 0, 0
    
    data = {
        'price': {
            'base': base_purchase,
            'listing_fee': buy_tax,
            'final_price': final_price
        },
        'value': {
            'base': base_value,
            'transaction_charge': transaction_charge,
            'listing_fee': sell_tax,
            'final_value': final_value
        },
        'profit': {
            'total': total_profit,
            'profit_per_item': profit_per_item,
            'profit_margin': profit_margin
        },
        'break_even': {
            'one': break_one,
            'quant': break_quant
        }
    }
    
    return render_template('newworld/market_calculator_hx.html', data=data, only_purchase=only_purchase, purchase_quant=purchase_quant)


@newworld.route('/crafting/trophy', methods=['GET', 'POST'])
def trophy_calculator():
    init_session()
    dictionary_key_replacements()
    
    search = search_function()
    if search:
        return redirect(url_for('newworld.material', material=search))

    return render_template('newworld/trophy_calculator.html')


@newworld.route('/crafting/trophy_hx', methods=['GET', 'POST'])
def trophy_calculator_hx():
    template_order = player_data.trade_post_trophy_order()

    if 'price_list' in session:
        price_dict = session['price_list']
    force_load = force_load_server_api_check()
    if force_load is not None:
        price_dict = force_load
    
    taxes_fees = session['taxes_fees']
    skill_level = session['skill_levels']['refining']
    gear_set = session['gear_sets']
    taxes_fees = session['taxes_fees']
    
    all_tiers_all_routes, financial_data = calcs.tp_cost_to_refine_all_routes_all_tiers(price_dict, session['skill_levels']['refining'], session['gear_sets'], taxes_fees)
    cheapest_route = calcs.cheapest_tp_cost_route_to_refine_each_tier(price_dict, all_tiers_all_routes, taxes_fees, financial_data)
    
    data = calcs.calculate_trophy_profitability(cheapest_route, price_dict, taxes_fees, skill_level, gear_set)
    
    return render_template('newworld/trophy_calculator_hx.html', data=data, template_order=template_order)


@newworld.route('/trading_post', methods=['GET', 'POST'])
def trading_post():
    init_session()
    dictionary_key_replacements()
    
    search = search_function()
    if search:
        return redirect(url_for('newworld.material', material=search))
    
    server_name = None
    if 'server_api' in session:
        server_name = session['server_api']['server_name']
        
    return render_template('newworld/trading_post.html', server=server_name)


@newworld.route('/trading_post_hx', methods=['GET', 'POST'])
def trading_post_hx():
    server_name = None
    if 'server_api' in session:
        server_name = session['server_api']['server_name']
        if server_name:
            try:
                item_data = db_scripts.retrieve_itemdata_for_tradingpost(server_name)
                item_data_price = sorted(item_data, key=lambda d: d['Price'])
            except Exception as e:
                print(e)
                item_data_price = None
    else:
        item_data_price = None
        
    return render_template('newworld/trading_post_hx.html', item_data=item_data_price)


@newworld.route('/test_scripts', methods=['GET', 'POST'])
def test_scripts():
    
    # update_table = db_scripts.import_itemdata_to_table()
    # print(update_table)
    # rename = db_scripts.rename_default_groups()
    # print(rename)
    return redirect(url_for("newworld.home"))