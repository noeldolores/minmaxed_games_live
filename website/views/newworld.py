from flask import Blueprint, request, flash, render_template, redirect, url_for, escape, session

from ..scripts.newworld import calculations as calcs
from ..scripts.newworld import player_data
import os


newworld = Blueprint('newworld', __name__)


def init_session():
    if 'first_visit' not in session:
        session.permanent = True
        session['first_visit'] = True
        session['skill_levels'] = player_data.init_skill_levels()
        session['gear_sets'] = player_data.init_gear_sets()
        session['price_list'] = player_data.init_price_list()
        
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
    primary_list = []
    secondary_list = []
    components_list = []
    
    with open(primary_ingredients) as file:
        lines = file.readlines()
        primary_list = [line.rstrip().lower() for line in lines]
    
    with open(secondary_ingredients) as file_2:
        lines = file_2.readlines()
        secondary_list = [line.rstrip().lower() for line in lines]
        
    with open(components) as file_3:
        lines = file_3.readlines()
        components_list = [line.rstrip().lower() for line in lines]
    
    if search in primary_list or search in secondary_list or search in components_list:
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
    
    if material in primary_list:
        return "primary"
    elif material in secondary_list:
        return "secondary"
    elif material in components_list:
        return "component"
    return None


@newworld.route('/', methods=['GET', 'POST'])
def home():
    init_session()
    search = search_function()
    if search:
        return redirect(url_for("newworld.material", material=search))

    return render_template('newworld/base.html')


@newworld.route('/skills', methods=['GET', 'POST'])
def skills():
    init_session()
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


@newworld.route('/tradepost', methods=['GET', 'POST'])
def tradepost():
    init_session()
    search = search_function()
    if search:
        return redirect(url_for('newworld.material', material=search))
    
    template_order = player_data.trade_post_order()
    
    return render_template('newworld/tradepost.html', price_list=session['price_list'], template_order=template_order)

