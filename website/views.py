from flask import Blueprint, request, flash, render_template, redirect, url_for, escape, session
from . import player_data, calculations as calcs



views = Blueprint('views', __name__)


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


@views.route('/', methods=['GET', 'POST'])
def home():
    init_session()
        
    return render_template('base.html')


@views.route('/skills', methods=['GET', 'POST'])
def skills():
    init_session()
    
    if request.method == 'POST':
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
    
    return render_template('skills.html', skill_levels=session['skill_levels'])


@views.route('/gearsets', methods=['GET', 'POST'])
def gearsets():
    init_session()
    
    if request.method == 'POST':
        for i in session['gear_sets'].keys():
            for j in session['gear_sets'][i].keys():
                if j in request.form:
                    session['gear_sets'][i][j] = True
                else:
                    session['gear_sets'][i][j] = False    

    return render_template('gearsets.html', gear_sets=session['gear_sets'])


@views.route('/tradepost', methods=['GET', 'POST'])
def tradepost():
    init_session()
    
    if request.method == 'POST':
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
    
    return render_template('tradepost.html', price_list=session['price_list'])


@views.route('/refined_material_cost', methods=['GET', 'POST'])
def refined_material_cost():
    init_session()
    
    cheapest_route = {
        "leatherworking": calcs.cheapest_route_leatherworking(session['price_list'], session['skill_levels']['refining']['leatherworking'], session['gear_sets']['leatherworking']),
        "smelting": calcs.cheapest_route_smelting(session['price_list'], session['skill_levels']['refining']['smelting'], session['gear_sets']['smelting']),
        "stone_cutting": calcs.cheapest_route_stone_cutting(session['price_list'], session['skill_levels']['refining']['stone_cutting'], session['gear_sets']['stone_cutting']),
        "weaving": calcs.cheapest_route_weaving(session['price_list'], session['skill_levels']['refining']['weaving'], session['gear_sets']['weaving']),
        "woodworking": calcs.cheapest_route_woodworking(session['price_list'], session['skill_levels']['refining']['woodworking'], session['gear_sets']['woodworking'])
    }

    return render_template('refined_material_cost.html', cheapest_route=cheapest_route)


@views.route('/refined_material_ingredients', methods=['GET', 'POST'])
def refined_material_ingredients():
    init_session()
    

    return render_template('refined_material_ingredients.html')


@views.route('/markets', methods=['GET', 'POST'])
def markets():
    init_session()
    
    return render_template('markets.html')


@views.route('/dropdown_show', methods=['GET', 'POST'])
def dropdown_show():
    
    return render_template('dropdown_show.html')


@views.route('/dropdown_hide', methods=['GET', 'POST'])
def dropdown_hide():
    
    return render_template('dropdown_hide.html')