#!/usr/bin/python3
import math
from . import player_data
import copy



conversions = {
    "leatherworking" : {
        "refining_component" : "aged_tannin",
        "coarse_leather" : {
            "tier" : 1,
            "primary" : "rawhide",
            "rawhide": 4
        },
        "rugged_leather": {
            "tier" : 2,
            "primary" : "coarse_leather",
            "coarse_leather": 4
        },
        "layered_leather" : {
            "tier" : 3,
            "primary" : "rugged_leather",
            "rugged_leather": 2,
            "thick_hide" : 6
        },
        "infused_leather" : {
            "tier" : 4,
            "primary" : "layered_leather",
            "layered_leather" : 2,
            "iron_hide" : 8
        },
        "runic_leather" : {
            "tier" : 5,
            "primary" : "infused_leather",
            "infused_leather" : 5,
            "smolderhide" : 1,
            "scarhide" : 1
        }
    },
    "smelting" : {
        "refining_component" : "obsidian_flux",
        "iron_ingot" : {
            "tier" : 1,
            "primary" : "iron_ore",
            "iron_ore": 4
        },
        "steel_ingot": {
            "tier" : 2,
            "primary" : "iron_ingot",
            "iron_ingot": 3,
            "charcoal" : 2
        },
        "starmetal_ingot" : {
            "tier" : 3,
            "primary" : "steel_ingot",
            "steel_ingot": 2,
            "starmetal_ore": 6,
            "charcoal" : 2
        },
        "orichalcum_ingot" : {
            "tier" : 4,
            "primary" : "starmetal_ingot",
            "starmetal_ingot" : 2,
            "orichalcum_ore": 8,
            "charcoal" : 2
        },
        "asmodeum" : {
            "tier" : 5,
            "primary" : "orichalcum_ingot",
            "orichalcum_ingot" : 5,
            "tolvium" : 1,
            "cinnabar" : 1,
            "charcoal" : 2
        }
    },
    "smelting_precious" : {
        "refining_component" : "obsidian_flux",
        "silver_ingot" : {
            "tier" : 1,
            "primary" : "silver_ore",
            "silver_ore": 4
        },
        "gold_ingot": {
            "tier" : 2,
            "primary" : "silver_ingot",
            "silver_ingot": 2,
            "gold_ore" : 5
        },
        "platinum_ingot" : {
            "tier" : 3,
            "primary" : "gold_ingot",
            "gold_ingot": 2,
            "platinum_ore": 6
        },
        "orichalcum_ingot_platinum" : {
            "tier" : 4,
            "primary" : "platinum_ingot",
            "orichalcum_ore": 8,
            "platinum_ingot" : 3,
            "charcoal" : 2
        },
    },
    "stone_cutting" : {
        "refining_component" : "obsidian_sandpaper",
        "stone_block" : {
            "tier" : 1,
            "primary" : "stone",
            "stone": 4
        },
        "stone_brick": {
            "tier" : 2,
            "primary" : "stone_block",
            "stone_block": 4
        },
        "lodestone_brick" : {
            "tier" : 3,
            "primary" : "stone_brick",
            "stone_brick": 2,
            "lodestone" : 6
        },
        "obsidian_voidstone" : {
            "tier" : 4,
            "primary" : "lodestone_brick",
            "lodestone_brick" : 8,
            "lodestone" : 2,
            "elemental_lodestone" : 1
        },
        "runestone" : {
            "tier" : 5,
            "primary" : "obsidian_voidstone",
            "obsidian_voidstone" : 5,
            "elemental_lodestone" : 1
        }
    },
    "weaving" : {
        "refining_component" : "wireweave",
        "linen" : {
            "tier" : 1,
            "primary" : "fibers",
            "fibers": 4
        },
        "sateen": {
            "tier" : 2,
            "primary" : "linen",
            "linen": 4
        },
        "silk" : {
            "tier" : 3,
            "primary" : "sateen",
            "sateen": 2,
            "silk_threads" : 6
        },
        "infused_silk" : {
            "tier" : 4,
            "primary" : "silk",
            "silk" : 2,
            "wirefiber" : 8
        },
        "phoenixweave" : {
            "tier" : 5,
            "primary" : "infused_silk",
            "infused_silk" : 5,
            "scalecloth" : 1,
            "blisterweave" : 1
        }
    },
    "woodworking" : {
        "refining_component" : "obsidian_sandpaper",
        "timber" : {
            "tier" : 1,
            "primary" : "green_wood",
            "green_wood": 4
        },
        "lumber": {
            "tier" : 2,
            "primary" : "timber",
            "timber": 2,
            "aged_wood": 4
        },
        "wyrdwood_planks" : {
            "tier" : 3,
            "primary" : "lumber",
            "lumber": 2,
            "wyrdwood" : 6
        },
        "ironwood_planks" : {
            "tier" : 4,
            "primary" : "wyrdwood_planks",
            "wyrdwood_planks" : 2,
            "ironwood" : 8
        },
        "glittering_ebony" : {
            "tier" : 5,
            "primary" : "ironwood_planks",
            "ironwood_planks" : 5,
            "wildwood" : 1,
            "barbvine" : 1
        }
    }
}

alchemy_conversions = {
    "mote": {
        "tier": 0
    },
    "wisp": {
        "tier": 2,
        'primary': "mote",
        "mote": 5
    },
    "essence": {
        "tier": 3,
        'primary': "wisp",
        'wisp': 4
    },
    "quintessence": {
        "tier": 5,
        'primary': "essence",
        'essence': 3
    }
}

def cost_comparison(list_of_prices):
    cheapest_price = min(list_of_prices, key=lambda tup: tup[1])

    return cheapest_price


def gear_set_bonus(gear_set):
    count = sum(int(i) > 0 for i in gear_set.values())
    bonus = count * 0.02

    return bonus


def total_craft_bonus(skill_level, gear_set, discipline, first_light):
    fl_bonus = 0
    if first_light == True:
        fl_bonus = 0.1
    skill_bonus = int(skill_level) * 0.001
    gear_bonus = 0.02 * (sum(int(i) > 0 for i in gear_set.values()))

    tier_1 = 1 + skill_bonus + gear_bonus + fl_bonus
    tier_2 = 1 + 0.75 + max(skill_bonus - 0.02, 0) + gear_bonus + fl_bonus
    tier_3 = 1 + 0.25 + max(skill_bonus - 0.05, 0) + gear_bonus + fl_bonus
    tier_4 = 1 + max(skill_bonus - 0.07, 0) + gear_bonus + fl_bonus
    tier_5 = 1 + max(skill_bonus - 0.2, 0) + gear_bonus + fl_bonus

    if discipline == "leatherworking":
        craft_bonus = {
            "coarse_leather": tier_1,
            "rugged_leather": tier_2,
            "layered_leather": tier_3,
            "infused_leather": tier_4,
            "runic_leather": tier_5
        }
    elif discipline == "smelting":
        craft_bonus = {
            "iron_ingot": tier_1,
            "steel_ingot": tier_2,
            "starmetal_ingot": tier_3,
            "orichalcum_ingot": tier_4,
            "orichalcum_ingot_platinum": tier_4,
            "asmodeum": tier_5,
            "silver_ingot": tier_1,
            "gold_ingot": 1 + 0.5 + max(skill_bonus - 0.05, 0) + gear_bonus + fl_bonus,
            "platinum_ingot": 1 + 0.25 + max(skill_bonus - 0.07, 0) + gear_bonus + fl_bonus#check rate for plat ori
        }
    elif discipline == "smelting_precious":
        craft_bonus = {
            "silver_ingot": tier_1,
            "gold_ingot": 1 + 0.5 + max(skill_bonus - 0.05, 0) + gear_bonus + fl_bonus,
            "platinum_ingot": 1 + 0.25 + max(skill_bonus - 0.07, 0) + gear_bonus + fl_bonus, #check rate for plat ori
            "orichalcum_ingot_platinum": tier_4
        }
    elif discipline == "stone_cutting":
        craft_bonus = {
            "stone_block": tier_1,
            "stone_brick": tier_2,
            "lodestone_brick": tier_3,
            "obsidian_voidstone": tier_4,
            "runestone": tier_5
        }
    elif discipline == "weaving":
        craft_bonus = {
            "linen": tier_1,
            "sateen": tier_2,
            "silk": tier_3,
            "infused_silk": tier_4,
            "phoenixweave": tier_5
        }
    elif discipline == "woodworking":
        craft_bonus = {
            "timber": tier_1,
            "lumber": tier_2,
            "wyrdwood_planks": tier_3,
            "ironwood_planks": tier_4,
            "glittering_ebony": tier_5
        }
    else:
        craft_bonus = None

    return craft_bonus


