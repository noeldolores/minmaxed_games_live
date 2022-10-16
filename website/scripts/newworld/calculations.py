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


def total_craft_bonus(skill_level, gear_set, discipline):
    skill_bonus = int(skill_level) * 0.001
    gear_bonus = 0.02 * (sum(int(i) > 0 for i in gear_set.values()))

    tier_1 = 1 + skill_bonus + gear_bonus
    tier_2 = 1 + 0.75 + max(skill_bonus - 0.02, 0) + gear_bonus
    tier_3 = 1 + 0.25 + max(skill_bonus - 0.05, 0) + gear_bonus
    tier_4 = 1 + max(skill_bonus - 0.07, 0) + gear_bonus
    tier_5 = 1 + max(skill_bonus - 0.2, 0) + gear_bonus

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
            "gold_ingot": 1 + 0.5 + max(skill_bonus - 0.05, 0) + gear_bonus,
            "platinum_ingot": 1 + 0.25 + max(skill_bonus - 0.07, 0) + gear_bonus #check rate for plat ori
        }
    elif discipline == "smelting_precious":
        craft_bonus = {
            "silver_ingot": tier_1,
            "gold_ingot": 1 + 0.5 + max(skill_bonus - 0.05, 0) + gear_bonus,
            "platinum_ingot": 1 + 0.25 + max(skill_bonus - 0.07, 0) + gear_bonus, #check rate for plat ori
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


def tp_cost_to_refine_all_routes_all_tiers(price_list, skill_level, gear_set):
    refining_dict_full = {}
    for discipline, discipline_data in conversions.items():
        prices = price_list[discipline]
        component = price_list['refining_component'][discipline_data['refining_component']]
        conv = conversions[discipline]
        
        if discipline == "smelting_precious":
            skill = skill_level['smelting']
            gear = gear_set['smelting']
        else:
            skill = skill_level[discipline]
            gear = gear_set[discipline]

        craft_bonus = total_craft_bonus(skill, gear, discipline)
        
        # Init Discipline / Material
        refining_dict_full[discipline] = {}
        refining_steps = list(conv.keys())[1:]
        for material in refining_steps:
            refining_dict_full[discipline][material] = {}

        
        # Add Target from TP
        for material in refining_dict_full[discipline].keys():
            name = material.replace("_"," ").title()
            tp_price = prices[material]
            refining_dict_full[discipline][material][name] = tp_price

            # Add Primary Ingrediennt
            primary, primary_2, primary_3, primary_4, primary_5 = None, None, None, None, None
            primary = conv[material]['primary']
            primary_name = primary.replace("_"," ").title()
            
            # Pricing 
            quant_req = conv[material][primary]
            
            sub_primary = prices[primary] * quant_req
            sub_component = (conv[material]['tier'] > 1) * component
            #sub_extra_parts = sum([ (prices[key] * conv[material][key]) for key in conv[material].keys() if key!="tier" and key!="primary" and key!=primary])
            
            sub_extra_parts = 0
            for key in conv[material].keys():
                if key!="tier" and key!="primary" and key!=primary:
                    if key!="elemental_lodestone":
                        sub_extra_parts += ( prices[key] * conv[material][key] )
                    else:
                        ele_lode = elemental_lodestone_calcs(prices)
                        sub_extra_parts += ( ele_lode[1] * conv[material][key] )
            
            sub_total = sub_component + sub_extra_parts
            
            bonus = craft_bonus[material]

            refining_dict_full[discipline][material][primary_name] = ( sub_primary + sub_total) / bonus
            

            # Check if Primary Ingredients have primaries
            if primary in conv:
                primary_2 = conv[primary]['primary']
                primary_2_name = primary_2.replace("_"," ").title()

                sub_primary =  refining_dict_full[discipline][primary][primary_2_name] * quant_req
                    
                refining_dict_full[discipline][material][primary_2_name] = ( sub_primary + sub_total) / bonus
        
                if primary_2 in conv:
                    primary_3 = conv[primary_2]['primary']
                    primary_3_name = primary_3.replace("_"," ").title()

                    sub_primary =  refining_dict_full[discipline][primary][primary_3_name] * quant_req

                    refining_dict_full[discipline][material][primary_3_name] = ( sub_primary + sub_total) / bonus

                    if primary_3 in conv:
                        primary_4 = conv[primary_3]['primary']
                        primary_4_name = primary_4.replace("_"," ").title()
                        
                        sub_primary =  refining_dict_full[discipline][primary][primary_4_name] * quant_req

                        refining_dict_full[discipline][material][primary_4_name] = ( sub_primary + sub_total) / bonus

                        if primary_4 in conv:
                            primary_5 = conv[primary_4]['primary']
                            primary_5_name = primary_5.replace("_"," ").title()
                            
                            sub_primary =  refining_dict_full[discipline][primary][primary_5_name] * quant_req

                            refining_dict_full[discipline][material][primary_5_name] = ( sub_primary + sub_total) / bonus
                    
    return refining_dict_full


def cheapest_tp_cost_route_to_refine_each_tier(price_list, refining_dict_full):
    refining_dict_cheapest = {}
    for discipline, discipline_data in refining_dict_full.items():
        refining_dict_cheapest[discipline] = {}
        for material, material_data in discipline_data.items():
            _price_data = cost_comparison(list(material_data.items()))
            refining_dict_cheapest[discipline][material] = {
                "source": _price_data[0],
                "price" : round(_price_data[1], 2),
                "tp_flip": round(price_list[discipline][material] - _price_data[1], 2),
                "tp_margin": tp_margin(price_list[discipline][material], _price_data[1])
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


def ingredients_needed_to_refine(discipline, material, quantity, skill_level, gear_set, price_dict):
    # if discipline == "smelting" and material in ["silver_ingot", "gold_ingot", "platinum_ingot", "orichalcum_ingot_platinum"]:
    #     refine_conversions = conversions["smelting_precious"]
    # else:
    refine_conversions = conversions[discipline]
    tier = refine_conversions[material]['tier']

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
                                
                                craft_bonus = total_craft_bonus(skill_level, gear_set, discipline)[target_refine]
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
            craft_bonus = total_craft_bonus(skill_level, gear_set, discipline)[target_refine]

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
    craft_bonus_dict = total_craft_bonus(skill_level, gear_set, discipline)
    
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
        
    refine_costs = []
    for ref_ings in ingredients_list:
        cost = 0
        for ingredient in ref_ings.keys():
            if type(ref_ings[ingredient]) is int:
                if ingredient in price_dict[discipline]:
                    cost += (price_dict[discipline][ingredient] * ref_ings[ingredient])
                elif ingredient in price_dict['refining_component']:
                    cost += (price_dict['refining_component'][ingredient] * ref_ings[ingredient])
                elif ingredient == "elemental_lodestone":
                    cost += specific_elemental_lodestone[1] * ref_ings[ingredient]
        
        
        total_value = price_dict[discipline][material] * output
        profit_craft = (total_value - cost)

        cost_each = cost / output
        profit_craft_each = profit_craft / output

        refine_costs.append((cost, cost_each, profit_craft, profit_craft_each))

    return ingredients_list, refine_costs, number_of_crafts, total_value, output, craft_bonus_dict[material], specific_elemental_lodestone


def determine_discipline(material):
    for key in conversions.keys():
        if material in conversions[key]:
            return key
        
    for key, value in conversions.items():
        for k in value.keys():
            if material in value[k]:
                return key
    return None