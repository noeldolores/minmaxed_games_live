#!/usr/bin/python3


#taxes and fees - store in cookies
taxes_fees = {
    "refining_station" : {
        "tier_2" : 0.01,
        "tier_3" : 0.04,
        "tier_4" : 0.07,
        "tier_5" : 0.13,
        "tier_5_L" : 0.19,
    },
    "trade_post" : {
        "tax" : 2.5,
        "discount" : 0,
        "duration" : "1_Day"
    },
    "territory" : {
        "company_owned" : False,
        "first_light" : False,
        "weavers_fen" : False
    }
}


# Player Levels - store in cookies
skill_levels = {
    "crafting" : {
        "arcana": 0,
        "armoring": 0,
        "cooking": 0,
        "engineering": 0,
        "furnishing" : 0,
        "jewelcrafting": 0,
        "weaponsmithing": 0
    },
    "refining" : {
        "leatherworking": 0,
        "smelting": 0,
        "stone_cutting": 0,
        "weaving": 0,
        "woodworking": 0
    },
    "gathering" : {
        "fishing" : 0,
        "harvesting" : 0,
        "logging" : 0,
        "mining" : 0,
        "skinning" : 0
    }    
}

# Bonus Gear - store in cookies
gear_sets = {
    "leatherworking" : {
        "leatherworking_headwear" : 0,
        "leatherworking_chestwear" : 0,
        "leatherworking_legwear" : 0,
        "leatherworking_footwear" : 0,
        "leatherworking_glove" : 0
    },
    "smelting" : {
        "smelting_headwear" : 0,
        "smelting_chestwear" : 0,
        "smelting_legwear" : 0,
        "smelting_footwear" : 0,
        "smelting_glove" : 0
    },
    "stone_cutting" : {
        "stone_cutting_headwear" : 0,
        "stone_cutting_chestwear" : 0,
        "stone_cutting_legwear" : 0,
        "stone_cutting_footwear" : 0,
        "stone_cutting_glove" : 0
    },
    "weaving" : {
        "weaving_headwear" : 0,
        "weaving_chestwear" : 0,
        "weaving_legwear" : 0,
        "weaving_footwear" : 0,
        "weaving_glove" : 0
    },
    "woodworking" : {
        "woodworking_headwear" : 0,
        "woodworking_chestwear" : 0,
        "woodworking_legwear" : 0,
        "woodworking_footwear" : 0,
        "woodworking_glove" : 0
    }
}

# Price List - store in cookies
price_list = {
    "refining_component" : {
        "aged_tannin" : 0,
        "obsidian_flux" : 0,
        "obsidian_sandpaper" : 0,
        "wireweave" : 0,
        "pure_solvent" : 0
    },
    "leatherworking" : {
        "rawhide" : 0,
        "coarse_leather" : 0,
        "rugged_leather" : 0,
        "thick_hide" : 0,
        "layered_leather" : 0,
        "iron_hide" : 0,
        "infused_leather" : 0,
        "smolderhide" : 0,
        "scarhide" : 0,
        "runic_leather" : 0
    },
    "smelting" : {
        "iron_ore" : 0,
        "iron_ingot" : 0,
        "charcoal" : 0,
        "steel_ingot" : 0,
        "starmetal_ore" : 0,
        "starmetal_ingot" : 0,
        "orichalcum_ore" : 0,
        "orichalcum_ingot" : 0,
        "tolvium" : 0,
        "cinnabar" : 0,
        "asmodeum" : 0
    },
    "smelting_precious" : {
        "silver_ore" : 0,
        "silver_ingot" : 0,
        "gold_ore" : 0,
        "gold_ingot" : 0,
        "platinum_ore" : 0,
        "platinum_ingot" : 0,
        "charcoal" : 0,
        "orichalcum_ore" : 0,
        "orichalcum_ingot_platinum" : 0
    },
    "stone_cutting" : {
        "stone" : 0,
        "stone_block" : 0,
        "stone_brick" : 0,
        "lodestone_brick" : 0,
        "lodestone" : 0,
        "molten_lodestone" : 0,
        "loamy_lodestone" : 0,
        "shocking_lodestone" : 0,
        "crystalline_lodestone" : 0,
        "freezing_lodestone" : 0,
        "putrid_lodestone" : 0,
        "gleaming_lodestone" : 0,
        "obsidian_voidstone" : 0,
        "runestone" : 0
    },
    "weaving" : {
        "fibers" : 0,
        "linen" : 0,
        "sateen" : 0,
        "silk_threads" : 0,
        "silk" : 0,
        "wirefiber" : 0,
        "infused_silk" : 0,
        "scalecloth" : 0,
        "blisterweave" : 0,
        "phoenixweave" : 0
    },
    "woodworking" : {
        "green_wood" : 0,
        "timber" : 0,
        "aged_wood" : 0,
        "lumber" : 0,
        "wyrdwood" : 0,
        "wyrdwood_planks" : 0,
        "ironwood" : 0,
        "ironwood_planks" : 0,
        "wildwood" : 0,
        "barbvine" : 0,
        "glittering_ebony" : 0  
    }
}