def tp_margin(tp_cost, lowest_cost):
    if lowest_cost == 0:
        return 0

    return round((tp_cost - lowest_cost) / lowest_cost * 100, 2)


def elemental_lodestone_calcs(prices):
    prices_elemental_lodestones = [
        ("Molten Lodestone", prices['molten_lodestone']),
        ("Loamy Lodestone", prices['loamy_lodestone']),
        ("Shocking Lodestone", prices['shocking_lodestone']),
        ("Crystalline Lodestone", prices['crystalline_lodestone']),
        ("Freezing Lodestone", prices['freezing_lodestone']),
        ("Putrid Lodestone", prices['putrid_lodestone'])
    ]
    return cost_comparison(prices_elemental_lodestones)


def tp_cost_to_refine_all_routes_all_tiers(price_list, skill_level, gear_set, taxes_fees):
    _refining_dict = init_refining_cost_table()
    _financials = init_refining_cost_table()

    for discipline, discipline_data in _refining_dict.items():
        
        if discipline == "smelting_precious":
            skill = skill_level['smelting']
            gear = gear_set['smelting']
        else:
            skill = skill_level[discipline]
            gear = gear_set[discipline]
            
        for material, material_data in discipline_data.items():
            market_value = price_list[discipline][material]
            purchase_total = market_value + apply_trade_post_tax_buy(market_value, taxes_fees)
            
            _refining_dict[discipline][material][material] = purchase_total
            _financials[discipline][material][material] = {
                'sell_profit' : 0,
                'profit_margin' : 0
            }
            
            quantity = 1000
            _data,_ = ingredients_needed_to_refine(discipline, material, quantity, skill, gear, price_list, taxes_fees)

            material_ingredient_list = list(material_data.keys())
            material_ingredient_list.remove(material)
            material_ingredient_list.reverse()

            for i in range(len(material_ingredient_list)):
                _financial = _data['financial'][i]
                _craft_cost = _financial['craft']['final_cost_each']
                _sell_profit = _financial['sell']['final_profit_each']
                _profit_margin = _sell_profit / _craft_cost
                
                _refining_dict[discipline][material][material_ingredient_list[i]] = _craft_cost
                _financials[discipline][material][material_ingredient_list[i]] = {
                    'sell_profit' : _sell_profit,
                    'profit_margin' : _profit_margin
                }
                    
    return _refining_dict, _financials


def cheapest_tp_cost_route_to_refine_each_tier(price_list, refining_dict_full, taxes_fees, financials):
    refining_dict_cheapest = {}
    for discipline, discipline_data in refining_dict_full.items():
        refining_dict_cheapest[discipline] = {}
        for material, material_data in discipline_data.items():
            material_list = list(material_data.items())

            material_from_tp = material_list[0]
            craft_cost = [material_from_tp]
            for i in material_list:
                mat = i[0]
                cost = i[1]
                profit = financials[discipline][material][mat]['sell_profit']
                if profit >= 0.01:
                    craft_cost.append((mat, cost))

            _price_data = cost_comparison(craft_cost)
            tp_flip = financials[discipline][material][_price_data[0]]['sell_profit']
            tp_margin= financials[discipline][material][_price_data[0]]['profit_margin']

            refining_dict_cheapest[discipline][material] = {
                "source": _price_data[0],
                "price" : round(_price_data[1], 2),
                "tp_flip": round(tp_flip, 2),
                "tp_margin": round(tp_margin * 100, 2)
            }
            
        if discipline == "stone_cutting":
            ele_lode = elemental_lodestone_calcs(price_list[discipline])
            refining_dict_cheapest[discipline]["elemental_lodestone"] = {
                "source": ele_lode[0],
                "price" : round(ele_lode[1], 2),
                "tp_flip": "-",
                "tp_margin": "-"
            }
    return refining_dict_cheapest