@newworld.route('/tradepost_hx', methods=['GET', 'POST'])
def tradepost_hx():
    template_order = player_data.trade_post_order()
    
    if request.method == 'POST':
        if "save" in request.form:
            session['price_list'] = {
                "refining_components" : {
                    "aged_tannin": strip_leading_zeros(True, request.form['aged_tannin']),
                    "obsidian_flux": strip_leading_zeros(True, request.form['obsidian_flux']),
                    "obsidian_sandpaper": strip_leading_zeros(True, request.form['obsidian_sandpaper']),
                    "wireweave": strip_leading_zeros(True, request.form['wireweave']),
                    "pure_solvent" : strip_leading_zeros(True, request.form['pure_solvent'])
                },
                "leatherworking" : {
                    "rawhide": strip_leading_zeros(True, request.form['rawhide']),
                    "coarse_leather": strip_leading_zeros(True, request.form['coarse_leather']),
                    "rugged_leather": strip_leading_zeros(True, request.form['rugged_leather']),
                    "layered_leather": strip_leading_zeros(True, request.form['layered_leather']),
                    "infused_leather": strip_leading_zeros(True, request.form['infused_leather']),
                    "runic_leather": strip_leading_zeros(True, request.form['runic_leather']),
                    "thick_hide": strip_leading_zeros(True, request.form['thick_hide']),
                    "iron_hide": strip_leading_zeros(True, request.form['iron_hide']),
                    "smolderhide": strip_leading_zeros(True, request.form['smolderhide']),
                    "scarhide": strip_leading_zeros(True, request.form['scarhide'])
                },
                "smelting" : {
                    "iron_ore" : strip_leading_zeros(True, request.form['iron_ore']),
                    "iron_ingot" : strip_leading_zeros(True, request.form['iron_ingot']),
                    "steel_ingot" : strip_leading_zeros(True, request.form['steel_ingot']),
                    "starmetal_ingot" : strip_leading_zeros(True, request.form['starmetal_ingot']),
                    "orichalcum_ingot" : strip_leading_zeros(True, request.form['orichalcum_ingot']),
                    "starmetal_ore" : strip_leading_zeros(True, request.form['starmetal_ore']),
                    "orichalcum_ore" : strip_leading_zeros(True, request.form['orichalcum_ore']),
                    "asmodeum" : strip_leading_zeros(True, request.form['asmodeum']),
                    "charcoal" : strip_leading_zeros(True, request.form['charcoal']),
                    "tolvium" : strip_leading_zeros(True, request.form['tolvium']),
                    "cinnabar" : strip_leading_zeros(True, request.form['cinnabar']),
                    "silver_ore" : strip_leading_zeros(True, request.form['silver_ore']),
                    "silver_ingot" : strip_leading_zeros(True, request.form['silver_ingot']),
                    "gold_ingot" : strip_leading_zeros(True, request.form['gold_ingot']),
                    "platinum_ingot" : strip_leading_zeros(True, request.form['platinum_ingot']),
                    "gold_ore" : strip_leading_zeros(True, request.form['gold_ore']),
                    "platinum_ore" : strip_leading_zeros(True, request.form['platinum_ore'])
                },
                "stone_cutting" : {
                    "stone": strip_leading_zeros(True, request.form['stone']),
                    "stone_block": strip_leading_zeros(True, request.form['stone_block']),
                    "stone_brick": strip_leading_zeros(True, request.form['stone_brick']),
                    "lodestone_brick": strip_leading_zeros(True, request.form['lodestone_brick']),
                    "obsidian_voidstone" : strip_leading_zeros(True, request.form['obsidian_voidstone']),
                    "runestone": strip_leading_zeros(True, request.form['runestone']),
                    "lodestone": strip_leading_zeros(True, request.form['lodestone']),
                    "molten_lodestone": strip_leading_zeros(True, request.form['molten_lodestone']),
                    "loamy_lodestone": strip_leading_zeros(True, request.form['loamy_lodestone']),
                    "shocking_lodestone": strip_leading_zeros(True, request.form['shocking_lodestone']),
                    "crystalline_lodestone" : strip_leading_zeros(True, request.form['crystalline_lodestone']),
                    "freezing_lodestone": strip_leading_zeros(True, request.form['freezing_lodestone']),
                    "putrid_lodestone": strip_leading_zeros(True, request.form['putrid_lodestone']),
                    "gleaming_lodestone": strip_leading_zeros(True, request.form['gleaming_lodestone'])
                },
                "weaving" : {
                    "fibers": strip_leading_zeros(True, request.form['fibers']),
                    "linen": strip_leading_zeros(True, request.form['linen']),
                    "sateen": strip_leading_zeros(True, request.form['sateen']),
                    "silk": strip_leading_zeros(True, request.form['silk']),
                    "infused_silk": strip_leading_zeros(True, request.form['infused_silk']),
                    "phoenixweave": strip_leading_zeros(True, request.form['phoenixweave']),
                    "silk_threads": strip_leading_zeros(True, request.form['silk_threads']),
                    "wirefiber": strip_leading_zeros(True, request.form['wirefiber']),
                    "scalecloth": strip_leading_zeros(True, request.form['scalecloth']),
                    "blisterweave": strip_leading_zeros(True, request.form['blisterweave'])
                },
                "woodworking" : {
                    "green_wood" : strip_leading_zeros(True, request.form['green_wood']),
                    "timber" : strip_leading_zeros(True, request.form['timber']),
                    "lumber" : strip_leading_zeros(True, request.form['lumber']),
                    "wyrdwood_planks" : strip_leading_zeros(True, request.form['wyrdwood_planks']),
                    "ironwood_planks" : strip_leading_zeros(True, request.form['ironwood_planks']),
                    "glittering_ebony" : strip_leading_zeros(True, request.form['glittering_ebony']),
                    "aged_wood" : strip_leading_zeros(True, request.form['aged_wood']),
                    "wyrdwood" : strip_leading_zeros(True, request.form['wyrdwood']),
                    "ironwood" : strip_leading_zeros(True, request.form['ironwood']),
                    "wildwood" : strip_leading_zeros(True, request.form['wildwood']),
                    "barbvine" : strip_leading_zeros(True, request.form['barbvine'])
                } 
            }

    return render_template('newworld/tradepost_hx.html', price_list=session['price_list'], template_order=template_order)
    
    
