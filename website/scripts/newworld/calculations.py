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
        "orichalcum_platinum_ingot" : {
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
            "infused_leather": 1 + max(skill_bonus - 0.07, 0) + gear_bonus,
            "runic_leather": 1 + + max(skill_bonus - 0.2, 0) + gear_bonus
        }
    elif discipline == "smelting":
        craft_bonus = {
            "iron_ingot": tier_1,
            "steel_ingot": tier_2,
            "starmetal_ingot": tier_3,
            "orichalcum_ingot": tier_4,
            "orichalcum_platinum_ingot": tier_4,
            "asmodeum": tier_5,
            "silver_ingot": tier_1,
            "gold_ingot": 1 + 0.5 + max(skill_bonus - 0.05, 0) + gear_bonus,
            "platinum_ingot": 1 + 0.25 + max(skill_bonus - 0.07, 0) + gear_bonus #check rate for plat ori
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

        

def cheapest_route_leatherworking(price_list, skill_level, gear_set):
    prices = price_list['leatherworking']
    aged_tannin = price_list['refining_components']['aged_tannin']
    conv = conversions['leatherworking']
    
    craft_bonus = total_craft_bonus(skill_level, gear_set, "leatherworking")
    
    coarse_leather_from_rawhide = ( prices['rawhide'] * conv['coarse_leather']['rawhide'] ) / craft_bonus['coarse_leather']
    rugged_leather_from_rawhide = ( (coarse_leather_from_rawhide * conv['rugged_leather']['coarse_leather']) + aged_tannin) / craft_bonus['rugged_leather']
    layered_leather_from_rawhide = ( (rugged_leather_from_rawhide * conv['layered_leather']['rugged_leather']) + (prices['thick_hide'] * conv['layered_leather']['thick_hide']) + aged_tannin) / craft_bonus['layered_leather']
    infused_leather_from_rawhide = ( (layered_leather_from_rawhide * conv['infused_leather']['layered_leather']) + (prices['iron_hide'] * conv['infused_leather']['iron_hide']) + aged_tannin) / craft_bonus['infused_leather']
    runic_leather_from_rawhide = ( (infused_leather_from_rawhide * conv['runic_leather']['infused_leather']) + (prices['smolderhide'] + prices['scarhide']) + aged_tannin) / craft_bonus['runic_leather']
    
    rugged_leather_from_coarse_leather = ( (prices['coarse_leather'] * conv['rugged_leather']['coarse_leather']) + aged_tannin) / craft_bonus['rugged_leather']
    layered_leather_from_coarse_leather = ( (rugged_leather_from_coarse_leather * conv['layered_leather']['rugged_leather']) + (prices['thick_hide'] * conv['layered_leather']['thick_hide']) + aged_tannin) / craft_bonus['layered_leather']
    infused_leather_from_coarse_leather = ( (layered_leather_from_coarse_leather * conv['infused_leather']['layered_leather']) + (prices['iron_hide'] * conv['infused_leather']['iron_hide']) + aged_tannin) / craft_bonus['infused_leather']
    runic_leather_from_coarse_leather = ( (infused_leather_from_coarse_leather * conv['runic_leather']['infused_leather']) + (prices['smolderhide'] + prices['scarhide']) + aged_tannin) / craft_bonus['runic_leather']
    
    layered_leather_from_rugged_leather = ( (prices['rugged_leather'] * conv['layered_leather']['rugged_leather']) + (prices['thick_hide'] * conv['layered_leather']['thick_hide']) + aged_tannin) / craft_bonus['layered_leather']
    infused_leather_from_rugged_leather = ( (layered_leather_from_rugged_leather * conv['infused_leather']['layered_leather']) + (prices['iron_hide'] * conv['infused_leather']['iron_hide']) + aged_tannin) / craft_bonus['infused_leather']
    runic_leather_from_rugged_leather = ( (infused_leather_from_rugged_leather * conv['runic_leather']['infused_leather']) + (prices['smolderhide'] + prices['scarhide']) + aged_tannin) / craft_bonus['runic_leather']
    
    infused_leather_from_layered_leather = ( (prices['layered_leather'] * conv['infused_leather']['layered_leather']) + (prices['iron_hide'] * conv['infused_leather']['iron_hide']) + aged_tannin) / craft_bonus['infused_leather']
    runic_leather_from_layered_leather = ( (infused_leather_from_layered_leather * conv['runic_leather']['infused_leather']) + (prices['smolderhide'] + prices['scarhide']) + aged_tannin) / craft_bonus['runic_leather']
    
    runic_leather_from_infused_leather = ( (prices['infused_leather'] * conv['runic_leather']['infused_leather']) + (prices['smolderhide'] + prices['scarhide']) + aged_tannin) / craft_bonus['runic_leather']
    
    coarse_leather = [
        ("Coarse Leather", prices['coarse_leather']),
        ("Rawhide", coarse_leather_from_rawhide)
    ]
    rugged_leather = [
        ("Rugged Leather", prices['rugged_leather']),
        ("Rawhide", rugged_leather_from_rawhide),
        ("Coarse Leather", rugged_leather_from_coarse_leather)
    ]
    layered_leather = [
        ("Layered Leather", prices['layered_leather']),
        ("Rawhide", layered_leather_from_rawhide),
        ("Coarse Leather", layered_leather_from_coarse_leather),
        ("Rugged Leather", layered_leather_from_rugged_leather)
    ]
    infused_leather = [
        ("Infused Leather", prices['infused_leather']),
        ("Rawhide", infused_leather_from_rawhide),
        ("Coarse Leather", infused_leather_from_coarse_leather),
        ("Rugged Leather", infused_leather_from_rugged_leather),
        ("Layered Leather", infused_leather_from_layered_leather)
    ]
    runic_leather = [
        ("Runic Leather", prices['runic_leather']),
        ("Rawhide", runic_leather_from_rawhide),
        ("Coarse Leather", runic_leather_from_coarse_leather),
        ("Rugged Leather", runic_leather_from_rugged_leather),
        ("Layered Leather", runic_leather_from_layered_leather),
        ("Infused Leather", runic_leather_from_infused_leather)
    ]
    
    coarse_leather_data = cost_comparison(coarse_leather)
    rugged_leather_data = cost_comparison(rugged_leather)
    layered_leather_data = cost_comparison(layered_leather)
    infused_leather_data = cost_comparison(infused_leather)
    runic_leather_data = cost_comparison(runic_leather)
    leatherworking = {
        "coarse_leather" : {
            "source": coarse_leather_data[0],
            "price" : round(coarse_leather_data[1], 2),
            "tp_flip": round(prices['coarse_leather'] - coarse_leather_data[1], 2),
            "tp_margin": tp_margin(prices['coarse_leather'], coarse_leather_data[1])
        },
        "rugged_leather": {
            "source": rugged_leather_data[0],
            "price" : round(rugged_leather_data[1], 2),
            "tp_flip": round(prices['rugged_leather'] - rugged_leather_data[1], 2),
            "tp_margin": tp_margin(prices['coarse_leather'], coarse_leather_data[1])
        },
        "layered_leather" : {
            "source": layered_leather_data[0],
            "price" : round(layered_leather_data[1], 2),
            "tp_flip": round(prices['layered_leather'] - layered_leather_data[1], 2),
            "tp_margin": tp_margin(prices['layered_leather'], layered_leather_data[1])
        },
        "infused_leather" : {
            "source": infused_leather_data[0],
            "price" : round(infused_leather_data[1], 2),
            "tp_flip": round(prices['infused_leather'] - infused_leather_data[1], 2),
            "tp_margin": tp_margin(prices['infused_leather'], infused_leather_data[1])
        },
        "runic_leather" : {
            "source": runic_leather_data[0],
            "price" : round(runic_leather_data[1], 2),
            "tp_flip": round(prices['runic_leather'] - runic_leather_data[1], 2),
            "tp_margin": tp_margin(prices['runic_leather'], runic_leather_data[1])
        }
    }
    
    return leatherworking


def cheapest_route_smelting(price_list, skill_level, gear_set):
    prices = price_list['smelting']
    obsidian_flux = price_list['refining_components']['obsidian_flux']
    charcoal = 2 * price_list['smelting']['charcoal']
    conv = conversions['smelting']
    
    craft_bonus = total_craft_bonus(skill_level, gear_set, "smelting")
    
    iron_ingot_from_iron_ore = ( prices['iron_ore'] * conv['iron_ingot']['iron_ore'] ) / craft_bonus['iron_ingot']
    steel_ingot_from_iron_ore = ( (iron_ingot_from_iron_ore * conv['steel_ingot']['iron_ingot']) + charcoal + obsidian_flux) / craft_bonus['steel_ingot']

    starmetal_ingot_from_iron_ore = ( (steel_ingot_from_iron_ore * conv['starmetal_ingot']['steel_ingot']) + (prices['starmetal_ore'] * conv['starmetal_ingot']['starmetal_ore']) + charcoal + obsidian_flux) / craft_bonus['starmetal_ingot']
    orichalcum_ingot_from_iron_ore = ( (starmetal_ingot_from_iron_ore * conv['orichalcum_ingot']['starmetal_ingot']) + (prices['orichalcum_ore'] * conv['orichalcum_ingot']['orichalcum_ore']) + charcoal + obsidian_flux) / craft_bonus['orichalcum_ingot']
    asmodeum_from_iron_ore = ( (orichalcum_ingot_from_iron_ore * conv['asmodeum']['orichalcum_ingot']) + (prices['cinnabar'] + prices['tolvium']) + charcoal + obsidian_flux) / craft_bonus['asmodeum']
    
    steel_ingot_from_iron_ingot = ( (prices['iron_ingot'] * conv['steel_ingot']['iron_ingot']) + charcoal + obsidian_flux) / craft_bonus['steel_ingot']
    starmetal_ingot_from_iron_ingot = ( (steel_ingot_from_iron_ingot * conv['starmetal_ingot']['steel_ingot']) + (prices['starmetal_ore'] * conv['starmetal_ingot']['starmetal_ore']) + charcoal + obsidian_flux) / craft_bonus['starmetal_ingot']
    orichalcum_ingot_from_iron_ingot = ( (starmetal_ingot_from_iron_ingot * conv['orichalcum_ingot']['starmetal_ingot']) + (prices['orichalcum_ore'] * conv['orichalcum_ingot']['orichalcum_ore']) + charcoal + obsidian_flux) / craft_bonus['orichalcum_ingot']
    asmodeum_from_iron_ingot = ( (orichalcum_ingot_from_iron_ingot * conv['asmodeum']['orichalcum_ingot']) + (prices['cinnabar'] + prices['tolvium']) + charcoal + obsidian_flux) / craft_bonus['asmodeum']
    
    starmetal_ingot_from_steel_ingot= ( (prices['steel_ingot'] * conv['starmetal_ingot']['steel_ingot']) + (prices['starmetal_ore'] * conv['starmetal_ingot']['starmetal_ore']) + charcoal + obsidian_flux) / craft_bonus['starmetal_ingot']
    orichalcum_ingot_from_steel_ingot = ( (starmetal_ingot_from_steel_ingot * conv['orichalcum_ingot']['starmetal_ingot']) + (prices['orichalcum_ore'] * conv['orichalcum_ingot']['orichalcum_ore']) + charcoal + obsidian_flux) / craft_bonus['orichalcum_ingot']
    asmodeum_from_steel_ingot = ( (orichalcum_ingot_from_steel_ingot * conv['asmodeum']['orichalcum_ingot']) + (prices['cinnabar'] + prices['tolvium']) + charcoal + obsidian_flux) / craft_bonus['asmodeum']
    
    orichalcum_ingot_from_starmetal_ingot = ( (prices['starmetal_ingot'] * conv['orichalcum_ingot']['starmetal_ingot']) + (prices['orichalcum_ore'] * conv['orichalcum_ingot']['orichalcum_ore']) + charcoal + obsidian_flux) / craft_bonus['orichalcum_ingot']
    asmodeum_from_starmetal_ingot = ( (orichalcum_ingot_from_starmetal_ingot * conv['asmodeum']['orichalcum_ingot']) + (prices['cinnabar'] + prices['tolvium']) + charcoal + obsidian_flux) / craft_bonus['asmodeum']
    
    asmodeum_from_orichalcum_ingot = ( (prices['orichalcum_ingot'] * conv['asmodeum']['orichalcum_ingot']) + (prices['cinnabar'] + prices['tolvium']) + charcoal + obsidian_flux) / craft_bonus['asmodeum']
    
    iron_ingot = [
        ("Iron Ingot", prices['iron_ingot']),
        ("Iron Ore", iron_ingot_from_iron_ore)
    ]
    steel_ingot = [
        ("Steel Ingot", prices['steel_ingot']),
        ("Iron Ore", steel_ingot_from_iron_ore),
        ("Iron Ingot", steel_ingot_from_iron_ingot)
    ]
    starmetal_ingot = [
        ("Starmetal Ingot", prices['starmetal_ingot']),
        ("Iron Ore", starmetal_ingot_from_iron_ore),
        ("Iron Ingot", starmetal_ingot_from_iron_ingot),
        ("Steel Ingot", starmetal_ingot_from_steel_ingot)
    ]
    orichalcum_ingot = [
        ("Orichalcum Ingot", prices['orichalcum_ingot']),
        ("Iron Ore", orichalcum_ingot_from_iron_ore),
        ("Iron Ingot", orichalcum_ingot_from_iron_ingot),
        ("Steel Ingot", orichalcum_ingot_from_steel_ingot),
        ("Starmetal Ingot", orichalcum_ingot_from_starmetal_ingot)
    ]
    asmodeum = [
        ("Asmodeum", prices['asmodeum']),
        ("Iron Ore", asmodeum_from_iron_ore),
        ("Iron Ingot", asmodeum_from_iron_ingot),
        ("Steel Ingot", asmodeum_from_steel_ingot),
        ("Starmetal Ingot", asmodeum_from_starmetal_ingot),
        ("Orichalcum Ingot", asmodeum_from_orichalcum_ingot)
    ]
    
    conv = conversions['smelting_precious']
    silver_ingot_from_silver_ore = ( prices['silver_ore'] * conv['silver_ingot']['silver_ore'] ) / craft_bonus['silver_ingot']
    gold_ingot_from_silver_ore = ( (silver_ingot_from_silver_ore * conv['gold_ingot']['silver_ingot']) + (prices['gold_ore'] * conv['gold_ingot']['gold_ore']) + obsidian_flux) / craft_bonus['gold_ingot']
    platinum_ingot_from_silver_ore = ( (gold_ingot_from_silver_ore * conv['platinum_ingot']['gold_ingot']) + (prices['platinum_ore'] * conv['platinum_ingot']['platinum_ore']) + obsidian_flux) / craft_bonus['platinum_ingot']
    orichalcum_ingot_platinum_from_silver_ore = ( (platinum_ingot_from_silver_ore * conv['orichalcum_platinum_ingot']['platinum_ingot']) + (prices['orichalcum_ore'] * conv['orichalcum_platinum_ingot']['orichalcum_ore']) + charcoal + obsidian_flux) / craft_bonus['orichalcum_ingot']
    
    gold_ingot_from_silver_ingot = ( (prices['silver_ingot'] * conv['gold_ingot']['silver_ingot']) + (prices['gold_ore'] * conv['gold_ingot']['gold_ore']) + obsidian_flux) / craft_bonus['gold_ingot']
    platinum_ingot_from_silver_ingot = ( (gold_ingot_from_silver_ingot * conv['platinum_ingot']['gold_ingot']) + (prices['platinum_ore'] * conv['platinum_ingot']['platinum_ore']) + obsidian_flux) / craft_bonus['platinum_ingot']
    orichalcum_ingot_platinum_from_silver_ingot = ( (platinum_ingot_from_silver_ingot * conv['orichalcum_platinum_ingot']['platinum_ingot']) + (prices['orichalcum_ore'] * conv['orichalcum_platinum_ingot']['orichalcum_ore']) + charcoal + obsidian_flux) / craft_bonus['orichalcum_ingot']
    
    platinum_ingot_from_gold_ingot= ( (prices['gold_ingot'] * conv['platinum_ingot']['gold_ingot']) + (prices['platinum_ore'] * conv['platinum_ingot']['platinum_ore']) + obsidian_flux) / craft_bonus['platinum_ingot']
    orichalcum_ingot_platinum_from_gold_ingot = ( (platinum_ingot_from_gold_ingot * conv['orichalcum_platinum_ingot']['platinum_ingot']) + (prices['orichalcum_ore'] * conv['orichalcum_platinum_ingot']['orichalcum_ore']) + charcoal + obsidian_flux) / craft_bonus['orichalcum_ingot']
    
    orichalcum_ingot_platinum_from_platinum_ingot = ( (prices['platinum_ingot'] * conv['orichalcum_platinum_ingot']['platinum_ingot']) + (prices['orichalcum_ore'] * conv['orichalcum_platinum_ingot']['orichalcum_ore']) + charcoal + obsidian_flux) / craft_bonus['orichalcum_ingot']
    
    silver_ingot = [
        ("Silver Ingot", prices['silver_ingot']),
        ("Silver Ore", silver_ingot_from_silver_ore)
    ]
    gold_ingot = [
        ("Gold Ingot", prices['gold_ingot']),
        ("Silver Ore", gold_ingot_from_silver_ore),
        ("Silver Ingot", gold_ingot_from_silver_ingot)
    ]
    platinum_ingot = [
        ("Platinum Ingot", prices['platinum_ingot']),
        ("Silver Ore", platinum_ingot_from_silver_ore),
        ("Silver Ingot", platinum_ingot_from_silver_ingot),
        ("Gold Ingot", platinum_ingot_from_gold_ingot)
    ]
    orichalcum_ingot_platinum = [
        ("Orichalcum Ingot", prices['orichalcum_ingot']),
        ("Silver Ore", orichalcum_ingot_platinum_from_silver_ore),
        ("Silver Ingot", orichalcum_ingot_platinum_from_silver_ingot),
        ("Gold Ingot", orichalcum_ingot_platinum_from_gold_ingot),
        ("Platinum Ingot", orichalcum_ingot_platinum_from_platinum_ingot)
    ]
    
    iron_ingot_data = cost_comparison(iron_ingot)
    steel_ingot_data = cost_comparison(steel_ingot)
    starmetal_ingot_data = cost_comparison(starmetal_ingot)
    orichalcum_ingot_data = cost_comparison(orichalcum_ingot)
    asmodeum_data = cost_comparison(asmodeum)
    silver_ingot_data = cost_comparison(silver_ingot)
    gold_ingot_data = cost_comparison(gold_ingot)
    platinum_ingot_data = cost_comparison(platinum_ingot)
    orichalcum_ingot_platinum_data = cost_comparison(orichalcum_ingot_platinum)
    smelting = {
        "iron_ingot" : {
            "source": iron_ingot_data[0],
            "price" : round(iron_ingot_data[1], 2),
            "tp_flip": round(prices['iron_ingot'] - iron_ingot_data[1], 2),
            "tp_margin": tp_margin(prices['iron_ingot'], iron_ingot_data[1])
        },
        "steel_ingot": {
            "source": steel_ingot_data[0],
            "price" : round(steel_ingot_data[1], 2),
            "tp_flip": round(prices['steel_ingot'] - steel_ingot_data[1], 2),
            "tp_margin": tp_margin(prices['steel_ingot'], steel_ingot_data[1])
        },
        "starmetal_ingot" : {
            "source": starmetal_ingot_data[0],
            "price" : round(starmetal_ingot_data[1], 2),
            "tp_flip": round(prices['starmetal_ingot'] - starmetal_ingot_data[1], 2),
            "tp_margin": tp_margin(prices['starmetal_ingot'], starmetal_ingot_data[1])
        },
        "orichalcum_ingot" : {
            "source": orichalcum_ingot_data[0],
            "price" : round(orichalcum_ingot_data[1], 2),
            "tp_flip": round(prices['orichalcum_ingot'] - orichalcum_ingot_data[1], 2),
            "tp_margin": tp_margin(prices['orichalcum_ingot'], orichalcum_ingot_data[1])
        },
        "asmodeum" : {
            "source": asmodeum_data[0],
            "price" : round(asmodeum_data[1], 2),
            "tp_flip": round(prices['asmodeum'] - asmodeum_data[1], 2),
            "tp_margin": tp_margin(prices['asmodeum'], asmodeum_data[1])
        },
        "silver_ingot" : {
            "source": silver_ingot_data[0],
            "price" : round(silver_ingot_data[1], 2),
            "tp_flip": round(prices['silver_ingot'] - silver_ingot_data[1], 2),
            "tp_margin": tp_margin(prices['silver_ingot'], silver_ingot_data[1])
        },
        "gold_ingot": {
            "source": gold_ingot_data[0],
            "price" : round(gold_ingot_data[1], 2),
            "tp_flip": round(prices['gold_ingot'] - gold_ingot_data[1], 2),
            "tp_margin": tp_margin(prices['gold_ingot'], gold_ingot_data[1])
        },
        "platinum_ingot" : {
            "source": platinum_ingot_data[0],
            "price" : round(platinum_ingot_data[1], 2),
            "tp_flip": round(prices['platinum_ingot'] - platinum_ingot_data[1], 2),
            "tp_margin": tp_margin(prices['platinum_ingot'], platinum_ingot_data[1])
        },
        "orichalcum_platinum_ingot" : {
            "source": orichalcum_ingot_platinum_data[0],
            "price" : round(orichalcum_ingot_platinum_data[1], 2),
            "tp_flip": round(prices['orichalcum_ingot'] - orichalcum_ingot_platinum_data[1], 2),
            "tp_margin": tp_margin(prices['orichalcum_ingot'], orichalcum_ingot_platinum_data[1])
        },
    }
    
    return smelting


def cheapest_route_stone_cutting(price_list, skill_level, gear_set):
    prices = price_list['stone_cutting']
    obsidian_sandpaper = price_list['refining_components']['obsidian_sandpaper']
    conv = conversions['stone_cutting']
    
    craft_bonus = total_craft_bonus(skill_level, gear_set, "stone_cutting")
    
    prices_elemental_lodestones = [
        ("Molten Lodestone", prices['molten_lodestone']),
        ("Loamy Lodestone", prices['loamy_lodestone']),
        ("Shocking Lodestone", prices['shocking_lodestone']),
        ("Crystalline Lodestone", prices['crystalline_lodestone']),
        ("Freezing Lodestone", prices['freezing_lodestone']),
        ("Putrid Lodestone", prices['putrid_lodestone'])
    ]
    elemental_lodestone = cost_comparison(prices_elemental_lodestones)
    
    stone_block_from_stone = ( prices['stone'] * conv['stone_block']['stone'] ) / craft_bonus['stone_block']
    stone_brick_from_stone = ( (stone_block_from_stone * conv['stone_brick']['stone_block']) + obsidian_sandpaper) / craft_bonus['stone_brick']
    lodestone_brick_from_stone = ( (stone_brick_from_stone * conv['lodestone_brick']['stone_brick']) + (prices['lodestone'] * conv['lodestone_brick']['lodestone']) + obsidian_sandpaper) / craft_bonus['lodestone_brick']
    obsidian_voidstone_from_stone = ( (lodestone_brick_from_stone * conv['obsidian_voidstone']['lodestone_brick']) + (prices['lodestone'] * conv['obsidian_voidstone']['lodestone']) + obsidian_sandpaper + elemental_lodestone[1]) / craft_bonus['obsidian_voidstone']
    runestone_from_stone = ( (obsidian_voidstone_from_stone * conv['runestone']['obsidian_voidstone']) + obsidian_sandpaper + elemental_lodestone[1]) / craft_bonus['runestone']
    
    stone_brick_from_stone_block = ( (prices['stone_block'] * conv['stone_brick']['stone_block']) + obsidian_sandpaper) / craft_bonus['stone_brick']
    lodestone_brick_from_stone_block = ( (stone_brick_from_stone_block * conv['lodestone_brick']['stone_brick']) + (prices['lodestone'] * conv['lodestone_brick']['lodestone']) + obsidian_sandpaper) / craft_bonus['lodestone_brick']
    obsidian_voidstone_from_stone_block = ( (lodestone_brick_from_stone_block * conv['obsidian_voidstone']['lodestone_brick']) + (prices['lodestone'] * conv['obsidian_voidstone']['lodestone']) + obsidian_sandpaper + elemental_lodestone[1]) / craft_bonus['obsidian_voidstone']
    runestone_from_stone_block = ( (obsidian_voidstone_from_stone_block * conv['runestone']['obsidian_voidstone']) + obsidian_sandpaper + elemental_lodestone[1]) / craft_bonus['runestone']
    
    lodestone_brick_from_stone_brick = ( (prices['stone_brick'] * conv['lodestone_brick']['stone_brick']) + (prices['lodestone'] * conv['lodestone_brick']['lodestone']) + obsidian_sandpaper) / craft_bonus['lodestone_brick']
    obsidian_voidstone_from_stone_brick = ( (lodestone_brick_from_stone_brick * conv['obsidian_voidstone']['lodestone_brick']) + (prices['lodestone'] * conv['obsidian_voidstone']['lodestone']) + obsidian_sandpaper + elemental_lodestone[1]) / craft_bonus['obsidian_voidstone']
    runestone_from_stone_brick = ( (obsidian_voidstone_from_stone_brick * conv['runestone']['obsidian_voidstone']) + obsidian_sandpaper + elemental_lodestone[1]) / craft_bonus['runestone']
    
    obsidian_voidstone_from_lodestone_brick = ( (prices['lodestone_brick'] * conv['obsidian_voidstone']['lodestone_brick']) + (prices['lodestone'] * conv['obsidian_voidstone']['lodestone']) + obsidian_sandpaper + elemental_lodestone[1]) / craft_bonus['obsidian_voidstone']
    runestone_from_lodestone_brick = ( (obsidian_voidstone_from_lodestone_brick * conv['runestone']['obsidian_voidstone']) + obsidian_sandpaper + elemental_lodestone[1]) / craft_bonus['runestone']
    
    runestone_from_obsidian_voidstone = ( (prices['obsidian_voidstone'] * conv['runestone']['obsidian_voidstone']) + obsidian_sandpaper + elemental_lodestone[1]) / craft_bonus['runestone']
    
    stone_block = [
        ("Stone Block", prices['stone_block']),
        ("Stone", stone_block_from_stone)
    ]
    stone_brick = [
        ("Stone Brick", prices['stone_brick']),
        ("Stone", stone_brick_from_stone),
        ("Stone Block", stone_brick_from_stone_block)
    ]
    lodestone_brick = [
        ("Lodestone Brick", prices['lodestone_brick']),
        ("Stone", lodestone_brick_from_stone),
        ("Stone Block", lodestone_brick_from_stone_block),
        ("Stone Brick", lodestone_brick_from_stone_brick)
    ]
    obsidian_voidstone = [
        ("Obsidian Voidstone", prices['obsidian_voidstone']),
        ("Stone", obsidian_voidstone_from_stone),
        ("Stone Block", obsidian_voidstone_from_stone_block),
        ("Stone Brick", obsidian_voidstone_from_stone_brick),
        ("Lodestone Brick", obsidian_voidstone_from_lodestone_brick)
    ]
    runestone = [
        ("Runestone", prices['runestone']),
        ("Stone", runestone_from_stone),
        ("Stone Block", runestone_from_stone_block),
        ("Stone Brick", runestone_from_stone_brick),
        ("Lodestone Brick", runestone_from_lodestone_brick),
        ("Obsidian Voidstone", runestone_from_obsidian_voidstone)
    ]
    
    
    stone_block_data = cost_comparison(stone_block)
    stone_brick_data = cost_comparison(stone_brick)
    lodestone_brick_data = cost_comparison(lodestone_brick)
    obsidian_voidstone_data = cost_comparison(obsidian_voidstone)
    runestone_data = cost_comparison(runestone)
    elemental_lodestone_data = elemental_lodestone
    stone_cutting = {
        "stone_block" : {
            "source": stone_block_data[0],
            "price" : round(stone_block_data[1], 2),
            "tp_flip": round(prices['stone_block'] - stone_block_data[1], 2),
            "tp_margin": tp_margin(prices['stone_block'], stone_block_data[1])
        },
        "stone_brick": {
            "source": stone_brick_data[0],
            "price" : round(stone_brick_data[1], 2),
            "tp_flip": round(prices['stone_brick'] - stone_brick_data[1], 2),
            "tp_margin": tp_margin(prices['stone_brick'], stone_brick_data[1])
        },
        "lodestone_brick" : {
            "source": lodestone_brick_data[0],
            "price" : round(lodestone_brick_data[1], 2),
            "tp_flip": round(prices['lodestone_brick'] - lodestone_brick_data[1], 2),
            "tp_margin": tp_margin(prices['lodestone_brick'], lodestone_brick_data[1])
        },
        "obsidian_voidstone" : {
            "source": obsidian_voidstone_data[0],
            "price" : round(obsidian_voidstone_data[1], 2),
            "tp_flip": round(prices['obsidian_voidstone'] - obsidian_voidstone_data[1], 2),
            "tp_margin": tp_margin(prices['obsidian_voidstone'], obsidian_voidstone_data[1])
        },
        "runestone" : {
            "source": runestone_data[0],
            "price" : round(runestone_data[1], 2),
            "tp_flip": round(prices['runestone'] - runestone_data[1], 2),
            "tp_margin": tp_margin(prices['runestone'], runestone_data[1])
        },
        "elemental_lodestone" : {
            "source": elemental_lodestone_data[0],
            "price" : round(elemental_lodestone_data[1], 2),
            "tp_flip": "-",
            "tp_margin": "-"
        }
    }
    
    return stone_cutting


def cheapest_route_weaving(price_list, skill_level, gear_set):
    prices = price_list['weaving']
    wireweave = price_list['refining_components']['wireweave']
    conv = conversions['weaving']
    
    craft_bonus = total_craft_bonus(skill_level, gear_set, "weaving")
    
    linen_from_fibers = ( prices['fibers'] * conv['linen']['fibers'] ) / craft_bonus['linen']
    sateen_from_fibers = ( (linen_from_fibers * conv['sateen']['linen']) + wireweave) / craft_bonus['sateen']
    silk_from_fibers = ( (sateen_from_fibers * conv['silk']['sateen']) + (prices['silk_threads'] * conv['silk']['silk_threads']) + wireweave) / craft_bonus['silk']
    infused_silk_from_fibers = ( (silk_from_fibers * conv['infused_silk']['silk']) + (prices['wirefiber'] * conv['infused_silk']['wirefiber']) + wireweave) / craft_bonus['infused_silk']
    phoenixweave_from_fibers = ( (infused_silk_from_fibers * conv['phoenixweave']['infused_silk']) + (prices['blisterweave'] + prices['scalecloth']) + wireweave) / craft_bonus['phoenixweave']
    
    sateen_from_linen = ( (prices['linen'] * conv['sateen']['linen']) + wireweave) / craft_bonus['sateen']
    silk_from_linen = ( (sateen_from_linen * conv['silk']['sateen']) + (prices['silk_threads'] * conv['silk']['silk_threads']) + wireweave) / craft_bonus['silk']
    infused_silk_from_linen = ( (silk_from_linen * conv['infused_silk']['silk']) + (prices['wirefiber'] * conv['infused_silk']['wirefiber']) + wireweave) / craft_bonus['infused_silk']
    phoenixweave_from_linen = ( (infused_silk_from_linen * conv['phoenixweave']['infused_silk']) + (prices['blisterweave'] + prices['scalecloth']) + wireweave) / craft_bonus['phoenixweave']
    
    silk_from_sateen = ( (prices['sateen'] * conv['silk']['sateen']) + (prices['silk_threads'] * conv['silk']['silk_threads']) + wireweave) / craft_bonus['silk']
    infused_silk_from_sateen = ( (silk_from_sateen * conv['infused_silk']['silk']) + (prices['wirefiber'] * conv['infused_silk']['wirefiber']) + wireweave) / craft_bonus['infused_silk']
    phoenixweave_from_sateen = ( (infused_silk_from_sateen * conv['phoenixweave']['infused_silk']) + (prices['blisterweave'] + prices['scalecloth']) + wireweave) / craft_bonus['phoenixweave']
    
    infused_silk_from_silk = ( (prices['silk'] * conv['infused_silk']['silk']) + (prices['wirefiber'] * conv['infused_silk']['wirefiber']) + wireweave) / craft_bonus['infused_silk']
    phoenixweave_from_silk = ( (infused_silk_from_silk * conv['phoenixweave']['infused_silk']) + (prices['blisterweave'] + prices['scalecloth']) + wireweave) / craft_bonus['phoenixweave']
    
    phoenixweave_from_infused_silk = ( (prices['infused_silk'] * conv['phoenixweave']['infused_silk']) + (prices['blisterweave'] + prices['scalecloth']) + wireweave) / craft_bonus['phoenixweave']
    
    linen = [
        ("Linen", prices['linen']),
        ("Fibers", linen_from_fibers)
    ]
    sateen = [
        ("Sateen", prices['sateen']),
        ("Fibers", sateen_from_fibers),
        ("Linen", sateen_from_linen)
    ]
    silk = [
        ("Silk", prices['silk']),
        ("Fibers", silk_from_fibers),
        ("Linen", silk_from_linen),
        ("Sateen", silk_from_sateen)
    ]
    infused_silk = [
        ("Infused Silk", prices['infused_silk']),
        ("Fibers", infused_silk_from_fibers),
        ("Linen", infused_silk_from_linen),
        ("Sateen", infused_silk_from_sateen),
        ("Silk", infused_silk_from_silk)
    ]
    phoenixweave = [
        ("Phoenixweave", prices['phoenixweave']),
        ("Fibers", phoenixweave_from_fibers),
        ("Linen", phoenixweave_from_linen),
        ("Sateen", phoenixweave_from_sateen),
        ("Silk", phoenixweave_from_silk),
        ("Infused Silk", phoenixweave_from_infused_silk)
    ]
    
    linen_data = cost_comparison(linen)
    sateen_data = cost_comparison(sateen)
    silk_data = cost_comparison(silk)
    infused_silk_data = cost_comparison(infused_silk)
    phoenixweave_data = cost_comparison(phoenixweave)
    weaving = {
        "linen" : {
            "source": linen_data[0],
            "price" : round(linen_data[1], 2),
            "tp_flip": round(prices['linen'] - linen_data[1], 2),
            "tp_margin": tp_margin(prices['linen'], linen_data[1])
        },
        "sateen": {
            "source": sateen_data[0],
            "price" : round(sateen_data[1], 2),
            "tp_flip": round(prices['sateen'] - sateen_data[1], 2),
            "tp_margin": tp_margin(prices['sateen'], sateen_data[1])
        },
        "silk" : {
            "source": silk_data[0],
            "price" : round(silk_data[1], 2),
            "tp_flip": round(prices['silk'] - silk_data[1], 2),
            "tp_margin": tp_margin(prices['silk'], silk_data[1])
        },
        "infused_silk" : {
            "source": infused_silk_data[0],
            "price" : round(infused_silk_data[1], 2),
            "tp_flip": round(prices['infused_silk'] - infused_silk_data[1], 2),
            "tp_margin": tp_margin(prices['infused_silk'], infused_silk_data[1])
        },
        "phoenixweave" : {
            "source": phoenixweave_data[0],
            "price" : round(phoenixweave_data[1], 2),
            "tp_flip": round(prices['phoenixweave'] - phoenixweave_data[1], 2),
            "tp_margin": tp_margin(prices['phoenixweave'], phoenixweave_data[1])
        }
    }
    
    return weaving

def cheapest_route_woodworking(price_list, skill_level, gear_set):
    prices = price_list['woodworking']
    obsidian_sandpaper = price_list['refining_components']['obsidian_sandpaper']
    conv = conversions['woodworking']
    
    craft_bonus = total_craft_bonus(skill_level, gear_set, "woodworking")
    
    timber_from_green_wood = ( prices['green_wood'] * conv['timber']['green_wood'] ) / craft_bonus['timber']
    lumber_from_green_wood = ( (timber_from_green_wood * conv['lumber']['timber']) + (prices['aged_wood'] * conv['lumber']['aged_wood']) + obsidian_sandpaper) / craft_bonus['lumber']
    wyrdwood_planks_from_green_wood = ( (lumber_from_green_wood * conv['wyrdwood_planks']['lumber']) + (prices['wyrdwood'] * conv['wyrdwood_planks']['wyrdwood']) + obsidian_sandpaper) / craft_bonus['wyrdwood_planks']
    ironwood_planks_from_green_wood = ( (wyrdwood_planks_from_green_wood * conv['ironwood_planks']['wyrdwood_planks']) + (prices['ironwood'] * conv['ironwood_planks']['ironwood']) + obsidian_sandpaper) / craft_bonus['ironwood_planks']
    glittering_ebony_from_green_wood = ( (ironwood_planks_from_green_wood * conv['glittering_ebony']['ironwood_planks']) + (prices['wildwood'] + prices['barbvine']) + obsidian_sandpaper) / craft_bonus['glittering_ebony']
    
    lumber_from_timber = ( (prices['timber'] * conv['lumber']['timber']) + (prices['aged_wood'] * conv['lumber']['aged_wood']) + obsidian_sandpaper) / craft_bonus['lumber']
    wyrdwood_planks_from_timber = ( (lumber_from_timber * conv['wyrdwood_planks']['lumber']) + (prices['wyrdwood'] * conv['wyrdwood_planks']['wyrdwood']) + obsidian_sandpaper) / craft_bonus['wyrdwood_planks']
    ironwood_planks_from_timber = ( (wyrdwood_planks_from_timber * conv['ironwood_planks']['wyrdwood_planks']) + (prices['ironwood'] * conv['ironwood_planks']['ironwood']) + obsidian_sandpaper) / craft_bonus['ironwood_planks']
    glittering_ebony_from_timber = ( (ironwood_planks_from_timber * conv['glittering_ebony']['ironwood_planks']) + (prices['wildwood'] + prices['barbvine']) + obsidian_sandpaper) / craft_bonus['glittering_ebony']
    
    wyrdwood_planks_from_lumber = ( (prices['lumber'] * conv['wyrdwood_planks']['lumber']) + (prices['wyrdwood'] * conv['wyrdwood_planks']['wyrdwood']) + obsidian_sandpaper) / craft_bonus['wyrdwood_planks']
    ironwood_planks_from_lumber = ( (wyrdwood_planks_from_lumber * conv['ironwood_planks']['wyrdwood_planks']) + (prices['ironwood'] * conv['ironwood_planks']['ironwood']) + obsidian_sandpaper) / craft_bonus['ironwood_planks']
    glittering_ebony_from_lumber = ( (ironwood_planks_from_lumber * conv['glittering_ebony']['ironwood_planks']) + (prices['wildwood'] + prices['barbvine']) + obsidian_sandpaper) / craft_bonus['glittering_ebony']
    
    ironwood_planks_from_wyrdwood_planks = ( (prices['wyrdwood_planks'] * conv['ironwood_planks']['wyrdwood_planks']) + (prices['ironwood'] * conv['ironwood_planks']['ironwood']) + obsidian_sandpaper) / craft_bonus['ironwood_planks']
    glittering_ebony_from_wyrdwood_planks = ( (ironwood_planks_from_wyrdwood_planks * conv['glittering_ebony']['ironwood_planks']) + (prices['wildwood'] + prices['barbvine']) + obsidian_sandpaper) / craft_bonus['glittering_ebony']
    
    glittering_ebony_from_ironwood_planks = ( (prices['ironwood_planks'] * conv['glittering_ebony']['ironwood_planks']) + (prices['wildwood'] + prices['barbvine']) + obsidian_sandpaper) / craft_bonus['glittering_ebony']
    
    timber = [
        ("Timber", prices['timber']),
        ("Green Wood", timber_from_green_wood)
    ]
    lumber = [
        ("Lumber", prices['lumber']),
        ("Green Wood", lumber_from_green_wood),
        ("Timber", lumber_from_timber)
    ]
    wyrdwood_planks = [
        ("Wyrdwood Planks", prices['wyrdwood_planks']),
        ("Green Wood", wyrdwood_planks_from_green_wood),
        ("Timber", wyrdwood_planks_from_timber),
        ("Lumber", wyrdwood_planks_from_lumber)
    ]
    ironwood_planks = [
        ("Ironwood Planks", prices['ironwood_planks']),
        ("Green Wood", ironwood_planks_from_green_wood),
        ("Timber", ironwood_planks_from_timber),
        ("Lumber", ironwood_planks_from_lumber),
        ("Wyrdwood Planks", ironwood_planks_from_wyrdwood_planks)
    ]
    glittering_ebony = [
        ("Glittering Ebony", prices['glittering_ebony']),
        ("Green Wood", glittering_ebony_from_green_wood),
        ("Timber", glittering_ebony_from_timber),
        ("Lumber", glittering_ebony_from_lumber),
        ("Wyrdwood Planks", glittering_ebony_from_wyrdwood_planks),
        ("Ironwood Planks", glittering_ebony_from_ironwood_planks)
    ]
    
    timber_data = cost_comparison(timber)
    lumber_data = cost_comparison(lumber)
    wyrdwood_planks_data = cost_comparison(wyrdwood_planks)
    ironwood_planks_data = cost_comparison(ironwood_planks)
    glittering_ebony_data = cost_comparison(glittering_ebony)
    woodworking = {
        "timber" : {
            "source": timber_data[0],
            "price" : round(timber_data[1], 2),
            "tp_flip": round(prices['timber'] - timber_data[1], 2),
            "tp_margin": tp_margin(prices['timber'], timber_data[1])
        },
        "lumber": {
            "source": lumber_data[0],
            "price" : round(lumber_data[1], 2),
            "tp_flip": round(prices['lumber'] - lumber_data[1], 2),
            "tp_margin": tp_margin(prices['lumber'], lumber_data[1])
        },
        "wyrdwood_planks" : {
            "source": wyrdwood_planks_data[0],
            "price" : round(wyrdwood_planks_data[1], 2),
            "tp_flip": round(prices['wyrdwood_planks'] - wyrdwood_planks_data[1], 2),
            "tp_margin": tp_margin(prices['wyrdwood_planks'], wyrdwood_planks_data[1])
        },
        "ironwood_planks" : {
            "source": ironwood_planks_data[0],
            "price" : round(ironwood_planks_data[1], 2),
            "tp_flip": round(prices['ironwood_planks'] - ironwood_planks_data[1], 2),
            "tp_margin": tp_margin(prices['ironwood_planks'], ironwood_planks_data[1])
        },
        "glittering_ebony" : {
            "source": glittering_ebony_data[0],
            "price" : round(glittering_ebony_data[1], 2),
            "tp_flip": round(prices['glittering_ebony'] - glittering_ebony_data[1], 2),
            "tp_margin": tp_margin(prices['glittering_ebony'], glittering_ebony_data[1])
        }
    }
    
    return woodworking


def ingredients_needed_to_refine(discipline, material, quantity, skill_level, gear_set):
    
    if discipline == "smelting" and material in ["silver_ingot", "gold_ingot", "platinum_ingot", "orichalcum_platinum_ingot"]:
        refine_conversions = conversions["smelting_precious"]
    else:
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
    
    for i in range(len(primary_ingredients)):
        if i == 0:  # Assign the secondary ingredient of the highest tier

            for key, value in refine_conversions[material].items():
                if key != "tier" and key != "primary" and key != primary_ingredients[i]:
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
                    secondary_quant_needed_per_refine = refine_conversions[target_refine][key]
                    ingredients[key] = int(ingredients[primary_ingredients[i]] / quant_needed_per_refine * secondary_quant_needed_per_refine)
                        
    test_refine = refining_component.copy()
          
    refining_component.insert(0, int(sum(refining_component)))
    refining_component_dict = {
        refine_conversions['refining_component']: refining_component
    }
    
    # Need to clean up, can probably combine with the original script
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
        ingredients_list[i][refine_conversions['refining_component']] = int(final_refine[i])
        current_tier = i + 1
        for key, value in ingredients.items():
            if key not in primary_ingredients:
                for k, v in refine_conversions.items():
                    if type(v) is dict:
                        if v['tier'] >= current_tier:
                            for kk in v.keys():
                                if kk != "primary" and kk != "tier" and kk not in primary_ingredients:
                                    if kk in ingredients:
                                        ingredients_list[i][kk] = ingredients[kk]
                                        if kk == "charcoal":
                                            ingredients_list[i][kk] = int(ingredients_list[i][refine_conversions['refining_component']] * 2)
                                    
    return ingredients, refining_component_dict, ingredients_list
    
    
def determine_discipline(material):    
    for key in conversions.keys():
        if material in conversions[key]:
            if key == "smelting_precious":
                return "smelting"
            return key
    return None