def ingredients_needed_to_refine(discipline, material, quantity, skill_level, gear_set, price_dict, taxes_fees):
    refine_conversions = conversions[discipline]
    tier = refine_conversions[material]['tier']
    first_light_bonus = taxes_fees['territory']['first_light']
    
    data = {}
    financial = []
    # Init ingredients list and set value of highest tier primary ingredient
    ingredients = {}
    primary_ingredients = []
    refining_component = []
    for key in refine_conversions.keys():
        if key != "refining_component":
            if refine_conversions[key]['tier'] <= tier:
                primary_ingredients.append(refine_conversions[key]['primary'])
                for value in refine_conversions[key]:
                    if value not in ingredients and value != "tier" and value != "primary":
                        if refine_conversions[key]['tier'] == tier: #grab only ingredients that match material tier
                            if primary_ingredients[-1] not in ingredients:
                                target_refine = material
                                target_refine_quant = quantity
                                quant_needed_per_refine = refine_conversions[key][primary_ingredients[-1]]
                                
                                craft_bonus = total_craft_bonus(skill_level, gear_set, discipline, first_light_bonus)[target_refine]
                                ingredients[primary_ingredients[-1]] = quant_needed_per_refine * math.ceil(target_refine_quant * quant_needed_per_refine / craft_bonus / quant_needed_per_refine)

                                if tier != 1:
                                    refining_component.append(ingredients[primary_ingredients[-1]] / quant_needed_per_refine)
                                    
                                else:
                                    refining_component.append(0)
                        else:
                            ingredients[value] = 0

    # Put primary ingredients list in tier order: high->low
    primary_ingredients.reverse()
    
    num_crafts = []
        
    for i in range(len(primary_ingredients)):
        if i == 0:  # Assign the secondary ingredient of the highest tier
            for key, value in refine_conversions[material].items():
                if key != "tier" and key != "primary" and key != primary_ingredients[i]:
                    num_crafts.append(key)
                    ingredients[key] = int(refine_conversions[material][key] * (ingredients[primary_ingredients[i]] / refine_conversions[material][primary_ingredients[i]]))

        else:
            # Assign the next tier primary ingredient
            target_refine = primary_ingredients[i - 1]
            target_refine_quant = ingredients[primary_ingredients[i - 1]]

            quant_needed_per_refine = refine_conversions[primary_ingredients[i - 1]][primary_ingredients[i]]
            craft_bonus = total_craft_bonus(skill_level, gear_set, discipline, first_light_bonus)[target_refine]

            ingredients[primary_ingredients[i]] = quant_needed_per_refine * math.ceil(target_refine_quant * quant_needed_per_refine / craft_bonus / quant_needed_per_refine)

            if i != len(primary_ingredients) - 1:
                refining_component.append(ingredients[primary_ingredients[i]] / quant_needed_per_refine)
            
            # Assign the next tier of the secondary ingredient
            for key, value in refine_conversions[target_refine].items():
                if key != "tier" and key != "primary" and key != primary_ingredients[i]:
                    if target_refine != "lodestone_brick" and target_refine != "obsidian_voidstone":
                        secondary_quant_needed_per_refine = refine_conversions[target_refine][key]
                        ingredients[key] = int(ingredients[primary_ingredients[i]] / quant_needed_per_refine * secondary_quant_needed_per_refine)
                    if target_refine == "obsidian_voidstone":
                        if key != "elemental_lodestone":
                            secondary_quant_needed_per_refine = refine_conversions[target_refine][key]
                            ingredients[key] = int(ingredients[primary_ingredients[i]] / quant_needed_per_refine * secondary_quant_needed_per_refine)
                            
    # Need to clean up, can probably combine with the original script         
    test_refine = refining_component.copy()
    refining_component.insert(0, int(sum(refining_component)))

    final_refine = []
    for i in range(len(test_refine)):
        if i == 0:
            final_refine.append(test_refine[i])
        else:
            final_refine.append(final_refine[i - 1] + test_refine[i])
    final_refine.append(final_refine[-1])
    final_refine.reverse()

    ingredients_list = []
    primary_ingredients.reverse()
    for i in primary_ingredients:
        ingredients_list.append(ingredients.fromkeys(ingredients.keys(), "-"))
        
    for i in range(len(primary_ingredients)):
        ingredients_list[i][primary_ingredients[i]] = ingredients[primary_ingredients[i]]
        if final_refine[0] != 0:
            ingredients_list[i][refine_conversions['refining_component']] = int(final_refine[i])
        current_tier = i + 1
        for key, value in ingredients.items():
            if key not in primary_ingredients:
                for _, v in refine_conversions.items():
                    if type(v) is dict:
                        if v['tier'] >= current_tier:
                            for kk in v.keys():
                                if kk != "primary" and kk != "tier" and kk not in primary_ingredients:
                                    if kk in ingredients:
                                        ingredients_list[i][kk] = ingredients[kk]
                                        if kk == "charcoal":
                                            if material != "orichalcum_ingot_platinum":
                                                ingredients_list[i][kk] = int(ingredients_list[i][refine_conversions['refining_component']] * 2)
                                        if kk == "lodestone" and material != 'lodestone_brick':
                                            if i < 3:
                                                ingredients_list[i]['lodestone'] += int(6 * ingredients['stone_brick'] / refine_conversions['lodestone_brick']['stone_brick'])
                                        if material == "runestone":
                                            if kk == "elemental_lodestone":
                                                if i < 4:
                                                    ingredients_list[i]['elemental_lodestone'] += int(1 * ingredients['lodestone_brick'] / refine_conversions['obsidian_voidstone']['lodestone_brick'])
        

    # Cost Calculations                        
    craft_bonus_dict = total_craft_bonus(skill_level, gear_set, discipline, first_light_bonus)
    
    if len(num_crafts) > 0:
        primary_ing = num_crafts[0] 
    else:
        primary_ing = primary_ingredients[-1]
        
    total_required = ingredients_list[-1][primary_ing]
    required_per_craft = refine_conversions[material][primary_ing]
    
    number_of_crafts = int(total_required / required_per_craft)
    output = round(number_of_crafts * craft_bonus_dict[material])    
    
    specific_elemental_lodestone = None
    if discipline == "stone_cutting":
        specific_elemental_lodestone = elemental_lodestone_calcs(price_dict[discipline])

    refining_tiers = len(primary_ingredients)

    for ref_ings in ingredients_list:
        tp_buy_tax_total = 0
        station_fee_total = 0
        base_cost = 0
        for ingredient in ref_ings.keys():
            if type(ref_ings[ingredient]) is int:
                # Add taxes and fees
                if ingredient in primary_ingredients:
                    _tier = primary_ingredients.index(ingredient)
                    if _tier < refining_tiers:
                        for i in range(_tier, refining_tiers):
                            if primary_ingredients[i] != refine_conversions[material]['primary']:
                                num_required = ingredients[primary_ingredients[i]]
                                num_per_craft = refine_conversions[primary_ingredients[i+1]][primary_ingredients[i]]
                                station_tier = refine_conversions[primary_ingredients[i+1]]['tier']
                            else:
                                num_required = ingredients[refine_conversions[material]['primary']]
                                num_per_craft = refine_conversions[material][primary_ingredients[i]]
                                station_tier = refine_conversions[material]['tier']
                            
                            num_crafts = int(num_required/num_per_craft)                            
                            station_fee = worbench_tax(station_tier, taxes_fees) * num_crafts
                            station_fee_total += station_fee
                
                # Add material cost
                if ingredient in price_dict[discipline]:
                    tp_buy_tax = apply_trade_post_tax_buy(price_dict[discipline][ingredient] * ref_ings[ingredient], taxes_fees)
                    tp_buy_tax_total += tp_buy_tax
                    base_cost += (price_dict[discipline][ingredient] * ref_ings[ingredient]) #+ tp_buy_tax
                elif ingredient in price_dict['refining_component']:
                    tp_buy_tax = apply_trade_post_tax_buy(price_dict['refining_component'][ingredient] * ref_ings[ingredient], taxes_fees)
                    tp_buy_tax_total += tp_buy_tax
                    base_cost += (price_dict['refining_component'][ingredient] * ref_ings[ingredient]) #+ tp_buy_tax
                elif ingredient == "elemental_lodestone":
                    tp_buy_tax = apply_trade_post_tax_buy(specific_elemental_lodestone[1] * ref_ings[ingredient], taxes_fees)
                    tp_buy_tax_total += tp_buy_tax
                    base_cost += (specific_elemental_lodestone[1] * ref_ings[ingredient]) #+ tp_buy_tax
        

        final_cost = base_cost + tp_buy_tax_total + station_fee_total
        
        value_pre_tax = price_dict[discipline][material] * output

        transaction_charge = value_pre_tax * (taxes_fees['trade_post']['tax'] / 100)
        listing_fee = determing_trade_post_sell_fee(value_pre_tax, taxes_fees)
        value_post_tax = value_pre_tax - listing_fee - transaction_charge
        
        profit_craft = (value_post_tax - final_cost)

        cost_each = final_cost / output
        profit_craft_each = profit_craft / output
        
        financial.append({
            'craft' : {
                'base_cost' : base_cost,
                'trade_post_tax' : tp_buy_tax_total,
                'station_tax' : station_fee_total,
                'final_cost': final_cost,
                'final_cost_each': cost_each,
            },
            'sell' : {
                'base_value' : value_pre_tax,
                'listing_fee' : listing_fee,
                'transaction_charge' : transaction_charge,
                'final_profit': profit_craft,
                'final_profit_each': profit_craft_each
            }
        })
    
    data = {
        'craft' : {
            'input' : number_of_crafts,
            'output': output,
            'bonus' : round(craft_bonus_dict[material],2),
            'final_value' : value_post_tax
        },
        'ingredients' : ingredients_list,
        'financial' : financial
    }
    
    return data, specific_elemental_lodestone


def determine_discipline(material):
    for key in conversions.keys():
        if material in conversions[key]:
            return key
        
    for key, value in conversions.items():
        for k in value.keys():
            if material in value[k]:
                return key
            
    for key in alchemy_conversions.keys():
        if f'_{key}' in material:
            return key
        
    return None


def worbench_tax(refine_tier, taxes):
    sub_total = 0
    if refine_tier == 1:
        sub_total =  taxes['refining_station']['tier_2']
    if refine_tier == 2:
        sub_total =  taxes['refining_station']['tier_3']
    if refine_tier == 3:
        sub_total =  taxes['refining_station']['tier_4']
    if refine_tier == 4:
        sub_total =  taxes['refining_station']['tier_5']
    if refine_tier == 5:
        sub_total =  taxes['refining_station']['tier_5_L']
    
    if taxes['territory']['company_owned'] == True:
        return sub_total * 0.7
    return sub_total