trade_post_template = [
    [   "refining_component",
        "aged_tannin",
        "obsidian_flux",
        "obsidian_sandpaper",
        "wireweave",
        "pure_solvent"
    ],
    [   "leatherworking",
        "rawhide",
        "coarse_leather",
        "rugged_leather",
        "thick_hide",
        "layered_leather",
        "iron_hide",
        "infused_leather",
        "smolderhide",
        "scarhide",
        "runic_leather"
    ],
    [   "smelting",
        "iron_ore",
        "iron_ingot",
        "charcoal",
        "steel_ingot",
        "starmetal_ore",
        "starmetal_ingot",
        "orichalcum_ore",
        "orichalcum_ingot",
        "tolvium",
        "cinnabar",
        "asmodeum"
    ],
    [   "smelting_precious",
        "silver_ore",
        "silver_ingot",
        "gold_ore",
        "gold_ingot",
        "platinum_ore",
        "platinum_ingot"
    ],
    [   "stone_cutting",
        "stone",
        "stone_block",
        "stone_brick",
        "lodestone_brick",
        "lodestone",
        "molten_lodestone",
        "loamy_lodestone",
        "shocking_lodestone",
        "crystalline_lodestone",
        "freezing_lodestone",
        "putrid_lodestone",
        "gleaming_lodestone",
        "obsidian_voidstone",
        "runestone"
    ],
    [   "weaving",
        "fibers",
        "linen",
        "sateen",
        "silk_threads",
        "silk",
        "wirefiber",
        "infused_silk",
        "scalecloth",
        "blisterweave",
        "phoenixweave"
    ],
    [   "woodworking",
        "green_wood",
        "timber",
        "aged_wood",
        "lumber",
        "wyrdwood",
        "wyrdwood_planks",
        "ironwood",
        "ironwood_planks",
        "wildwood",
        "barbvine",
        "glittering_ebony"  
    ]
]


refining_template = [
    [   "leatherworking",
        "coarse_leather",
        "rugged_leather",
        "layered_leather",
        "infused_leather",
        "runic_leather"
    ],
    [   "smelting",
        "iron_ingot",
        "steel_ingot",
        "starmetal_ingot",
        "orichalcum_ingot",
        "asmodeum"
    ],
    [   "smelting_precious",
        "silver_ingot",
        "gold_ingot",
        "platinum_ingot",
        "orichalcum_ingot_platinum"
    ],
    [   "stone_cutting",
        "stone_block",
        "stone_brick",
        "lodestone_brick",
        "obsidian_voidstone",
        "runestone",
        "elemental_lodestone"
    ],
    [   "weaving",
        "linen",
        "sateen",
        "silk",
        "infused_silk",
        "phoenixweave"
    ],
    [   "woodworking",
        "timber",
        "lumber",
        "wyrdwood_planks",
        "ironwood_planks",
        "glittering_ebony"  
    ]
]

navbar_template = [
    [   "leatherworking",
        "rawhide",
        "coarse_leather",
        "rugged_leather",
        "layered_leather",
        "infused_leather",
        "runic_leather"
    ],
    [   "smelting",
        "iron_ore",
        "iron_ingot",
        "steel_ingot",
        "starmetal_ingot",
        "orichalcum_ingot",
        "asmodeum"
    ],
    [   "smelting_precious",
        "silver_ore",
        "silver_ingot",
        "gold_ingot",
        "platinum_ingot",
        "orichalcum_ingot_platinum"
    ],
    [   "stone_cutting",
        "stone",
        "stone_block",
        "stone_brick",
        "lodestone_brick",
        "obsidian_voidstone",
        "runestone",
        "elemental_lodestone"
    ],
    [   "weaving",
        "fibers",
        "linen",
        "sateen",
        "silk",
        "infused_silk",
        "phoenixweave"
    ],
    [   "woodworking",
        "green_wood",
        "timber",
        "lumber",
        "wyrdwood_planks",
        "ironwood_planks",
        "glittering_ebony"  
    ]
]

def init_skill_levels():
    return skill_levels

def init_gear_sets():
    return gear_sets

def init_price_list():
    return price_list

def trade_post_order():
    return trade_post_template

def refining_order():
    return refining_template

def init_taxes_and_fees():
    return taxes_fees

def material_navbar():
    return navbar_template