@newworld.route('/refining', methods=['GET', 'POST'])
def refining():
    init_session()
    search = search_function()
    if search:
        return redirect(url_for('newworld.material', material=search))
    
    template_order = player_data.refining_order()
    
    cheapest_route = {
        "leatherworking": calcs.cheapest_route_leatherworking(session['price_list'], session['skill_levels']['refining']['leatherworking'], session['gear_sets']['leatherworking']),
        "smelting": calcs.cheapest_route_smelting(session['price_list'], session['skill_levels']['refining']['smelting'], session['gear_sets']['smelting']),
        "stone_cutting": calcs.cheapest_route_stone_cutting(session['price_list'], session['skill_levels']['refining']['stone_cutting'], session['gear_sets']['stone_cutting']),
        "weaving": calcs.cheapest_route_weaving(session['price_list'], session['skill_levels']['refining']['weaving'], session['gear_sets']['weaving']),
        "woodworking": calcs.cheapest_route_woodworking(session['price_list'], session['skill_levels']['refining']['woodworking'], session['gear_sets']['woodworking'])
    }

    return render_template('newworld/refining.html', cheapest_route=cheapest_route, template_order=template_order)


@newworld.route('/material/<material>', methods=['GET', 'POST'])
def material(material):
    init_session()
    search = search_function()
    if search:
        return redirect(url_for('newworld.material', material=search))
    
    category = determine_material_category(material.replace("_"," "))
    material_display = material.replace("_"," ").lower().title()
    quantity = 1
    
    if category == "primary":
        material_check = material.replace(" ","_").lower()
        discipline = calcs.determine_discipline(material_check)
        
        if "update_quantity" in request.args:
            if request.args['update_quantity'] != "":
                quantity = max(int(str(escape(request.args['update_quantity']))), 1)

        material_data, component_data, data = calcs.ingredients_needed_to_refine(discipline, material_check, quantity, session['skill_levels']['refining'][discipline], session['gear_sets'][discipline])
    
        return render_template('newworld/primary_material.html', data=data, quantity=quantity, material=material_display,material_data=material_data, component_data=component_data) 
     
    if category == "secondary":
        return render_template('newworld/secondary_material.html', material=material_display)
    
    if category == "component":  
        return render_template('newworld/component_material.html', material=material_display)


@newworld.route('/primary_material_hx/<material>', methods=['GET', 'POST'])
def material_table(material):

    material_check = material.replace(" ","_").lower()
    discipline = calcs.determine_discipline(material_check)
    if "update_quantity" in request.args:
        if request.args['update_quantity'] == "":
            quantity = 1
        else:
            quantity = max(int(str(escape(request.args['update_quantity']))), 1)
    material_data, component_data, data = calcs.ingredients_needed_to_refine(discipline, material_check, quantity, session['skill_levels']['refining'][discipline], session['gear_sets'][discipline])
    
    material_display = material.replace("_"," ").lower().title()
    
    return render_template('newworld/primary_material_hx.html', data=data, quantity=quantity, material=material_display,material_data=material_data, component_data=component_data)




@newworld.route('/refined_material_ingredients', methods=['GET', 'POST'])
def refined_material_ingredients():
    init_session()
    search = search_function()
    if search:
        return redirect(url_for('newworld.material', material=search))

    return render_template('newworld/refined_material_ingredients.html')


@newworld.route('/markets', methods=['GET', 'POST'])
def markets():
    init_session()
    search = search_function()
    if search:
        return redirect(url_for('newworld.material', material=search))
    
    return render_template('newworld/markets.html')


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

    return render_template('newworld/datalist.html', datalist=parsed_list[0:return_length])


@newworld.route('/dropdown_show', methods=['GET', 'POST'])
def dropdown_show():
    
    return render_template('newworld/dropdown_show.html')


@newworld.route('/dropdown_hide', methods=['GET', 'POST'])
def dropdown_hide():
    
    return render_template('newworld/dropdown_hide.html')