def determing_trade_post_sell_fee(value, taxes):
    company_owned = taxes['territory']['company_owned']
    company_discount = 1
    if company_owned == True:
        company_discount = 0.7
        
    weavers_fen = taxes['territory']['weavers_fen']
    weavers_discount = 1
    if weavers_fen == True:
        weavers_discount = 0.9
    
    duration_fees = {
        "1_Day": 0.4956,
        "3_Days": 0.9912,
        "7_Days": 1.9824,
        "14_Days": 3.9648,
    }
    per_value = {
        "1_Day": 1,
        "3_Days": 1.25,
        "7_Days": 1.5,
        "14_Days": 1.75,
    }
    duration = taxes['trade_post']['duration']
  
    base_fee = duration_fees[duration]
    tax_rate = taxes['trade_post']['tax'] / 100
    discount_rate = taxes['trade_post']['discount'] / 100
    
    list_fee = abs(base_fee * (1 + tax_rate - discount_rate))
    
    per_value_multiplier = per_value[duration]
    fee_per_value = (abs(tax_rate - discount_rate)/10) * per_value_multiplier
    total_value_fee = value * fee_per_value
    
    total_listing_fee = (list_fee + total_value_fee) * company_discount * weavers_discount

    return total_listing_fee


def apply_trade_post_tax_buy(cost, taxes):
    weavers_fen = taxes['territory']['weavers_fen']
    weavers_discount = 1
    if weavers_fen == True:
        weavers_discount = 0.9
        
    tax_rate = taxes['trade_post']['tax'] / 100
    discount_rate = 1 - taxes['trade_post']['discount'] / 100 
    
    sub_tax = tax_rate * cost
    final_tax = sub_tax * discount_rate * weavers_discount
    
    return final_tax


def final_market_buy_cost(cost, taxes):
    if cost == 0:
        return 0
    tax = apply_trade_post_tax_buy(cost, taxes)
    return cost + tax


def determine_break_even(purchase_price, purchase_quantity, taxes):
    base_purchase = purchase_price * purchase_quantity
    purchase_tax = apply_trade_post_tax_buy(base_purchase, taxes)
    final_purchase = base_purchase + purchase_tax
    
    company_owned = taxes['territory']['company_owned']
    company_discount = 1
    if company_owned == True:
        company_discount = 0.7
        
    weavers_fen = taxes['territory']['weavers_fen']
    weavers_discount = 1
    if weavers_fen == True:
        weavers_discount = 0.9
    
    duration_fees = {
        "1_Day": 0.4956,
        "3_Days": 0.9912,
        "7_Days": 1.9824,
        "14_Days": 3.9648,
    }
    per_value = {
        "1_Day": 1,
        "3_Days": 1.25,
        "7_Days": 1.5,
        "14_Days": 1.75,
    }
    duration = taxes['trade_post']['duration']
    sell_tax = taxes['trade_post']['tax'] / 100
    
    base_fee = duration_fees[duration]
    tax_rate = taxes['trade_post']['tax'] / 100
    discount_rate = taxes['trade_post']['discount'] / 100
    
    list_fee = abs(base_fee * (1 + tax_rate - discount_rate))
    
    per_value_multiplier = per_value[duration]
    fee_per_value = (abs(tax_rate - discount_rate)/10) * per_value_multiplier
    
    sell_price = final_purchase + list_fee
    break_even = -1
    while break_even < 0:
        if sell_price > final_purchase * 2:
            break
        sell_price += 0.01
        base_sell = sell_price
        
        total_value_fee = base_sell * fee_per_value
        total_listing_fee = (list_fee + total_value_fee) * company_discount * weavers_discount
        transaction_charge = base_sell * sell_tax
        
        final_sell = base_sell - total_listing_fee - transaction_charge
        
        break_even = final_sell - final_purchase
    
    data = {
        'break_even_one': sell_price,
        'break_even_quant': sell_price/purchase_quantity
    }
    
    return data
    

def init_refining_cost_table():
    _refining_dict = {}
    for discipline, discipline_data in conversions.items():
        _refining_dict[discipline] = {}
        for key in discipline_data.keys():
            if key != 'refining_component':
                _refining_dict[discipline][key] = {}
    
    
    for discipline, discipline_data in _refining_dict.items():
        for target_material in discipline_data.keys():
            _refining_dict[discipline][target_material][target_material] = 0

            # Init Secondary Ingredients
            ingred_1, ingred_2, ingred_3, ingred_4, ingred_5 = None, None, None, None, None
            
            ingred_1 = conversions[discipline][target_material]['primary']
            _refining_dict[discipline][target_material][ingred_1] = 0
            
            if ingred_1 in conversions[discipline]:
                ingred_2 = conversions[discipline][ingred_1]['primary']
                _refining_dict[discipline][target_material][ingred_2] = 0
                
                if ingred_2 in conversions[discipline]:
                    ingred_3 = conversions[discipline][ingred_2]['primary']
                    _refining_dict[discipline][target_material][ingred_3] = 0
                    
                    if ingred_3 in conversions[discipline]:
                        ingred_4 = conversions[discipline][ingred_3]['primary']
                        _refining_dict[discipline][target_material][ingred_4] = 0
                        
                        if ingred_4 in conversions[discipline]:
                            ingred_5 = conversions[discipline][ingred_4]['primary']
                            _refining_dict[discipline][target_material][ingred_5] = 0
    return _refining_dict


def refining_up_profitability_table(discipline, material, quantity, skill_level, gear_set, market, taxes):
    first_light_bonus = taxes['territory']['first_light']
    craft_bonus = total_craft_bonus(skill_level, gear_set, discipline, first_light_bonus)
    
    #determine material tier
    tier = -1
    
    refining_list = (list(conversions[discipline].keys()))
    refining_list.remove('refining_component')
    
    if material == conversions[discipline][refining_list[0]]['primary']:
        tier = 0
    else:
        for item in refining_list:
            if material == item:
                tier = conversions[discipline][item]['tier']
    
    if tier != 5:
        refining_list = [material] + refining_list[tier:]
        
        #init ref dict for items needed
        refining_dict = {}
        for item in refining_list:
            refining_dict[item] = {
                'craft' : {
                    'quantity': 0,
                    'base_cost': 0,
                    'trade_post_tax' : 0,
                    'station_tax' : 0,
                    'final_cost': 0
                    },
                'sell': {
                    'quantity': 0,
                    'base_value': 0,
                    'listing_fee' : 0,
                    'transaction_charge' : 0,
                    'final_profit': 0
                    }
            }
        refining_dict[material]['sell']['quantity'] = quantity
            
        #determine how many can be made for each tier
        for i in range(len(refining_list)-1):
            refine_ingredient = refining_list[i]
            target_refine = refining_list[i+1]
            
            quant_available = refining_dict[refine_ingredient]['sell']['quantity']
            quant_per_craft = conversions[discipline][target_refine][refine_ingredient]
            
            if quant_available >= quant_per_craft:
                bonus = craft_bonus[target_refine]
                number_of_crafts = math.floor(quant_available / quant_per_craft)
                output = math.floor(number_of_crafts * bonus)
                
                refining_dict[target_refine]['craft']['quantity'] = number_of_crafts
                refining_dict[target_refine]['sell']['quantity'] = output
            else:
                refining_dict[target_refine]['craft']['quantity'] = 0
                refining_dict[target_refine]['sell']['quantity'] = 0
            

        # determine craft cost for each tier
        base_cost = 0
        trade_post_tax = 0
        station_tax = 0 
        final_cost = 0
        for i in range(len(refining_list)-1):
            refine_ingredient = refining_list[i]
            target_refine = refining_list[i+1]
            
            quant_available = refining_dict[refine_ingredient]['sell']['quantity']
            quant_per_craft = conversions[discipline][target_refine][refine_ingredient]
            
            number_of_crafts = math.floor(quant_available / quant_per_craft)

            #station fees
            target_refine_tier = conversions[discipline][target_refine]['tier']
            station_tax += worbench_tax(target_refine_tier, taxes) * number_of_crafts
            
            #check for additional ingredients
            for key in conversions[discipline][target_refine].keys():
                if key != "tier" and key != "primary" and key != refine_ingredient:
                    if key != 'elemental_lodestone':
                        market_cost = market[discipline][key]
                    else:
                        ele_lode = elemental_lodestone_calcs(market[discipline])
                        market_cost = ele_lode[1]
                        
                    quant_per_craft = conversions[discipline][target_refine][key]
                    quant_required = number_of_crafts * quant_per_craft

                    quant_cost = quant_required * market_cost
                    purchase_tax = apply_trade_post_tax_buy(quant_cost, taxes)
                    
                    base_cost += quant_cost
                    trade_post_tax += purchase_tax
                
                    
            #refining components
            market_cost = market['refining_component'][conversions[discipline]['refining_component']]
            if target_refine_tier > 1:
                quant_cost = market_cost * number_of_crafts
                purchase_tax = apply_trade_post_tax_buy(quant_cost, taxes)
                
                base_cost += quant_cost
                trade_post_tax += purchase_tax
            
            
            final_cost = base_cost + trade_post_tax + station_tax
            
            refining_dict[target_refine]['craft']['quantity'] = number_of_crafts
            refining_dict[target_refine]['craft']['base_cost'] = base_cost
            refining_dict[target_refine]['craft']['trade_post_tax'] = trade_post_tax
            refining_dict[target_refine]['craft']['station_tax'] = station_tax
            refining_dict[target_refine]['craft']['final_cost'] = final_cost
        
        
        #determine sell value for each tier
        for _material, _material_data in refining_dict.items():
            market_value_each = market[discipline][_material]
            sell_quant = _material_data['sell']['quantity']
            base_market_value = market_value_each * sell_quant
            
            listing_fee = determing_trade_post_sell_fee(base_market_value, taxes)
            transaction_charge = base_market_value * (taxes['trade_post']['tax'] / 100)
            
            craft_cost = _material_data['craft']['final_cost']
            final_profit = base_market_value - listing_fee - transaction_charge - craft_cost

            if base_market_value > 0:
                refining_dict[_material]['sell']['base_value'] = base_market_value
                refining_dict[_material]['sell']['listing_fee'] = listing_fee
                refining_dict[_material]['sell']['transaction_charge'] = transaction_charge
                refining_dict[_material]['sell']['final_profit'] = final_profit
            else:
                refining_dict[_material]['sell']['base_value'] = 0
                refining_dict[_material]['sell']['listing_fee'] = 0
                refining_dict[_material]['sell']['transaction_charge'] = 0
                refining_dict[_material]['sell']['final_profit'] = 0
        
        return refining_dict
    return None


