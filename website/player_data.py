#!/usr/bin/python3


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
    "refining_components" : {
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
        "layered_leather" : 0,
        "infused_leather" : 0,
        "runic_leather" : 0,
        "thick_hide" : 0,
        "iron_hide" : 0,
        "smolderhide" : 0,
        "scarhide" : 0
    },
    "smelting" : {
        "iron_ore" : 0,
        "iron_ingot" : 0,
        "steel_ingot" : 0,
        "starmetal_ingot" : 0,
        "orichalcum_ingot" : 0,
        "asmodeum" : 0,
        "starmetal_ore" : 0,
        "orichalcum_ore" : 0,
        "charcoal" : 0,
        "tolvium" : 0,
        "cinnabar" : 0,
        "silver_ore" : 0,
        "silver_ingot" : 0,
        "gold_ingot" : 0,
        "platinum_ingot" : 0,
        "gold_ore" : 0,
        "platinum_ore" : 0
    },
    "stone_cutting" : {
        "stone" : 0,
        "stone_block" : 0,
        "stone_brick" : 0,
        "lodestone_brick" : 0,
        "obsidian_voidstone" : 0,
        "runestone" : 0,
        "lodestone" : 0,
        "molten_lodestone" : 0,
        "loamy_lodestone" : 0,
        "shocking_lodestone" : 0,
        "crystalline_lodestone" : 0,
        "freezing_lodestone" : 0,
        "putrid_lodestone" : 0,
        "gleaming_lodestone" : 0
    },
    "weaving" : {
        "fibers" : 0,
        "linen" : 0,
        "sateen" : 0,
        "silk" : 0,
        "infused_silk" : 0,
        "phoenixweave" : 0,
        "silk_threads" : 0,
        "wirefiber" : 0,
        "scalecloth" : 0,
        "blisterweave" : 0
    },
    "woodworking" : {
        "green_wood" : 0,
        "timber" : 0,
        "lumber" : 0,
        "wyrdwood_planks" : 0,
        "ironwood_planks" : 0,
        "glittering_ebony" : 0,
        "aged_wood" : 0,
        "wyrdwood" : 0,
        "ironwood" : 0,
        "wildwood" : 0,
        "barbvine" : 0
    }
}



def init_skill_levels():
    return skill_levels

def init_gear_sets():
    return gear_sets

def init_price_list():
    return price_list

