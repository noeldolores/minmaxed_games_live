#!/usr/bin/python3




conversions = {
    "leatherworking" : {
        "coarse_leather" : {
            "rawhide": 4
        },
        "rugged_leather": {
            "coarse_leather": 4
        },
        "layered_leather" : {
            "rugged_leather": 2,
            "thick_hide" : 6
        },
        "infused_leather" : {
            "layered_leather" : 2,
            "iron_hide" : 8
        },
        "runic_leather" : {
            "infused_leather" : 5,
            "smolderhide" : 1,
            "scarhide" : 1
        }
    },
    "smelting" : {
        "iron_ingot" : {
            "iron_ore": 4
        },
        "steel_ingot": {
            "iron_ingot": 3,
            "charcoal" : 2
        },
        "starmetal_ingot" : {
            "steel_ingot": 2,
            "starmetal_ore": 6,
            "charcoal" : 2
        },
        "orichalcum_ingot" : {
            "starmetal_ingot" : 2,
            "orichalcum_ore": 8,
            "platinum_ingot" : 3,
            "charcoal" : 2
        },
        "asmodeum" : {
            "orichalcum_ingot" : 5,
            "tolvium" : 1,
            "cinnabar" : 1,
            "charcoal" : 2
        },
        "silver_ingot" : {
            "silver_ore": 4
        },
        "gold_ingot": {
            "silver_ingot": 2,
            "gold_ore" : 5
        },
        "platinum_ingot" : {
            "gold_ingot": 2,
            "platinum_ore": 6
        }
    },
    "stone_cutting" : {
        "stone_block" : {
            "stone": 4
        },
        "stone_brick": {
            "stone_block": 4
        },
        "lodestone_brick" : {
            "stone_brick": 2,
            "lodestone" : 6
        },
        "obsidian_voidstone" : {
            "lodestone_brick" : 8,
            "lodestone" : 2,
            "elemental_lodestone" : 1
        },
        "runestone" : {
            "obsidian_voidstone" : 5,
            "elemental_lodestone" : 1
        }
    },
    "weaving" : {
        "linen" : {
            "fibers": 4
        },
        "sateen": {
            "linen": 4
        },
        "silk" : {
            "sateen": 2,
            "silk_threads" : 6
        },
        "infused_silk" : {
            "silk" : 2,
            "wirefiber" : 8
        },
        "phoenixweave" : {
            "infused_silk" : 5,
            "scalecloth" : 1,
            "blisterweave" : 1
        }
    },
    "woodworking" : {
        "timber" : {
            "green_wood": 4
        },
        "lumber": {
            "timber": 2,
            "aged_wood": 4
        },
        "wyrdwood_planks" : {
            "lumber": 2,
            "wyrdwood" : 6
        },
        "ironwood_planks" : {
            "wyrdwood_planks" : 2,
            "ironwood" : 8
        },
        "glittering_ebony" : {
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
    
    if discipline == "leatherworking":
        craft_bonus = {
            "coarse_leather": 1 + skill_bonus + gear_bonus,
            "rugged_leather": 1 + 0.75 + max(skill_bonus - 0.02, 0) + gear_bonus,
            "layered_leather": 1 + 0.3 + max(skill_bonus - 0.1, 0) + gear_bonus,
            "infused_leather": 1 + 0.1 + max(skill_bonus - 0.17, 0) + gear_bonus,
            "runic_leather": 1 + gear_bonus
        }
    elif discipline == "smelting":
        craft_bonus = {
            "iron_ingot": 1 + skill_bonus + gear_bonus,
            "steel_ingot": 1 + 0.75 + max(skill_bonus - 0.02, 0) + gear_bonus,
            "starmetal_ingot": 1 + 0.3 + max(skill_bonus - 0.1, 0) + gear_bonus,
            "orichalcum_ingot": 1 + 0.1 + max(skill_bonus - 0.17, 0) + gear_bonus,
            "asmodeum": 1 + gear_bonus,
            "silver_ingot": 1 + skill_bonus + gear_bonus,
            "gold_ingot": 1 + 0.55 + max(skill_bonus - 0.1, 0) + gear_bonus,
            "platinum_ingot": 1 + 0.35 + max(skill_bonus - 0.17, 0) + gear_bonus #check rate for plat ori
        }
    elif discipline == "stone_cutting":
        craft_bonus = {
            "stone_block": 1 + skill_bonus + gear_bonus,
            "stone_brick": 1 + 0.75 + max(skill_bonus - 0.02, 0) + gear_bonus,
            "lodestone_brick": 1 + 0.3 + max(skill_bonus - 0.1, 0) + gear_bonus,
            "obsidian_voidstone": 1 + 0.1 + max(skill_bonus - 0.17, 0) + gear_bonus,
            "runestone": 1 + gear_bonus
        }
    elif discipline == "weaving":
        craft_bonus = {
            "linen": 1 + skill_bonus + gear_bonus,
            "sateen": 1 + 0.75 + max(skill_bonus - 0.02, 0) + gear_bonus,
            "silk": 1 + 0.3 + max(skill_bonus - 0.1, 0) + gear_bonus,
            "infused_silk": 1 + 0.1 + max(skill_bonus - 0.17, 0) + gear_bonus,
            "phoenixweave": 1 + gear_bonus
        }
    elif discipline == "woodworking":
        craft_bonus = {
            "timber": 1 + skill_bonus + gear_bonus,
            "lumber": 1 + 0.75 + max(skill_bonus - 0.02, 0) + gear_bonus,
            "wyrdwood_planks": 1 + 0.3 + max(skill_bonus - 0.1, 0) + gear_bonus,
            "ironwood_planks": 1 + 0.1 + max(skill_bonus - 0.17, 0) + gear_bonus,
            "glittering_ebony": 1 + gear_bonus
        }
    else:
        craft_bonus = None
        
    return craft_bonus
        

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
        ("coarse_leather", prices['coarse_leather']),
        ("rawhide", coarse_leather_from_rawhide)
    ]
    rugged_leather = [
        ("rugged_leather", prices['rugged_leather']),
        ("rawhide", rugged_leather_from_rawhide),
        ("coarse_leather", rugged_leather_from_coarse_leather)
    ]
    layered_leather = [
        ("layered_leather", prices['layered_leather']),
        ("rawhide", layered_leather_from_rawhide),
        ("coarse_leather", layered_leather_from_coarse_leather),
        ("rugged_leather", layered_leather_from_rugged_leather)
    ]
    infused_leather = [
        ("infused_leather", prices['infused_leather']),
        ("rawhide", infused_leather_from_rawhide),
        ("coarse_leather", infused_leather_from_coarse_leather),
        ("rugged_leather", infused_leather_from_rugged_leather),
        ("layered_leather", infused_leather_from_layered_leather)
    ]
    runic_leather = [
        ("runic_leather", prices['runic_leather']),
        ("rawhide", runic_leather_from_rawhide),
        ("coarse_leather", runic_leather_from_coarse_leather),
        ("rugged_leather", runic_leather_from_rugged_leather),
        ("layered_leather", runic_leather_from_layered_leather),
        ("infused_leather", runic_leather_from_infused_leather)
    ]
    
    leatherworking = {
        "coarse_leather" : {
            "source": cost_comparison(coarse_leather)[0],
            "price" : round(cost_comparison(coarse_leather)[1], 2)
        },
        "rugged_leather": {
            "source": cost_comparison(rugged_leather)[0],
            "price" : round(cost_comparison(rugged_leather)[1], 2)
        },
        "layered_leather" : {
            "source": cost_comparison(layered_leather)[0],
            "price" : round(cost_comparison(layered_leather)[1], 2)
        },
        "infused_leather" : {
            "source": cost_comparison(infused_leather)[0],
            "price" : round(cost_comparison(infused_leather)[1], 2)
        },
        "runic_leather" : {
            "source": cost_comparison(runic_leather)[0],
            "price" : round(cost_comparison(runic_leather)[1], 2)
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
        ("iron_ingot", prices['iron_ingot']),
        ("iron_ore", iron_ingot_from_iron_ore)
    ]
    steel_ingot = [
        ("steel_ingot", prices['steel_ingot']),
        ("iron_ore", steel_ingot_from_iron_ore),
        ("iron_ingot", steel_ingot_from_iron_ingot)
    ]
    starmetal_ingot = [
        ("starmetal_ingot", prices['starmetal_ingot']),
        ("iron_ore", starmetal_ingot_from_iron_ore),
        ("iron_ingot", starmetal_ingot_from_iron_ingot),
        ("steel_ingot", starmetal_ingot_from_steel_ingot)
    ]
    orichalcum_ingot = [
        ("orichalcum_ingot", prices['orichalcum_ingot']),
        ("iron_ore", orichalcum_ingot_from_iron_ore),
        ("iron_ingot", orichalcum_ingot_from_iron_ingot),
        ("steel_ingot", orichalcum_ingot_from_steel_ingot),
        ("starmetal_ingot", orichalcum_ingot_from_starmetal_ingot)
    ]
    asmodeum = [
        ("asmodeum", prices['asmodeum']),
        ("iron_ore", asmodeum_from_iron_ore),
        ("iron_ingot", asmodeum_from_iron_ingot),
        ("steel_ingot", asmodeum_from_steel_ingot),
        ("starmetal_ingot", asmodeum_from_starmetal_ingot),
        ("orichalcum_ingot", asmodeum_from_orichalcum_ingot)
    ]
    
    silver_ingot_from_silver_ore = ( prices['silver_ore'] * conv['silver_ingot']['silver_ore'] ) / craft_bonus['silver_ingot']
    gold_ingot_from_silver_ore = ( (silver_ingot_from_silver_ore * conv['gold_ingot']['silver_ingot']) + (prices['gold_ore'] * conv['gold_ingot']['gold_ore']) + obsidian_flux) / craft_bonus['gold_ingot']
    platinum_ingot_from_silver_ore = ( (gold_ingot_from_silver_ore * conv['platinum_ingot']['gold_ingot']) + (prices['platinum_ore'] * conv['platinum_ingot']['platinum_ore']) + obsidian_flux) / craft_bonus['platinum_ingot']
    orichalcum_ingot_platinum_from_silver_ore = ( (platinum_ingot_from_silver_ore * conv['orichalcum_ingot']['platinum_ingot']) + (prices['orichalcum_ore'] * conv['orichalcum_ingot']['orichalcum_ore']) + charcoal + obsidian_flux) / craft_bonus['orichalcum_ingot']
    
    gold_ingot_from_silver_ingot = ( (prices['silver_ingot'] * conv['gold_ingot']['silver_ingot']) + (prices['gold_ore'] * conv['gold_ingot']['gold_ore']) + obsidian_flux) / craft_bonus['gold_ingot']
    platinum_ingot_from_silver_ingot = ( (gold_ingot_from_silver_ingot * conv['platinum_ingot']['gold_ingot']) + (prices['platinum_ore'] * conv['platinum_ingot']['platinum_ore']) + obsidian_flux) / craft_bonus['platinum_ingot']
    orichalcum_ingot_platinum_from_silver_ingot = ( (platinum_ingot_from_silver_ingot * conv['orichalcum_ingot']['platinum_ingot']) + (prices['orichalcum_ore'] * conv['orichalcum_ingot']['orichalcum_ore']) + charcoal + obsidian_flux) / craft_bonus['orichalcum_ingot']
    
    platinum_ingot_from_gold_ingot= ( (prices['gold_ingot'] * conv['platinum_ingot']['gold_ingot']) + (prices['platinum_ore'] * conv['platinum_ingot']['platinum_ore']) + obsidian_flux) / craft_bonus['platinum_ingot']
    orichalcum_ingot_platinum_from_gold_ingot = ( (platinum_ingot_from_gold_ingot * conv['orichalcum_ingot']['platinum_ingot']) + (prices['orichalcum_ore'] * conv['orichalcum_ingot']['orichalcum_ore']) + charcoal + obsidian_flux) / craft_bonus['orichalcum_ingot']
    
    orichalcum_ingot_platinum_from_platinum_ingot = ( (prices['platinum_ingot'] * conv['orichalcum_ingot']['platinum_ingot']) + (prices['orichalcum_ore'] * conv['orichalcum_ingot']['orichalcum_ore']) + charcoal + obsidian_flux) / craft_bonus['orichalcum_ingot']
    
    silver_ingot = [
        ("silver_ingot", prices['silver_ingot']),
        ("silver_ore", silver_ingot_from_silver_ore)
    ]
    gold_ingot = [
        ("gold_ingot", prices['gold_ingot']),
        ("silver_ore", gold_ingot_from_silver_ore),
        ("silver_ingot", gold_ingot_from_silver_ingot)
    ]
    platinum_ingot = [
        ("platinum_ingot", prices['platinum_ingot']),
        ("silver_ore", platinum_ingot_from_silver_ore),
        ("silver_ingot", platinum_ingot_from_silver_ingot),
        ("gold_ingot", platinum_ingot_from_gold_ingot)
    ]
    orichalcum_ingot_platinum = [
        ("orichalcum_ingot", prices['orichalcum_ingot']),
        ("silver_ore", orichalcum_ingot_platinum_from_silver_ore),
        ("silver_ingot", orichalcum_ingot_platinum_from_silver_ingot),
        ("gold_ingot", orichalcum_ingot_platinum_from_gold_ingot),
        ("platinum_ingot", orichalcum_ingot_platinum_from_platinum_ingot)
    ]
    
    smelting = {
        "iron_ingot" : {
            "source": cost_comparison(iron_ingot)[0],
            "price" : round(cost_comparison(iron_ingot)[1], 2)
        },
        "steel_ingot": {
            "source": cost_comparison(steel_ingot)[0],
            "price" : round(cost_comparison(steel_ingot)[1], 2)
        },
        "starmetal_ingot" : {
            "source": cost_comparison(starmetal_ingot)[0],
            "price" : round(cost_comparison(starmetal_ingot)[1], 2)
        },
        "orichalcum_ingot" : {
            "source": cost_comparison(orichalcum_ingot)[0],
            "price" : round(cost_comparison(orichalcum_ingot)[1], 2)
        },
        "asmodeum" : {
            "source": cost_comparison(asmodeum)[0],
            "price" : round(cost_comparison(asmodeum)[1], 2)
        },
        "silver_ingot" : {
            "source": cost_comparison(silver_ingot)[0],
            "price" : round(cost_comparison(silver_ingot)[1], 2)
        },
        "gold_ingot": {
            "source": cost_comparison(gold_ingot)[0],
            "price" : round(cost_comparison(gold_ingot)[1], 2)
        },
        "platinum_ingot" : {
            "source": cost_comparison(platinum_ingot)[0],
            "price" : round(cost_comparison(platinum_ingot)[1], 2)
        },
        "orichalcum_ingot_platinum" : {
            "source": cost_comparison(orichalcum_ingot_platinum)[0],
            "price" : round(cost_comparison(orichalcum_ingot_platinum)[1], 2)
        },
    }
    
    return smelting


def cheapest_route_stone_cutting(price_list, skill_level, gear_set):
    prices = price_list['stone_cutting']
    obsidian_sandpaper = price_list['refining_components']['obsidian_sandpaper']
    conv = conversions['stone_cutting']
    
    craft_bonus = total_craft_bonus(skill_level, gear_set, "stone_cutting")
    
    prices_elemental_lodestones = [
        ("molten_lodestone", prices['molten_lodestone']),
        ("loamy_lodestone", prices['loamy_lodestone']),
        ("shocking_lodestone", prices['shocking_lodestone']),
        ("crystalline_lodestone", prices['crystalline_lodestone']),
        ("freezing_lodestone", prices['freezing_lodestone']),
        ("putrid_lodestone", prices['putrid_lodestone'])
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
        ("stone_block", prices['stone_block']),
        ("stone", stone_block_from_stone)
    ]
    stone_brick = [
        ("stone_brick", prices['stone_brick']),
        ("stone", stone_brick_from_stone),
        ("stone_block", stone_brick_from_stone_block)
    ]
    lodestone_brick = [
        ("lodestone_brick", prices['lodestone_brick']),
        ("stone", lodestone_brick_from_stone),
        ("stone_block", lodestone_brick_from_stone_block),
        ("stone_brick", lodestone_brick_from_stone_brick)
    ]
    obsidian_voidstone = [
        ("obsidian_voidstone", prices['obsidian_voidstone']),
        ("stone", obsidian_voidstone_from_stone),
        ("stone_block", obsidian_voidstone_from_stone_block),
        ("stone_brick", obsidian_voidstone_from_stone_brick),
        ("lodestone_brick", obsidian_voidstone_from_lodestone_brick)
    ]
    runestone = [
        ("runestone", prices['runestone']),
        ("stone", runestone_from_stone),
        ("stone_block", runestone_from_stone_block),
        ("stone_brick", runestone_from_stone_brick),
        ("lodestone_brick", runestone_from_lodestone_brick),
        ("obsidian_voidstone", runestone_from_obsidian_voidstone)
    ]
    
    stone_cutting = {
        "stone_block" : {
            "source": cost_comparison(stone_block)[0],
            "price" : round(cost_comparison(stone_block)[1], 2)
        },
        "stone_brick": {
            "source": cost_comparison(stone_brick)[0],
            "price" : round(cost_comparison(stone_brick)[1], 2)
        },
        "lodestone_brick" : {
            "source": cost_comparison(lodestone_brick)[0],
            "price" : round(cost_comparison(lodestone_brick)[1], 2)
        },
        "obsidian_voidstone" : {
            "source": cost_comparison(obsidian_voidstone)[0],
            "price" : round(cost_comparison(obsidian_voidstone)[1], 2)
        },
        "runestone" : {
            "source": cost_comparison(runestone)[0],
            "price" : round(cost_comparison(runestone)[1], 2)
        },
        "elemental_lodestone" : {
            "source": elemental_lodestone[0],
            "price" : round(elemental_lodestone[1], 2)
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
        ("linen", prices['linen']),
        ("fibers", linen_from_fibers)
    ]
    sateen = [
        ("sateen", prices['sateen']),
        ("fibers", sateen_from_fibers),
        ("linen", sateen_from_linen)
    ]
    silk = [
        ("silk", prices['silk']),
        ("fibers", silk_from_fibers),
        ("linen", silk_from_linen),
        ("sateen", silk_from_sateen)
    ]
    infused_silk = [
        ("infused_silk", prices['infused_silk']),
        ("fibers", infused_silk_from_fibers),
        ("linen", infused_silk_from_linen),
        ("sateen", infused_silk_from_sateen),
        ("silk", infused_silk_from_silk)
    ]
    phoenixweave = [
        ("phoenixweave", prices['phoenixweave']),
        ("fibers", phoenixweave_from_fibers),
        ("linen", phoenixweave_from_linen),
        ("sateen", phoenixweave_from_sateen),
        ("silk", phoenixweave_from_silk),
        ("infused_silk", phoenixweave_from_infused_silk)
    ]
    
    weaving = {
        "linen" : {
            "source": cost_comparison(linen)[0],
            "price" : round(cost_comparison(linen)[1], 2)
        },
        "sateen": {
            "source": cost_comparison(sateen)[0],
            "price" : round(cost_comparison(sateen)[1], 2)
        },
        "silk" : {
            "source": cost_comparison(silk)[0],
            "price" : round(cost_comparison(silk)[1], 2)
        },
        "infused_silk" : {
            "source": cost_comparison(infused_silk)[0],
            "price" : round(cost_comparison(infused_silk)[1], 2)
        },
        "phoenixweave" : {
            "source": cost_comparison(phoenixweave)[0],
            "price" : round(cost_comparison(phoenixweave)[1], 2)
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
        ("timber", prices['timber']),
        ("green_wood", timber_from_green_wood)
    ]
    lumber = [
        ("lumber", prices['lumber']),
        ("green_wood", lumber_from_green_wood),
        ("timber", lumber_from_timber)
    ]
    wyrdwood_planks = [
        ("wyrdwood_planks", prices['wyrdwood_planks']),
        ("green_wood", wyrdwood_planks_from_green_wood),
        ("timber", wyrdwood_planks_from_timber),
        ("lumber", wyrdwood_planks_from_lumber)
    ]
    ironwood_planks = [
        ("ironwood_planks", prices['ironwood_planks']),
        ("green_wood", ironwood_planks_from_green_wood),
        ("timber", ironwood_planks_from_timber),
        ("lumber", ironwood_planks_from_lumber),
        ("wyrdwood_planks", ironwood_planks_from_wyrdwood_planks)
    ]
    glittering_ebony = [
        ("glittering_ebony", prices['glittering_ebony']),
        ("green_wood", glittering_ebony_from_green_wood),
        ("timber", glittering_ebony_from_timber),
        ("lumber", glittering_ebony_from_lumber),
        ("wyrdwood_planks", glittering_ebony_from_wyrdwood_planks),
        ("ironwood_planks", glittering_ebony_from_ironwood_planks)
    ]
    
    woodworking = {
        "timber" : {
            "source": cost_comparison(timber)[0],
            "price" : round(cost_comparison(timber)[1], 2)
        },
        "lumber": {
            "source": cost_comparison(lumber)[0],
            "price" : round(cost_comparison(lumber)[1], 2)
        },
        "wyrdwood_planks" : {
            "source": cost_comparison(wyrdwood_planks)[0],
            "price" : round(cost_comparison(wyrdwood_planks)[1], 2)
        },
        "ironwood_planks" : {
            "source": cost_comparison(ironwood_planks)[0],
            "price" : round(cost_comparison(ironwood_planks)[1], 2)
        },
        "glittering_ebony" : {
            "source": cost_comparison(glittering_ebony)[0],
            "price" : round(cost_comparison(glittering_ebony)[1], 2)
        }
    }
    
    return woodworking