def determine_tier(material):
    discipline = determine_discipline(material)
    
    if discipline in conversions:
        if material in conversions[discipline]:
            return conversions[discipline][material]['tier']
        else:
            for key, value in conversions[discipline].items():
                if key != "refining_components":
                    if material in value:
                        return 0
        
    elif discipline in alchemy_conversions:
        return alchemy_conversions[discipline]['tier']
        
    return None


def determine_refining_route_given_material(discipline, target, quantity, material, skill_level, gear_set, price_list, taxes_fees):
    _data, _ = ingredients_needed_to_refine(discipline, target, quantity, skill_level, gear_set, price_list, taxes_fees)
    
    for i in range(len(_data['ingredients'])):
        check = _data['ingredients'][i]
        for ingredient in check.keys():
            if ingredient == material:
                if type(check[ingredient]) is int:
                    refine_cost = _data['financial'][i]['craft']['final_cost']
                    ingredients = {
                        'cost': round(refine_cost,2),
                        'ingredients': {}
                    }
                    for item, quant in check.items():
                        if type(quant) is int:
                            ingredients['ingredients'][item] = quant
                    return ingredients
    if target == material:
        final_price = final_market_buy_cost(price_list[discipline][target] * quantity, taxes_fees)
        ingredients = {
            'cost': round(final_price,2),
            'ingredients': {
                target: quantity
            }
            
        }
        return ingredients
    return None


