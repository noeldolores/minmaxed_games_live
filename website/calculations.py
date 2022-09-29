#!/usr/bin/python3
import numpy as np


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
    }
}


def cost_comparison(list_of_prices):
    cheapest_price = min(list_of_prices, key=lambda tup: tup[1])
    
    return cheapest_price


def gear_set_bonus(gear_set):
    count = sum(int(i) > 0 for i in gear_set.values())
    bonus = count * 0.02
    
    return bonus


def cheapest_route_leatherworking(price_list, skill_level, gear_set):
    prices = price_list['leatherworking']
    aged_tannin = price_list['refining_components']['aged_tannin']
    conv = conversions['leatherworking']
    
    skill_bonus = int(skill_level) * 0.001
    gear_bonus = gear_set_bonus(gear_set)
    craft_bonus = {
        "coarse_leather": 1 + skill_bonus + gear_bonus,
        "rugged_leather": 1 + 0.75 + max(skill_bonus - 0.02, 0) + gear_bonus,
        "layered_leather": 1 + 0.3 + max(skill_bonus - 0.1, 0) + gear_bonus,
        "infused_leather": 1 + 0.1 + max(skill_bonus - 0.17, 0) + gear_bonus,
        "runic_leather": 1 + gear_bonus
    }
    
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





