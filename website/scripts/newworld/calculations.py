#!/usr/bin/python3
import math



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

    return round((tp_cost- lowest_cost) / lowest_cost * 100, 2)


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
            for i in range(len(material_ingredient_list)-1):
                _financial = _data['financial'][i-1]
                _craft_cost = _financial['craft']['final_cost_each']
                _sell_profit = _financial['sell']['final_profit_each']
                _profit_margin = _sell_profit / _craft_cost
                _refining_dict[discipline][material][material_ingredient_list[i+1]] = _craft_cost
                _financials[discipline][material][material_ingredient_list[i+1]] = {
                    'sell_profit' : _sell_profit,
                    'profit_margin' : _profit_margin
                }
                    
    return _refining_dict, _financials


def cheapest_tp_cost_route_to_refine_each_tier(price_list, refining_dict_full, taxes_fees, financials):
    refining_dict_cheapest = {}
    for discipline, discipline_data in refining_dict_full.items():
        refining_dict_cheapest[discipline] = {}
        for material, material_data in discipline_data.items():
            
            _price_data = cost_comparison(list(material_data.items()))
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
            'bonus' : craft_bonus_dict[material],
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

            refining_dict[_material]['sell']['base_value'] = base_market_value
            refining_dict[_material]['sell']['listing_fee'] = listing_fee
            refining_dict[_material]['sell']['transaction_charge'] = transaction_charge
            refining_dict[_material]['sell']['final_profit'] = final_profit
        
        return refining_dict
    return None


def determine_tier(material):
    discipline = determine_discipline(material)
    if discipline:
        if material in conversions[discipline]:
            return conversions[discipline][material]['tier']
        else:
            for key, value in conversions[discipline].items():
                if key != "refining_components":
                    if material in value:
                        return 0
    return None