def calculate_trophy_profitability(cheapest_route, price_list, taxes_fees, skill_level, gear_set):
    weavers_discount = taxes_fees['territory']['weavers_fen']
    weavers = 1
    if weavers_discount:
        weavers = 0.9
    total_discount = (taxes_fees['crafting']['station'] + taxes_fees['trade_post']['discount']) * weavers / 100
    
    station_fee = {
        'minor': 0.5 * total_discount,
        'basic': 7.48 * total_discount,
        'major': 7.48 * total_discount
    }

    mote_quantity = 25
    wood_quantity = 25
    metals_quantity = 20
    
    lumber_data = cheapest_route['woodworking']['lumber']
    lumber_source = determine_refining_route_given_material('woodworking', 'lumber', wood_quantity, lumber_data['source'], skill_level['woodworking'], gear_set['woodworking'], price_list, taxes_fees)
    
    steel_ingot_data = cheapest_route['smelting']['steel_ingot']
    steel_ingot_source = determine_refining_route_given_material('smelting', 'steel_ingot', metals_quantity, steel_ingot_data['source'], skill_level['smelting'], gear_set['smelting'], price_list, taxes_fees)
    
    wyrdwood_planks_data = cheapest_route['woodworking']['wyrdwood_planks']
    wyrdwood_planks_source = determine_refining_route_given_material('woodworking', 'wyrdwood_planks', wood_quantity, wyrdwood_planks_data['source'], skill_level['woodworking'], gear_set['woodworking'], price_list, taxes_fees)
    
    starmetal_ingot_data = cheapest_route['smelting']['starmetal_ingot']
    starmetal_ingot_source = determine_refining_route_given_material('smelting', 'starmetal_ingot', metals_quantity, starmetal_ingot_data['source'], skill_level['smelting'], gear_set['smelting'], price_list, taxes_fees)
    
    ironwood_planks_data = cheapest_route['woodworking']['ironwood_planks']
    ironwood_planks_source = determine_refining_route_given_material('woodworking', 'ironwood_planks', wood_quantity, ironwood_planks_data['source'], skill_level['woodworking'], gear_set['woodworking'], price_list, taxes_fees)
    
    orichalcum_ingot_data = cheapest_route['smelting']['orichalcum_ingot']
    orichalcum_ingot_source = determine_refining_route_given_material('smelting', 'orichalcum_ingot', metals_quantity, orichalcum_ingot_data['source'], skill_level['smelting'], gear_set['smelting'], price_list, taxes_fees)
    
    motes = {
        'arcana_crafting': {
            'item' : 'earth',
            'quantity': mote_quantity,
            'cost' : round(final_market_buy_cost(price_list['components']['earth_mote'] * mote_quantity, taxes_fees),2)
        },
        'weaponsmithing_crafting': {
            'item' : 'fire',
            'quantity': mote_quantity,
            'cost' : round(final_market_buy_cost(price_list['components']['fire_mote'] * mote_quantity, taxes_fees),2)
        },
        'cooking_crafting': {
            'item' : 'water',
            'quantity': mote_quantity,
            'cost' : round(final_market_buy_cost(price_list['components']['water_mote'] * mote_quantity, taxes_fees),2)
        },
        'engineering_crafting': {
            'item' : 'air',
            'quantity': mote_quantity,
            'cost' : round(final_market_buy_cost(price_list['components']['air_mote'] * mote_quantity, taxes_fees),2)
        },
        'armoring_crafting': {
            'item' : 'fire',
            'quantity': mote_quantity,
            'cost' : round(final_market_buy_cost(price_list['components']['fire_mote'] * mote_quantity, taxes_fees),2)
        },
        'ancients_combat': {
            'item' : 'soul',
            'quantity': mote_quantity,
            'cost' : round(final_market_buy_cost(price_list['components']['soul_mote'] * mote_quantity, taxes_fees),2)
        },
        'angry_earth_combat': {
            'item' : 'earth',
            'quantity': mote_quantity,
            'cost' : round(final_market_buy_cost(price_list['components']['earth_mote'] * mote_quantity, taxes_fees),2)
        },
        'wildlife_combat': {
            'item' : 'fire',
            'quantity': mote_quantity,
            'cost' : round(final_market_buy_cost(price_list['components']['fire_mote'] * mote_quantity, taxes_fees),2)
        },
        'corrupted_combat': {
            'item' : 'life',
            'quantity': mote_quantity,
            'cost' : round(final_market_buy_cost(price_list['components']['life_mote'] * mote_quantity, taxes_fees),2)
        },
        'lost_combat':  {
            'item' : 'death',
            'quantity': mote_quantity,
            'cost' : round(final_market_buy_cost(price_list['components']['death_mote'] * mote_quantity, taxes_fees),2)
        },
        'harvesting_gathering': {
            'item' : 'water',
            'quantity': mote_quantity,
            'cost' : round(final_market_buy_cost(price_list['components']['water_mote'] * mote_quantity, taxes_fees),2)
        },
        'logging_gathering': {
            'item' : 'air',
            'quantity': mote_quantity,
            'cost' : round(final_market_buy_cost(price_list['components']['air_mote'] * mote_quantity, taxes_fees),2)
        },
        'mining_gathering': {
            'item' : 'earth',
            'quantity': mote_quantity,
            'cost' : round(final_market_buy_cost(price_list['components']['earth_mote'] * mote_quantity, taxes_fees),2)
        },
        'skinning_gathering': {
            'item' : 'air',
            'quantity': mote_quantity,
            'cost' : round(final_market_buy_cost(price_list['components']['air_mote'] * mote_quantity, taxes_fees),2)
        },
        'fishing_gathering': {
            'item' : 'water',
            'quantity': mote_quantity,
            'cost' : round(final_market_buy_cost(price_list['components']['water_mote'] * mote_quantity, taxes_fees),2)
        }
    }
    
    base_ingredients = {
        'minor': {
            'lumber': {
                'quantity': wood_quantity,
                'method': lumber_data['source'],
                'ingredients': lumber_source['ingredients'],
                'cost': lumber_source['cost']
            },
            'steel_ingot': {
                'quantity': metals_quantity,
                'method': steel_ingot_data['source'],
                'ingredients': steel_ingot_source['ingredients'],
                'cost': steel_ingot_source['cost']
            },
            'stain': {
                'item': 'maple_stain',
                'quantity': 1,
                'cost': round(final_market_buy_cost(price_list['components']['maple_stain'], taxes_fees),2)
            },
            'component': {},
            'station_fee': {
                'cost': station_fee['minor']
            }
        },
        'basic': {
            'wyrdwood_planks': {
                'quantity': wood_quantity,
                'method': wyrdwood_planks_data['source'],
                'ingredients': wyrdwood_planks_source['ingredients'],
                'cost': wyrdwood_planks_source['cost']
            },
            'starmetal_ingot': {
                'quantity': metals_quantity,
                'method': starmetal_ingot_data['source'],
                'ingredients': starmetal_ingot_source['ingredients'],
                'cost': starmetal_ingot_source['cost']
            },
            'stain': {
                'item': 'oak_stain',
                'quantity': 1,
                'cost': round(final_market_buy_cost(price_list['components']['oak_stain'], taxes_fees),2)
            },
            'component': {
                'item': '',
                'quantity': 1,
                'cost': 0
            },
            'station_fee': {
                'cost': station_fee['basic']
            }
        },
        'major': {
            'ironwood_planks': {
                'quantity': wood_quantity,
                'method': ironwood_planks_data['source'],
                'ingredients': ironwood_planks_source['ingredients'],
                'cost': ironwood_planks_source['cost']
            },
            'orichalcum_ingot': {
                'quantity': metals_quantity,
                'method': orichalcum_ingot_data['source'],
                'ingredients': orichalcum_ingot_source['ingredients'],
                'cost': orichalcum_ingot_source['cost']
            },
            'stain': {
                'item': 'mahogany_stain',
                'quantity': 1,
                'cost': round(final_market_buy_cost(price_list['components']['mahogany_stain'], taxes_fees),2)
            },
            'component': {
                'item': '',
                'quantity': 1,
                'cost': 0
            },
            'station_fee': {
                'cost': station_fee['major']
            }
        }
    }
    
    trophy_dict = {}
    trophy_order = player_data.trade_post_trophy_order()
    for items in trophy_order:
        category = items[0]
        if category != "components":
            category_list = items[1:]
            trophy_dict[category] = {}
            for item in category_list:
                if item in ['minor', 'basic', 'major']:
                    trophy_dict[category][item] = {}
    
    
    for trophy in trophy_dict.keys():
        minor_price, basic_price, major_price = 0, 0, 0

        minor_ingr = base_ingredients['minor']
        # if trophy != "loot_luck":
        #     minor_price = motes[trophy]['cost']
        # else:
        if trophy == "loot_luck":
            for _t in trophy_order:
                if _t[0] == trophy:
                    component_ingr = _t[-3]

        if trophy != "loot_luck":
            minor_ingr['component'] = motes[trophy]
        else:
            minor_ingr['component']['item'] = component_ingr
            minor_ingr['component']['quantity'] = 1
            minor_ingr['component']['cost'] = round(final_market_buy_cost(price_list[trophy][component_ingr], taxes_fees),2)
        
        for _, tier_details in minor_ingr.items():
            minor_price += tier_details['cost']
        
        market_price = final_market_buy_cost(price_list[trophy][f'minor_{trophy}_trophy'], taxes_fees)
        final_minor_price = market_price + apply_trade_post_tax_buy(market_price, taxes_fees)
        sell_tax = determing_trade_post_sell_fee(market_price, taxes_fees)
        transaction_charge = sell_tax * (taxes_fees['trade_post']['tax'] / 100)
        sell_value = market_price - sell_tax - transaction_charge
        profit = sell_value - minor_price
        
        trophy_acquire_method = {
            'method': 'craft',
            'cost': round(minor_price,2)
        }
        if final_minor_price <= minor_price:
            trophy_acquire_method = {
            'method': 'buy',
            'cost': round(final_minor_price,2)
        }
            
        trophy_dict[trophy]['minor'] = {
            'craft_cost': round(minor_price,2),
            'sell_value': round(sell_value,2),
            'market_price': round(final_minor_price,2),
            'profit': round(profit,2),
            'detail': copy.deepcopy(minor_ingr),
            'trophy': trophy_acquire_method
        }

        basic_ingr = base_ingredients['basic']
        basic_price += minor_price
        for _t in trophy_order:
            if _t[0] == trophy:
                component_ingr = _t[-2]
        
        basic_ingr['component']['item'] = component_ingr
        basic_ingr['component']['cost'] = round(final_market_buy_cost(price_list[trophy][component_ingr], taxes_fees),2)
                
        for _, tier_details in basic_ingr.items():
            basic_price += tier_details['cost']
        
        market_price = final_market_buy_cost(price_list[trophy][f'basic_{trophy}_trophy'], taxes_fees)
        final_basic_price = market_price + apply_trade_post_tax_buy(market_price, taxes_fees)
        sell_tax = determing_trade_post_sell_fee(market_price, taxes_fees)
        transaction_charge = sell_tax * (taxes_fees['trade_post']['tax'] / 100)
        sell_value = market_price - sell_tax - transaction_charge
        profit = sell_value - basic_price
        
        sub_trophy_acquire = {
            'method': 'craft',
            'cost': round(minor_price,2)
        }
        if final_minor_price <= minor_price:
            sub_trophy_acquire = {
            'method': 'buy',
            'cost': round(final_minor_price,2)
        }
        trophy_acquire = {
            'method': 'craft',
            'cost': round(basic_price,2)
        }
        if final_basic_price <= basic_price:
            trophy_acquire = {
            'method': 'buy',
            'cost': round(final_basic_price,2)
        }
            
        trophy_dict[trophy]['basic'] = {
            'craft_cost' : round(basic_price,2),
            'sell_value': round(sell_value,2),
            'market_price': round(final_basic_price,2),
            'profit': round(profit,2),
            'detail': copy.deepcopy(basic_ingr),
            'sub_trophy': sub_trophy_acquire,
            'trophy': trophy_acquire
        }
        
        major_ingr = base_ingredients['major']
        major_price += basic_price
        for _t in trophy_order:
            if _t[0] == trophy:
                component_ingr = _t[-1]
                
        major_ingr['component']['item'] = component_ingr
        major_ingr['component']['cost'] = round(final_market_buy_cost(price_list[trophy][component_ingr], taxes_fees),2)
        
        for _, tier_details in major_ingr.items():
            major_price += tier_details['cost']
        
        market_price = final_market_buy_cost(price_list[trophy][f'major_{trophy}_trophy'], taxes_fees)
        final_major_price = market_price + apply_trade_post_tax_buy(market_price, taxes_fees)
        sell_tax = determing_trade_post_sell_fee(market_price, taxes_fees)
        transaction_charge = sell_tax * (taxes_fees['trade_post']['tax'] / 100)
        sell_value = market_price - sell_tax - transaction_charge
        profit = sell_value - major_price
        
        sub_trophy_acquire = {
            'method': 'craft',
            'cost': round(basic_price,2)
        }
        if final_basic_price <= basic_price:
            sub_trophy_acquire = {
            'method': 'buy',
            'cost': round(final_basic_price,2)
        }
        trophy_acquire = {
            'method': 'craft',
            'cost': round(major_price,2)
        }
        if final_major_price <= major_price:
            trophy_acquire = {
            'method': 'buy',
            'cost': round(final_major_price,2)
        }
            
        trophy_dict[trophy]['major'] = {
            'craft_cost' : round(major_price,2),
            'sell_value': round(sell_value,2),
            'market_price': round(final_major_price,2),
            'profit': round(profit,2),
            'detail': copy.deepcopy(major_ingr),
            'sub_trophy': sub_trophy_acquire,
            'trophy': trophy_acquire
        }

    return trophy_dict


def round_to_nearest_multiple(number, multiple):
    return multiple * math.ceil(number/multiple)


# keys in alchemy_station_tax represent ingredient used to make +1 tier. Mote -> Wisp tax = alchemy_station_tax[mote]
def alchemy_station_tax(material, taxes_fees):  
    discount = 1 - (taxes_fees['crafting']['station'] / 100)
    town_tax = 0.5
    alchemy_station_tax = {
        'mote': 0.15,
        'wisp': 0.37,
        'essence': 0.9
    }
    
    if material in alchemy_station_tax:
        return discount * alchemy_station_tax[material] * town_tax
    else:
        return 0


def materials_to_refine_alchemy(material, quantity, price_dict, taxes_fees, skill_level):
    skill_bonus = 1 + (int(skill_level) * 0.001)
    
    element = None
    category = None
    for key in alchemy_conversions.keys():
        if f'_{key}' in material:
            category = key
            element = material.replace(f'_{key}', '')
    
    essence_base = alchemy_conversions["quintessence"]["essence"]
    wisp_base = alchemy_conversions["essence"]["wisp"]
    mote_base = alchemy_conversions["wisp"]["mote"]
    
    number_of_crafts = 0
    if category == "quintessence":
        essence_quant = round_to_nearest_multiple((essence_base * quantity) / (skill_bonus), essence_base)
        wisp_quant = round_to_nearest_multiple((wisp_base * essence_quant) / (skill_bonus), wisp_base)
        mote_quant = round_to_nearest_multiple((mote_base * wisp_quant) / (skill_bonus), mote_base)
        
        ingredient_options = {
            "essence" : {
                "crafts": essence_quant / essence_base,
                "essence": essence_quant
            },
            "wisp" : {
                "crafts": wisp_quant / wisp_base,
                "wisp": wisp_quant
            },
            "mote" : {
                "crafts": mote_quant / mote_base,
                "mote": mote_quant
            }
        }
        number_of_crafts = essence_quant / essence_base
    elif category == "essence":
        wisp_quant = round_to_nearest_multiple((wisp_base * quantity) / (skill_bonus), wisp_base)
        mote_quant = round_to_nearest_multiple((mote_base * wisp_quant) / (skill_bonus), mote_base)
        ingredient_options = {
            "wisp" : {
                "crafts": wisp_quant / wisp_base,
                "wisp": wisp_quant
            },
            "mote" : {
                "crafts": mote_quant / mote_base,
                "mote": mote_quant
            }
        }
        number_of_crafts = wisp_quant / wisp_base
    elif category == "wisp":
        mote_quant = round_to_nearest_multiple((mote_base * quantity) / (skill_bonus), mote_base)
        ingredient_options = {
            "mote" : {
                "crafts": mote_quant / mote_base,
                "mote": mote_quant
            }
        }
        number_of_crafts = mote_quant / mote_base
    
    
    output = round(number_of_crafts * (skill_bonus))
    
    value_pre_tax = price_dict[category][material] * output
    transaction_charge = value_pre_tax * (taxes_fees['trade_post']['tax'] / 100)
    listing_fee = determing_trade_post_sell_fee(value_pre_tax, taxes_fees)
    value_post_tax = value_pre_tax - listing_fee - transaction_charge
    
    primary_ingredients = list(ingredient_options.keys())
    financial = []
    total_station_fee = 0
    for material in primary_ingredients:
        tp_buy_tax_total = 0
        base_cost = 0
        
        material_quant = ingredient_options[material][material]
        material_cost = price_dict[material][f'{element}_{material}']
        base_cost = material_quant * material_cost
        
        tp_buy_tax_total = apply_trade_post_tax_buy(base_cost, taxes_fees)
        
        craft_quant = ingredient_options[material]['crafts']
        material_station_fee = alchemy_station_tax(material, taxes_fees) * craft_quant
        total_station_fee += material_station_fee
        
        final_cost = base_cost + tp_buy_tax_total + total_station_fee
        cost_each = final_cost / output
        
        profit_craft = (value_post_tax - final_cost)
        profit_craft_each = profit_craft / output
        
        financial.append({
            'craft' : {
                'base_cost' : base_cost,
                'trade_post_tax' : tp_buy_tax_total,
                'station_tax' : total_station_fee,
                'final_cost': final_cost,
                'final_cost_each': cost_each,
            },
            'sell' : {
                'base_value' : value_pre_tax,
                'listing_fee' : listing_fee,
                'transaction_charge' : transaction_charge,
                'final_profit': profit_craft,
                'final_profit_each': profit_craft_each
            }
        })

    ingredients_list = []
    for material in primary_ingredients:
        if material == "mote":
            ingredients_list.append({
                material: ingredient_options[material][material],
                "wisp": "-",
                "essence": "-"
                
            })
        elif material == "wisp":
            ingredients_list.append({
                "mote": "-",
                material: ingredient_options[material][material],
                "essence": "-"
                
            })
        elif material == "essence":
            ingredients_list.append({
                "mote": "-",
                "wisp": "-",
                material: ingredient_options[material][material]
                
            })
    for material in primary_ingredients:
        for mat_dict in ingredients_list:
            target_tier = alchemy_conversions[category]['tier']
            for key in list(mat_dict.keys()):
                mat_tier =  alchemy_conversions[key]['tier']
                if mat_tier >= target_tier:
                    mat_dict.pop(key)

    ingredients_list.reverse()
    financial.reverse()
    
    data = {
        'craft' : {
            'input' : number_of_crafts,
            'output': output,
            'bonus' : round(skill_bonus,2),
            'final_value' : value_post_tax
        },
        'ingredients' : ingredients_list,
        'financial' : financial
    }

    return data
    

def alchemy_refining_up_profitability_table(material, quantity, skill_level, market, taxes_fees):
    craft_bonus = 1 + (int(skill_level) * 0.001)

    #determine material tier
    tier = -1
    
    refining_list = (list(alchemy_conversions.keys()))
    
    material_category = None
    for item in refining_list:
        if f'_{item}' in material:
            tier = alchemy_conversions[item]['tier']
            material_category = item
    
    if tier != 5:
        # Mote check
        if tier == 0:
            tier = 1
            
        refining_list = [material_category] + refining_list[tier:]
        #init ref dict for items needed
        refining_dict = {}
        for item in refining_list:
            refining_dict[item] = {
                'craft' : {
                    'quantity': 0,
                    'station_tax' : 0,
                    'final_cost': 0
                    },
                'sell': {
                    'quantity': 0,
                    'base_value': 0,
                    'listing_fee' : 0,
                    'transaction_charge' : 0,
                    'final_profit': 0
                    }
            }
        refining_dict[material_category]['sell']['quantity'] = quantity
        
        #determine how many can be made for each tier
        for i in range(len(refining_list)-1):
            refine_ingredient = refining_list[i]
            for key in alchemy_conversions.keys():
                if f'_{key}' in refine_ingredient:
                    refine_ingredient = key
                    
            target_refine = refining_list[i+1]
            for key in alchemy_conversions.keys():
                if f'_{key}' in target_refine:
                    target_refine = key
            
            quant_available = refining_dict[refine_ingredient]['sell']['quantity']
            quant_per_craft = alchemy_conversions[target_refine][refine_ingredient]
            
            if quant_available >= quant_per_craft:
                bonus = craft_bonus
                number_of_crafts = math.floor(quant_available / quant_per_craft)
                output = math.floor(number_of_crafts * bonus)
                
                refining_dict[target_refine]['craft']['quantity'] = number_of_crafts
                refining_dict[target_refine]['sell']['quantity'] = output
            else:
                refining_dict[target_refine]['craft']['quantity'] = 0
                refining_dict[target_refine]['sell']['quantity'] = 0
            
        # determine craft cost for each tier
        station_tax = 0 
        final_cost = 0
        for i in range(len(refining_list)-1):
            refine_ingredient = refining_list[i]
            target_refine = refining_list[i+1]
            
            refine_ingredient = refining_list[i]
            for key in alchemy_conversions.keys():
                if f'_{key}' in refine_ingredient:
                    refine_ingredient = key
                    
            target_refine = refining_list[i+1]
            for key in alchemy_conversions.keys():
                if f'_{key}' in target_refine:
                    target_refine = key
                    
            quant_available = refining_dict[refine_ingredient]['sell']['quantity']
            quant_per_craft = alchemy_conversions[target_refine][refine_ingredient]
            
            number_of_crafts = math.floor(quant_available / quant_per_craft)

            #station fees
            station_tax += alchemy_station_tax(refine_ingredient, taxes_fees) * number_of_crafts
            
            final_cost = station_tax
            
            refining_dict[target_refine]['craft']['quantity'] = number_of_crafts
            refining_dict[target_refine]['craft']['station_tax'] = station_tax
            refining_dict[target_refine]['craft']['final_cost'] = final_cost
        
        
        #determine sell value for each tier
        for _material, _material_data in refining_dict.items():
            category = None
            for key in alchemy_conversions.keys():
                if f'_{key}' in material:
                    category = key
            
            market_value_each = market[category][material]
            sell_quant = _material_data['sell']['quantity']
            base_market_value = market_value_each * sell_quant
            
            listing_fee = determing_trade_post_sell_fee(base_market_value, taxes_fees)
            transaction_charge = base_market_value * (taxes_fees['trade_post']['tax'] / 100)
            
            craft_cost = _material_data['craft']['final_cost']
            final_profit = base_market_value - listing_fee - transaction_charge - craft_cost

            if base_market_value > 0:
                refining_dict[_material]['sell']['base_value'] = base_market_value
                refining_dict[_material]['sell']['listing_fee'] = listing_fee
                refining_dict[_material]['sell']['transaction_charge'] = transaction_charge
                refining_dict[_material]['sell']['final_profit'] = final_profit
            else:
                refining_dict[_material]['sell']['base_value'] = 0
                refining_dict[_material]['sell']['listing_fee'] = 0
                refining_dict[_material]['sell']['transaction_charge'] = 0
                refining_dict[_material]['sell']['final_profit'] = 0
        
        return refining_dict
    return None


def init_alchemy_cost_table():
    alchemy_template = player_data.alchemy_order()
    alchemy_dict = {}
    for category in alchemy_template:
        if category[0] != 'mote':
            alchemy_dict[category[0]] = {}
            for item in category[1:]:
                alchemy_dict[category[0]][item] = {}
    
    for category, cat_data in alchemy_dict.items():
        for item in cat_data.keys():
            element = item.replace(f'_{category}','')
            if category == 'wisp':
                alchemy_dict[category][item] = {
                    f'{element}_wisp': 0,
                    f'{element}_mote': 0
                }
            elif category == 'essence':
                alchemy_dict[category][item] = {
                    f'{element}_essence': 0,
                    f'{element}_mote': 0,
                    f'{element}_wisp': 0
                }
            elif category == 'quintessence':
                alchemy_dict[category][item] = {
                    f'{element}_quintessence': 0,
                    f'{element}_mote': 0,
                    f'{element}_wisp': 0,
                    f'{element}_essence': 0
                }
    return alchemy_dict


def tp_cost_to_upgrade_all_alchemy(price_list, skill_level, taxes_fees):
    _refining_dict = init_alchemy_cost_table()
    _financials = init_alchemy_cost_table()

    for discipline, discipline_data in _refining_dict.items():
            
        for material, material_data in discipline_data.items():
            market_value = price_list[discipline][material]
            purchase_total = market_value + apply_trade_post_tax_buy(market_value, taxes_fees)
            
            _refining_dict[discipline][material][material] = purchase_total
            _financials[discipline][material][material] = {
                'sell_profit' : 0,
                'profit_margin' : 0
            }
            
            quantity = 1000
            _data = materials_to_refine_alchemy(material, quantity, price_list, taxes_fees, skill_level)
                    

            material_ingredient_list = list(material_data.keys())
            material_ingredient_list.remove(material)
            material_ingredient_list.reverse()

            for i in range(len(material_ingredient_list)):
                _financial = _data['financial'][i]
                _craft_cost = _financial['craft']['final_cost_each']
                _sell_profit = _financial['sell']['final_profit_each']
                _profit_margin = _sell_profit / _craft_cost
                
                _refining_dict[discipline][material][material_ingredient_list[i]] = _craft_cost
                _financials[discipline][material][material_ingredient_list[i]] = {
                    'sell_profit' : _sell_profit,
                    'profit_margin' : _profit_margin
                }
                    
    return _refining_dict, _financials


def generate_cheapest_route_alchemy_table(refining_dict_full, financials):
    refining_dict_cheapest = {}
    for discipline, discipline_data in refining_dict_full.items():
        refining_dict_cheapest[discipline] = {}
        for material, material_data in discipline_data.items():
            
            material_list = list(material_data.items())

            material_from_tp = material_list[0]
            craft_cost = [material_from_tp]
            for i in material_list:
                mat = i[0]
                cost = i[1]
                profit = financials[discipline][material][mat]['sell_profit']
                if profit >= 0.01:
                    craft_cost.append((mat, cost))
                
            _price_data = cost_comparison(craft_cost)
            tp_flip = financials[discipline][material][_price_data[0]]['sell_profit']
            tp_margin= financials[discipline][material][_price_data[0]]['profit_margin']

            refining_dict_cheapest[discipline][material] = {
                "source": _price_data[0],
                "price" : round(_price_data[1], 2),
                "tp_flip": round(tp_flip, 2),
                "tp_margin": round(tp_margin * 100, 2)
            }
            
    return refining_dict_cheapest