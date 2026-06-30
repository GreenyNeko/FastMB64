bl_info = {
    "name": "FastMB64",
    "author": "GreenyNeko",
    "version": (1, 0, 2),
    "blender": (4, 0, 0),
    "location": "File > Import > MB64",
    "description": "Imports .mb64 file and builds a scene using Fast64",
    "category": "Import-Export",
}

import bpy
from bpy.props import StringProperty
from bpy_extras.io_utils import ImportHelper
import bmesh
from mathutils import Vector, Matrix
import math

def coinFormationParamHandler(self, objData, bParam):
    specialMacros = [{"macro": 'macro_coin_line_horizontal', "name": "(h-line)"},
        {"macro": 'macro_coin_line_vertical', "name": "(v-line)"},
        {"macro": 'macro_coin_ring_horizontal', "name": "(h-ring)"},
        {"macro": 'macro_coin_ring_vertical', "name": "(v-ring)"},
        {"macro": 'macro_coin_arrow', "name": "arrow"}
    ]
    bpy.context.object.sm64_macro_enum = specialMacros[bParam]["macro"]
    bpy.context.object.name = objData["name"] + " " + specialMacros[bParam]["name"]

idToObjData = {2: {"name": "Power Star", "type": 'Object', "model": 'MODEL_STAR', "behavior": '13003e3c', "hasParams": False},
    3: {"name": "Red Coin Star", "type": 'Object', "model": 'MODEL_STAR', "behavior": '13003e8c', "hasParams": False },
    4: {"name": "Goomba", "type": 'Macro', "preset": 'macro_goomba', "hasParams": False},
    5: {"name": "Huge Goomba", "type": 'Macro', "preset": 'macro_huge_goomba', "hasParams": False},
    6: {"name": "Tiny Goomba", "type": 'Macro', "preset": 'macro_tiny_goomba', "hasParams": False},
    7: {"name": "Piranha Plant", "type": 'Macro', "preset": 'macro_piranha_plant', "hasParams": False},
    8: {"name": "Big Piranha Plant", "type": 'Object', "model": 'MODEL_PIRANHA_PLANT', "behavior": '13005120', "hasParams": False},
    9: {"name": "Tiny Piranha Plant", "type": 'Object', "model": 'MODEL_PIRANHA_PLANT', "behavior": '13005120', "hasParams": False},
    10: {"name": "Koopa", "type": 'Macro', "preset": 'macro_koopa', "hasParams": False},
    11: {"name": "Yellow Coin", "type": 'Macro', "preset": 'macro_yellow_coin', "hasParams": False},
    12: {"name": "1-up (Green Coin)", "type": 'Object', "model": 'MODEL_1UP', "behavior": '1300407c', "hasParams": False},
    13: {"name": "Red Coin", "type": 'Macro', "preset": 'macro_red_coin', "hasParams": False},
    14: {"name": "Blue Coin", "type": 'Macro', "preset": 'macro_hidden_blue_coin', "hasParams": False},
    15: {"name": "Blue Coin Switch", "type": 'Macro', "preset": 'macro_blue_coin_switch', "hasParams": False},
    16: {"name": "Trampoline (Noteblock)", "type": 'Object', "model": 'MODEL_TRAMPOLINE', "behavior": '13001608', "hasParams": False},
    17: {"name": "Bob Omb", "type": 'Macro', "preset": 'macro_bobomb', "hasParams": False},
    18: {"name": "Chuckya", "type": 'Macro', "preset": 'macro_chuckya', "hasParams": False},
    19: {"name": "Bully", "type": 'Macro', "preset": 'macro_bully', "hasParams": False},
    20: {"name": "Chill Bully", "type": 'Object', "model": 'MODEL_CHILL_BULLY', "behavior": '130036c8', "hasParams": False},
    21: {"name": "Bullet Bill", "type": 'Macro', "preset": 'macro_bullet_bill_cannon', "hasParams": False},
    22: {"name": "Heave Ho", "type": 'Macro', "preset": 'macro_heave_ho', "hasParams": False},
    23: {"name": "Chuckya (Motos)", "type": 'Object', "model": 'MODEL_CHUCKYA', "behavior": '13000528', "hasParams": False},
    24: {"name": "Tree", "type": 'Object', "model": 'MODEL_BOB_BUBBLY_TREE', "behavior": '13002aa4', "hasParams": False},
    25: {"name": "!-Box", "type": 'Object', "model": 'MODEL_EXCLAMATION_BOX', "behavior": '13002250', "hasParams": False},
    26: {"name": "Mario Spawn", "type": 'Mario Start', "hasParams": False},
    27: {"name": "Shelless Koopa (Rex)", "type": 'Object', "model": 'MODEL_KOOPA_WITHOUT_SHELL', "behavior": '13004580', "hasParams": False},
    28: {"name": "Bouncing Fireball (Poodoobo)", "type": 'Object', "model": 'MODEL_RED_FLAME', "behavior": '13001168', "hasParams": False},
    29: {"name": "Scuttlebug (Crablet)", "type": 'Object', "model": 'MODEL_SCUTTLEBUG', "behavior": '13002b5c', "hasParams": False},
    30: {"name": "Snufit (Hammerbro)", "type": 'Object', "model": 'MODEL_SNUFIT', "behavior": '130051e0', "hasParams": False},
    31: {"name": "Flyguy Flame (Firebro)", "type": 'Object', "model": 'MODEL_FLYGUY', "behavior": '130051ac', "hasParams": False},
    32: {"name": "Flyguy Flame (Chicken)", "type": 'Object', "model": 'MODEL_FLYGUY', "behavior": '130051ac', "hasParams": False},
    33: {"name": "Missing (Cosmic Phantasm)", "type": 'None', "hasParams": False},
    34: {"name": "Warp Pipe", "type": 'Object', "model": 'MODEL_THI_WARP_PIPE', "behavior": '130007a0', "hasParams": False},
    35: {"name": "Missing (Badge)", "type": 'None', "hasParams": False},
    36: {"name": "King Bobomb", "type": 'Object', "model": 'MODEL_KING_BOBOMB', "behavior": '130001f4', "hasParams": False},
    37: {"name": "Whomp King", "type": 'Object', "model": 'MODEL_WHOMP', "behavior": '13002bb8', "hasParams": False},
    38: {"name": "Big Boo", "type": 'Object', "model": 'MODEL_BOO', "behavior": '130027e4', "hasParams": False},
    39: {"name": "Big Bully", "type": 'Object', "model": 'MODEL_BULLY', "behavior": '13003660', "hasParams": False},
    40: {"name": "Big Chill Bully", "type": 'Object', "model": 'MODEL_BIG_CHILL_BULLY', "behavior": '13003700', "hasParams": False},
    41: {"name": "Wiggler", "type": 'Macro', "preset": 'macro_wiggler', "hasParams": False},
    42: {"name": "Bowser", "type": 'Object', "model": 'MODEL_BOWSER', "behavior": '13001850', "hasParams": False},
    43: {"name": "Yellow Platform", "type": 'Object', "model": 'MODEL_CHECKERBOARD_PLATFORM', "behavior": '13004ab0', "hasParams": False},
    44: {"name": "Blue Platform (WIP)", "type": 'Object', "model": 'MODEL_BITS_BLUE_PLATFORM', "behavior": '13004ab0', "hasParams": False},
    45: {"name": "Bowling Ball Spawner", "type": 'Object', "model": 'MODEL_NONE', "behavior": '13003aa4', "hasParams": False},
    46: {"name": "Koopa the Quick", "type": 'Macro', "preset": 'macro_bob_koopa_the_quick', "hasParams": False},
    47: {"name": "Purple Switch", "type": 'Object', "model": 'MODEL_PURPLE_SWITCH', "behavior": '13002558', "hasParams": False},
    48: {"name": "Timed Breakable Box", "type": 'Macro', "preset": 'macro_hidden_box', "hasParams": False},
    49: {"name": "Recovery Heart", "type": 'Macro', "preset": 'macro_recovery_heart', "hasParams": False},
    50: {"name": "Test Mario", "type": 'None', "hasParams": False},
    51: {"name": "Thwomp", "type": 'Macro', "preset": 'macro_thwomp', "hasParams": False},
    52: {"name": "Whomp", "type": 'Macro', "preset": 'macro_whomp', "hasParams": False},
    53: {"name": "Grindel", "type": 'Object', "model": 'MODEL_SSL_GRINDEL', "behavior": '13000b58', "hasParams": False},
    54: {"name": "Lakitu", "type": 'Macro', "preset": 'macro_enemy_lakitu', "hasParams": False},
    55: {"name": "Flyguy", "type": 'Macro', "preset": 'macro_fly_guy', "hasParams": False},
    56: {"name": "Snufit", "type": 'Macro', "preset": 'macro_snufit', "hasParams": False},
    57: {"name": "Circling Amp", "type": 'Macro', "preset": 'macro_circling_amp', "hasParams": False},
    58: {"name": "Boo", "type": 'Macro', "preset": 'macro_boo', "hasParams": False},
    59: {"name": "Mr. I", "type": 'Macro', "preset": 'macro_mr_i', "hasParams": False},
    60: {"name": "Scuttlebug", "type": 'Macro', "preset": 'macro_scuttlebug', "hasParams": False},
    61: {"name": "Bowser Bomb", "type": 'Object', "model": 'MODEL_BOWSER_BOMB', "behavior": '130037ec', "hasParams": False},
    62: {"name": "Firespinner", "type": 'Object', "model": 'MODEL_LLL_ROTATING_BLOCK_FIRE_BARS', "behavior": '13001da8', "hasParams": False},
    63: {"name": "Coin Formation", "type": 'Macro', "preset": 'macro_coin_line_horizontal_flying', "hasParams": True, "paramHandler": coinFormationParamHandler},
    64: {"name": "Red Flame", "type": 'Object', "model": 'MODEL_RED_FLAME', "behavior": '13000c84', "hasParams": False},
    65: {"name": "Blue Flame", "type": 'Object', "model": 'MODEL_BLUE_FLAME', "behavior": '13000c84', "hasParams": False},
    66: {"name": "Fire Spitter", "type": 'Macro', "preset": 'macro_fire_spitter', "hasParams": False},
    67: {"name": "Flamethrower", "type": 'Macro', "preset": 'macro_flamethrower', "hasParams": False},
    68: {"name": "Spindrift", "type": 'Macro', "preset": 'macro_spindrift', "hasParams": False},
    69: {"name": "Mr. Blizzard", "type": 'Macro', "preset": 'macro_mr_blizzard', "hasParams": False},
    70: {"name": "Moneybag", "type": 'Macro', "preset": 'macro_moneybag', "hasParams": False},
    71: {"name": "Skeeter", "type": 'Macro', "preset": 'macro_skeeter', "hasParams": False},
    72: {"name": "Pokey", "type": 'Macro', "preset": 'macro_pokey', "hasParams": False},
    73: {"name": "Small Breakable Box", "type": 'Macro', "preset": 'macro_breakable_box_small', "hasParams": False},
    74: {"name": "Giant Breakable Box", "type": 'Macro', "preset": 'macro_breakable_box_giant', "hasParams": False},
    75: {"name": "Missing (Crazy Box)", "type": 'None', "hasParams": False},
    76: {"name": "Water Diamond", "type": 'Object', "model": 'MODEL_WDW_WATER_LEVEL_DIAMOND', "behavior": '130025f8', "hasParams": False},
    77: {"name": "Wooden Signpost", "type": 'Macro', "preset": 'macro_wooden_signpost', "hasParams": False},
    78: {"name": "Bobomb Buddy (NPC)", "type": 'Object', "model": 'MODEL_BOBOMB_BUDDY', "behavior": '130031dc', "hasParams": False},
    79: {"name": "Missing (Button)", "type": 'None', "hasParams": False},
    80: {"name": "Missing (On Off Block)", "type": 'None', "hasParams": False},
    81: {"name": "Floating Platform", "type": 'Object', "model": 'MODEL_WDW_SQUARE_FLOATING_PLATFORM', "behavior": '13004284', "hasParams": False},
    82: {"name": "Missing (Reinforced Box)", "type": 'None', "hasParams": False},
    83: {"name": "Missing (On Off Block)", "type": 'None', "hasParams": False},
    84: {"name": "Missing (Showrunner)", "type": 'None', "hasParams": False},
    85: {"name": "Missing (Crowbar)", "type": 'None', "hasParams": False},
    86: {"name": "Missing (Bullet Bill Mask)", "type": 'None', "hasParams": False},
    87: {"name": "Toad (NPC)", "type": 'Object', "model": 'MODEL_TOAD', "behavior": '13002ef8', "hasParams": False},
    88: {"name": "Tuxie (NPC)", "type": 'Object', "model": 'MODEL_PENGUIN', "behavior": '13002088', "hasParams": False},
    89: {"name": "Ukiki (NPC)", "type": 'Object', "model": 'MODEL_UKIKI', "behavior": '13002088', "hasParams": False},
    90: {"name": "Toad (NPC Moleman)", "type": 'Object', "model": 'MODEL_MONTY_MOLE', "behavior": '13002ef8', "hasParams": False},
    91: {"name": "Buddy (NPC Cobie)", "type": 'Object', "model": 'MODEL_BOBOMB_BUDDY', "behavior": '130031dc', "hasParams": False},    
    92: {"name": "Treadmill (Conveyor)", "type": 'Macro', "preset": 'macro_ttc_small_treadmill', "hasParams": False},
    93: {"name": "Missing (Timed Block)", "type": 'None', "hasParams": False},
    94: {"name": "Hidden Star Trigger", "type": 'Macro', "preset": 'macro_hidden_star_trigger', "hasParams": False},
    95: {"name": "Star Trigger Star? (WIP)", "type": 'Object', "model": 'MODEL_STAR', "behavior": '13003efc', "hasParams": False},
}

surface_walkable = "SURFACE_NOT_SLIPPERY"
surface_smooth = "SURFACE_DEFAULT"
surface_slippery = "SURFACE_VERY_SLIPPERY"
surface_burning = "SURFACE_BURNING"
surface_hangable = "SURFACE_HANGABLE"

idToMatData = {0: {"surface": surface_walkable, "color": (0.1529,0.8157,0.12157,1), "render": "opaque", "name": "Grass" },
    1: {"surface": surface_walkable, "color": (0.1922,0.8392,0,1), "render": "opaque", "name": "Grass (old)"  },
    2: {"surface": surface_walkable, "color": (0.4902,0.8470,0,1), "render": "opaque", "name": "Smooth Grass"  },
    3: {"surface": surface_walkable, "color": (0,0.3059,0,1), "render": "opaque", "name": "Dark Grass"  }, 
    4: {"surface": surface_walkable, "color": (0.2235,0.2902,0.1608,1), "render": "opaque", "name": "Cave Grass"  },
    5: {"surface": surface_walkable, "color": (0.702,0.3216,0.0235,1), "render": "opaque", "name": "Orange Grass"  },
    6: {"surface": surface_walkable, "color": (0.7216,0.02,0.0157,1), "render": "opaque", "name": "Red Grass"  },
    7: {"surface": surface_walkable, "color": (0.4431,0.1451,0.7961,1), "render": "opaque", "name": "Purple Grass"  },
    8: {"surface": surface_walkable, "color": (1,0.8078,0.4353,1), "render": "opaque", "name": "Sand"  },
    9: {"surface": surface_walkable, "color": (0.6314,0.5961,0.502,1), "render": "opaque", "name": "Ocean Sand"  }, 
    10: {"surface": surface_slippery, "color": (0.0775,0.9059,0.9373,1), "render": "opaque", "name": "Snow"  },
    11: {"surface": surface_slippery, "color": (0.8706,0.9294,1,1), "render": "opaque", "name": "Snow (old)"  },
    12: {"surface": surface_walkable, "color": (0.5108,0.2588,0.1608,1), "render": "opaque", "name": "Dirt"  },
    13: {"surface": surface_walkable, "color": (0.7373,0.4157,0.0941,1), "render": "opaque", "name": "Sandy Dirt"  },
    14: {"surface": surface_walkable, "color": (0.7098,0.4,0.2039,1), "render": "opaque", "name": "Light Dirt"  },
    15: {"surface": surface_walkable, "color": (0.3373,0.2549,0.1451,1), "render": "opaque", "name": "Cave Dirt"  },
    16: {"surface": surface_walkable, "color": (0.349,0.251,0.1882,1), "render": "opaque", "name": "Rocky Dirt"  },
    17: {"surface": surface_walkable, "color": (0.7137,0.3098,0.051,1), "render": "opaque", "name": "Dirt (old)"  },
    18: {"surface": surface_walkable, "color": (0.5451,0.2235,0.0627,1), "render": "opaque", "name": "Orange Wavy Dirt"  },
    19: {"surface": surface_walkable, "color": (0.2902,0.4039,0.494,1), "render": "opaque", "name": "Blue Wavy Dirt"  },
    20: {"surface": surface_walkable, "color": (0.502,0.631,0.6627,1), "render": "opaque", "name": "Snowy Dirt"  },
    21: {"surface": surface_walkable, "color": (0.498,0.2314,0.5255,1), "render": "opaque", "name": "Purple Dirt"  },
    22: {"surface": surface_walkable, "color": (0.5098,0.4196,0.4118,1), "render": "opaque", "name": "Clay"  },
    # stone
    23: {"surface": surface_smooth, "color": (0.8078,0.8078,0.8078,1), "render": "opaque", "name": "White Stone"  },
    24: {"surface": surface_walkable, "color": (0.3569,0.3569,0.3882,1), "render": "opaque", "name": "Cave Stone"  },
    25: {"surface": surface_smooth, "color": (0.5490,0.4824,0.4196,1), "render": "opaque", "name": "Beige Stone"  },
    26: {"surface": surface_walkable, "color": (0.4196,0.5137,0.4118,1), "render": "opaque", "name": "Green Stone"  },
    27: {"surface": surface_walkable, "color": (0.7255,0.4902,0.3059,1), "render": "opaque", "name": "Mountain Stone"  },
    28: {"surface": surface_walkable, "color": (0.6078,0.5059,0.4667,1), "render": "opaque", "name": "Mountain Rock"  },
    29: {"surface": surface_walkable, "color": (0.9294,0.9294,0.9294,1), "render": "opaque", "name": "White Rock"  },
    30: {"surface": surface_walkable, "color": (0.3255,0.3961,0.251,1), "render": "opaque", "name": "Green Rock"  },
    31: {"surface": surface_smooth, "color": (0.1922,0.2235,0.2588,1), "render": "opaque", "name": "Black Rock"  },
    32: {"surface": surface_walkable, "color": (0.1804,0.1804,0.1804,1), "render": "opaque", "name": "Scorched Rock"  },
    33: {"surface": surface_walkable, "color": (0.6863,0.2667,0.0314,1), "render": "opaque", "name": "Volcanic Rocks"  },
    34: {"surface": surface_smooth, "color": (0.4941,0.2431,0.0039,1), "render": "opaque", "name": "Volcanic Wall"  },
    35: {"surface": surface_walkable, "color": (0.3529,0.4157,0.4235,1), "render": "opaque", "name": "Basalt"  },
    36: {"surface": surface_walkable, "color": (0.1294,0.1647,0.2314,1), "render": "opaque", "name": "Obsidian"  },
    37: {"surface": surface_walkable, "color": (0.6941,0.6941,0.7765,1), "render": "opaque", "name": "Plum Concrete"  },
    38: {"surface": surface_walkable, "color": (0.3765,0.5059,0.6902,1), "render": "opaque", "name": "Ocean Floor"  },
    39: {"surface": surface_smooth, "color": (0.4078,0.5059,0.6314,1), "render": "opaque", "name": "Snowy Rock"  },
    40: {"surface": surface_slippery, "color": (0.7333,0.8314,0.9608,1), "render": "opaque", "name": "CCM Slippery Rock"  },
    41: {"surface": surface_walkable, "color": (0.4196,0.4196,0.4196,1), "render": "opaque", "name": "BOB Cobblestone"  },
    42: {"surface": surface_walkable, "color": (0.3333,0.3333,0.3333,1), "render": "opaque", "name": "Cobblestone (2)"  },
    43: {"surface": surface_walkable, "color": (0.5647,0.5333,0.6039,1), "render": "opaque", "name": "JRB Cobblestone"  },
    # bricks
    44: {"surface": surface_smooth, "color": (0.651,0.651,0.651,1), "render": "opaque", "name": "Stone Bricks"  },
    45: {"surface": surface_smooth, "color": (0.6549,0.4902,0.102,1), "render": "opaque", "name": "Pyramid Bricks"  },
    46: {"surface": surface_walkable, "color": (0.1608,0.1608,0.1608,1), "render": "opaque", "name": "Scorched Bricks"  },
    47: {"surface": surface_smooth, "color": (0.2118,0.149,0.1294,1), "render": "opaque", "name": "HMC Bricks"  },
    48: {"surface": surface_smooth, "color": (0.4353,0.3686,0.3373,1), "render": "opaque", "name": "WF Wall"  },
    49: {"surface": surface_smooth, "color": (0.3333,0.2706,0.2235,1), "render": "opaque", "name": "WF Ground"  },
    50: {"surface": surface_smooth, "color": (0.3529,0.1529,0.086,1), "render": "opaque", "name": "Brown Bricks"  },
    51: {"surface": surface_walkable, "color": (0.5647,0.4878,0.3098,1), "render": "opaque", "name": "Castle Bricks"  },
    52: {"surface": surface_walkable, "color": (0.451,0.1725,0.0627,1), "render": "opaque", "name": "Red Bricks Dark"  },
    53: {"surface": surface_smooth, "color": (1,0.3765,0.1804,1), "render": "opaque", "name": "Red Bricks Bright"  },
    54: {"surface": surface_smooth, "color": (0.9137,0.9137,0.9137,1), "render": "opaque", "name": "White Bricks Big"  },
    55: {"surface": surface_smooth, "color": (0.8353,0.9059,0.9412,1), "render": "opaque", "name": "White Bricks Small"  },
    56: {"surface": surface_smooth, "color": (0.0667,0.3569,0.3647,1), "render": "opaque", "name": "Ocean Bricks"  },
    57: {"surface": surface_smooth, "color": (0.4627,0.5922,0.7647,1), "render": "opaque", "name": "Blue Bricks"  },
    58: {"surface": surface_walkable, "color": (0.7137,0.7137,0.6824,1), "render": "opaque", "name": "Mixed Bricks"  },
    # tiling
    59: {"surface": surface_walkable, "color": (0.5804,0.5725,0.4745,1), "render": "opaque", "name": "Checkered Tiling"  },
    60: {"surface": surface_walkable, "color": (0.4941,0.4941,0.4941,1), "render": "opaque", "name": "Castle Tiling"  },
    61: {"surface": surface_walkable, "color": (0.7725,0.3176,0.0627,1), "render": "opaque", "name": "Desert Tiling"  },
    62: {"surface": surface_walkable, "color": (0.7765,0.8392,0.8275,1), "render": "opaque", "name": "Blue Tiling Pastel"  },
    63: {"surface": surface_walkable, "color": (0.2039,0.4,0.6275,1), "render": "opaque", "name": "Blue Tiling Dark"  },
    64: {"surface": surface_walkable, "color": (0.2235,0.3529,0.3216,1), "render": "opaque", "name": "Ocean Tiling 2x2"  },
    65: {"surface": surface_smooth, "color": (0.2275,0.2275,0.2275,1), "render": "opaque", "name": "Ocean Tiling 4x4"  },
    66: {"surface": surface_walkable, "color": (0.2275,0.2275,0.2275,1), "render": "opaque", "name": "Dark Tiling"  },
    67: {"surface": surface_walkable, "color": (0.5922,0.4902,0.4588,1), "render": "opaque", "name": "Granite Tiling"  },
    68: {"surface": surface_walkable, "color": (0.2588,0.2588,0.2588,1), "render": "opaque", "name": "Black Tiling"  },
    69: {"surface": surface_smooth, "color": (0.5608,0.5608,0.5608,1), "render": "opaque", "name": "Grey Tiling"  },
    70: {"surface": surface_walkable, "color": (0.4392,0.4392,0.4706,1), "render": "opaque", "name": "Diamond Pattern"  },
    71: {"surface": surface_walkable, "color": (0.6824,0.6824,0.6824,1), "render": "opaque", "name": "Hex Tiling"  },
    72: {"surface": surface_smooth, "color": (0.7843,0.8392,0.8706,1), "render": "opaque", "name": "Diamond Tiling"  },
    # cut stone
    73: {"surface": surface_walkable, "color": (0.3529,0.3725,0.3725,1), "render": "opaque", "name": "Stone Block"  }, 
    74: {"surface": surface_smooth, "color": (0.5137,0.5137,0.5137,1), "render": "opaque", "name": "Smooth Block"  },
    75: {"surface": surface_smooth, "color": (0.4902,0.4706,0.6275,1), "render": "opaque", "name": "Mansion Wall"  },
    76: {"surface": surface_smooth, "color": (0.4627,0.4314,0.549,1), "render": "opaque", "name": "Chiseled Wall"  },
    77: {"surface": surface_smooth, "color": (0.5647,0.498,0.4667,1), "render": "opaque", "name": "Patterned Block"  },
    78: {"surface": surface_smooth, "color": (0.2863,0.2863,0.2863,1), "render": "opaque", "name": "Black Slabs"  },
    79: {"surface": surface_smooth, "color": (0.1216,0.1216,0.1216,1), "render": "opaque", "name": "Chiseled Block"  },
    80: {"surface": surface_walkable, "color": (0.7137,0.4275,0.3294,1), "render": "opaque", "name": "Granite Block"  },
    81: {"surface": surface_smooth, "color": (0.6784,0.6784,0.6784,1), "render": "opaque", "name": "Stone Slab"  },
    82: {"surface": surface_smooth, "color": (0.7294,0.7294,0.7333,1), "render": "opaque", "name": "Castle Pillar"  },
    83: {"surface": surface_smooth, "color": (0.4157,0.4157,0.5373,1), "render": "opaque", "name": "Mansion Pillar"  },
    84: {"surface": surface_walkable, "color": (0.1922,0.1922,0.1922,1), "render": "opaque", "name": "Scorched Pillar"  },
    # wood
    85: {"surface": surface_walkable, "color": (0.651,0.4392,0.2,1), "render": "opaque", "name": "Planks (1)"  },
    86: {"surface": surface_walkable, "color": (0.4078,0.251,0.1255,1), "render": "opaque", "name": "Planks (2)"  },
    87: {"surface": surface_walkable, "color": (0.1922,0.0941,0.0314,1), "render": "opaque", "name": "Dark Planks"  },
    88: {"surface": surface_walkable, "color": (0.4667,0.3529,0.1569,1), "render": "opaque", "name": "Castle Planks"  },
    89: {"surface": surface_walkable, "color": (0.2667,0.2471,0.0824,1), "render": "opaque", "name": "Docks"  },
    90: {"surface": surface_walkable, "color": (0.149,0.302,0.4,1), "render": "opaque", "name": "Ship Planks"  },
    91: {"surface": surface_walkable, "color": (0.3215,0.298,0.298,1), "render": "opaque", "name": "Ship Decking"  },
    92: {"surface": surface_walkable, "color": (0.1255,0.0902,0.0588,1), "render": "opaque", "name": "Spooky Planks"  },
    93: {"surface": surface_walkable, "color": (0.2235,0.0314,0,1), "render": "opaque", "name": "Masion Roof"  },
    94: {"surface": surface_walkable, "color": (0.4667,0.302,0.2078,1), "render": "opaque", "name": "Wood (old)"  },
    95: {"surface": surface_walkable, "color": (0.2196,0.1882,0.1882,1), "render": "opaque", "name": "Scorched Wood"  },
    # metal
    96: {"surface": surface_walkable, "color": (0.3647,0.4,0.3333,1), "render": "opaque", "name": "Metal Flooring"  },
    97: {"surface": surface_smooth, "color": (0.3882,0.3882,0.6471,1), "render": "opaque", "name": "Metal Sheet"  },
    98: {"surface": surface_smooth, "color": (0.3882,0.3333,0.2902,1), "render": "opaque", "name": "Metal Plating"  },
    99: {"surface": surface_smooth, "color": (0.2667,0.3608,0.2941,1), "render": "opaque", "name": "Basement Plating"  },
    100: {"surface": surface_smooth, "color": (0.6039,0.5098,0.1843,1), "render": "opaque", "name": "Desert Plating"  }, 
    101: {"surface": surface_smooth, "color": (0.3922,0.349,0.2549,1), "render": "opaque", "name": "Rusted Block"  },
    #other
    102: {"surface": surface_walkable, "color": (0.5882,0.0941,0.0941,1), "render": "opaque", "name": "Carpet"  },
    103: {"surface": surface_smooth, "color": (0.9451,0.7765,0.5608,1), "render": "opaque", "name": "Castle Wall"  },
    104: {"surface": surface_walkable, "color": (0.8353,0.1922,0.1922,1), "render": "opaque", "name": "Roof"  },
    105: {"surface": surface_walkable, "color": (1,0.3529,0.1294,1), "render": "opaque", "name": "Castle Roof"  },
    106: {"surface": surface_slippery, "color": (0.1922,0.4157,0.902,1), "render": "opaque", "name": "Blue Roof"  },
    107: {"surface": surface_smooth, "color": (0.7725,0.451,0.0784,1), "render": "opaque", "name": "Window"  },
    108: {"surface": surface_smooth, "color": (0.9686,0.2471,0,1), "render": "opaque", "name": "Lantern"  },
    109: {"surface": surface_smooth, "color": (0.9686,0.71,0.0078,1), "render": "opaque", "name": "Hazard Stripes" },
    110: {"surface": surface_smooth, "color": (0.9608,0.7529,0.8588,1), "render": "opaque", "name": "Rainbow Blocks"  },
    111: {"surface": surface_walkable, "color": (0.8706,0.8706,0.6118,1), "render": "opaque", "name": "Studded Tile"  },
    112: {"surface": surface_smooth, "color": (1,0.7765,0,1), "render": "opaque", "name": "Yellow Block"  },
    113: {"surface": surface_smooth, "color": (0.4706,0.3412,0.1059,1), "render": "opaque", "name": "Clock Platform"  },
    114: {"surface": surface_smooth, "color": (0.2588,0.1451,0.0314,1), "render": "opaque", "name": "Clock Exterior"  },
    115: {"surface": surface_walkable, "color": (1,0.7843,0.1922,1), "render": "opaque", "name": "Flowers"  },
    #hazards
    116: {"surface": surface_burning, "color": (0.8353,0.1569,0.0589,1), "render": "opaque", "name": "Lava"  },
    117: {"surface": surface_burning, "color": (0.7608,0.016,0,1), "render": "opaque", "name": "Lava (Old)"  },
    118: {"surface": surface_burning, "color": (0,0,0.0863,1), "render": "opaque", "name": "Server Acid"  },
    119: {"surface": surface_burning, "color": (0.4784,0.7373,0.8667,1), "render": "opaque", "name": "Hazard Ice"  },
    120: {"surface": "SURFACE_INSTANT_QUICKSAND", "color": (0.6392,0.502,0.1529,1), "render": "opaque", "name": "Quicksand"  },
    121: {"surface": "SURFACE_DEEP_QUICKSAND", "color": (0.8706,0.6784,0.4157,1), "render": "opaque", "name": "Slow Quicksand"  },
    122: {"surface": "SURFACE_INSTANT_QUICKSAND", "color": (0.0667,0.0039,0.0039,1), "render": "opaque", "name": "Cosmic Void"  },
    #seethrough
    123: {"surface": surface_hangable, "color": (0.6157,0.6157,0.6157,1), "render": "cutout", "name": "Mesh"  },
    124: {"surface": surface_hangable, "color": (0.4588,0.4588,0.4588,1.), "render": "cutout", "name": "Fine Mesh"  },
    125: {"surface": surface_hangable, "color": (0.3804,0.078,0.1176,1), "render": "cutout", "name": "Red Grille"  },
    126: {"surface": surface_hangable, "color": (0.3216,0,0,1.), "render": "cutout", "name": "Red Mesh"  },
    127: {"surface": surface_hangable, "color": (0.4392,0.2863,0.3059,1), "render": "cutout", "name": "Pink Mesh"  },
    128: {"surface": surface_hangable, "color": (0.7843,0.7216,0.4353,1), "render": "cutout", "name": "Clock Grille"  },
    129: {"surface": surface_slippery, "color": (0.2392,0.4353,0.6706,0.75), "render": "transparent", "name": "Ice"  },
    130: {"surface": surface_smooth, "color": (0.7373,0.8235,0.851,0.75), "render": "transparent", "name": "Crystal"  },
    131: {"surface": surface_smooth, "color": (0,0,0,1), "render": "opaque", "name": "Screen"  },
    #retro
    132: {"surface": surface_walkable, "color": (0.7765,0.2902,0.0314,1), "render": "opaque", "name": "Retro Ground"  },
    133: {"surface": surface_smooth, "color": (0.5647,0.2118,0.0235,1), "render": "opaque", "name": "Retro Bricks"  },
    134: {"surface": surface_walkable, "color": (0.502,0.8157,0.0627,1), "render": "opaque", "name": "Treetop"  },
    135: {"surface": surface_smooth, "color": (0.7765, 0.2902, 0.0314,1), "render": "opaque", "name": "Tree"  },
    136: {"surface": surface_walkable, "color": (0.8867,0.5922,0.3529,1), "render": "opaque", "name": "Retro Block"  },
    137: {"surface": surface_walkable, "color": (0,0.5176,0.549,1), "render": "opaque", "name": "Blue Ground"  },
    138: {"surface": surface_smooth, "color": (0,0.3765,0.4,1), "render": "opaque", "name": "Blue Bricks"  },
    139: {"surface": surface_walkable, "color": (0.1686,0.651,0.6549,1), "render": "opaque", "name": "Blue Block"  },
    140: {"surface": surface_smooth, "color": (0.7059,0.7059,0.7059,1), "render": "opaque", "name": "White Bricks"  },
    141: {"surface": surface_burning, "color": (0.8392,0.1608,0,1), "render": "opaque", "name": "Retro Lava"  },
    142: {"surface": surface_walkable, "color": (0,0.6471,0,1), "render": "opaque", "name": "Underwater Tile"  },
    #minecraft
    143: {"surface": surface_walkable, "color": (0.5804,0.4196,0.2902,1), "render": "opaque", "name": "MC Dirt" },
    144: {"surface": surface_walkable, "color": (0.3882,0.5176,0.2588,1), "render": "opaque", "name": "MC Grass"  },
    145: {"surface": surface_walkable, "color": (0.6471,0.6471,0.6471,1), "render": "opaque", "name": "MC Cobblestone"  },
    146:{"surface": surface_smooth, "color": (0.4823,0.4823,0.4823,1), "render": "opaque", "name": "MC Stone"  },
    147: {"surface": surface_walkable, "color": (0.6784,0.549,0.3216,1), "render": "opaque", "name": "Log Top"  },
    148: {"surface": surface_walkable, "color": (0.4627,0.3686,0.3686,1), "render": "opaque", "name": "Log Side"  },
    149: {"surface": surface_walkable, "color": (0.251,0.3137,0.1569,1), "render": "cutout", "name": "Leaves"  },
    150: {"surface": surface_walkable, "color": (0.7098,0.5804,0.3882,1), "render": "opaque", "name": "MC Planks"  },
    151: {"surface": surface_walkable, "color": (0.8706,0.8078,0.6471,1), "render": "opaque", "name": "MC Sand"  },
    152: {"surface": surface_smooth, "color": (0.549,0.3216,0.2588,1), "render": "opaque", "name": "MC Bricks"  },
    153: {"surface": surface_burning, "color": (0.8353,0.3176,0.0588,1), "render": "opaque", "name": "MC Lava"  },
    154: {"surface": surface_burning, "color": (0.8353,0.3176,0.0589,1), "render": "opaque", "name": "MC Lava 'Flowing'"  },
    155: {"surface": surface_smooth, "color": (0.8078,0.9059,0.9059,0.25), "render": "cutout", "name": "MC Glass"  }
}

def materialSettingCutout():
    bpy.context.object.active_material.f3d_mat.draw_layer.sm64 = '4'
    bpy.context.object.active_material.f3d_mat.combiner1.A = 'TEXEL0'
    bpy.context.object.active_material.f3d_mat.combiner1.A_alpha = 'TEXEL0'
    bpy.context.object.active_material.f3d_mat.combiner1.C = 'SHADE'
    bpy.context.object.active_material.f3d_mat.combiner1.C_alpha = 'ENVIRONMENT'
    bpy.context.object.active_material.f3d_mat.combiner1.D = '0'
    bpy.context.object.active_material.f3d_mat.combiner1.D_alpha = '0'
    bpy.context.object.active_material.f3d_mat.rdp_settings.g_cull_back = False

def materialSettingTransparent():
    bpy.context.object.active_material.f3d_mat.draw_layer.sm64 = '5'
    bpy.context.object.active_material.f3d_mat.combiner1.A = 'TEXEL0'
    bpy.context.object.active_material.f3d_mat.combiner1.A_alpha = 'TEXEL0'
    bpy.context.object.active_material.f3d_mat.combiner1.C = 'SHADE'
    bpy.context.object.active_material.f3d_mat.combiner1.C_alpha = 'PRIMITIVE'
    bpy.context.object.active_material.f3d_mat.combiner1.D = '0'
    bpy.context.object.active_material.f3d_mat.combiner1.D_alpha = '0'
    bpy.context.object.active_material.f3d_mat.rdp_settings.g_cull_back = False

renderToMaterialSetup = {"opaque": lambda: None, "cutout": materialSettingCutout, "transparent": materialSettingTransparent}

idToBackground = {0: 'OCEAN_SKY', 1: 'BELOW_CLOUDS', 2: 'FLAMING_SKY', 3: 'GREEN_SKY', 4: 'HAUNTED',
    5:  'SNOW_MOUNTAINS', 6: 'DESERT', 7: 'UNDERWATER_CITY', 8:  'PURPLE_SKY', 9: 'NONE'
}

idToSequence = {0: 'SEQ_LEVEL_GRASS', 1: 'SEQ_LEVEL_SLIDE', 2: 'SEQ_LEVEL_WATER', 3: 'SEQ_LEVEL_WATER',
    4: 'SEQ_LEVEL_HOT', 5: 'SEQ_LEVEL_SNOW', 6: 'SEQ_LEVEL_SPOOKY', 7: 'SEQ_LEVEL_UNDERGROUND',
    8: 'SEQ_LEVEL_UNDERGROUND', 9: 'SEQ_LEVEL_KOOPA_ROAD', 10: 'SEQ_EVENT_BOSS',
    11: 'SEQ_LEVEL_BOSS_KOOPA', 12: 'SEQ_LEVEL_BOSS_KOOPA_FINAL', 13: 'SEQ_LEVEL_INSIDE_CASTLE',
}

# WIP: NONE, ASHES?, SNOW, RAIN, SANDSTORM?
idToEnvFX = {0: 'ENVFX_MODE_NONE', 1: 'ENVFX_LAVA_BUBBLES', 2: 'ENVFX_SNOW_NORMAL', 3: 'ENVFX_SNOW_WATER',
    4: 'ENVFX_JETSTREAM_BUBBLES'
}

# idk how exactly this works but... magic?
#0 is fine, 4 is fine? 2 is fine, 6 is fine
# 1 did nothing,
# found something with rot value 7?
rotCorrection = {0: 0, 1: 0, 2: 1, 3: 1, 4: 2, 5: 2, 6: 3, 7: 3}

def compute_face_normal(face_verts):
    """Compute the normal of a face from its vertices."""
    if len(face_verts) == 3:
        v0, v1, v2 = face_verts[0].co, face_verts[1].co, face_verts[2].co
        normal = (v1 - v0).cross(v2 - v0).normalized()
    elif len(face_verts) == 4:
        v0, v1, v2, v3 = face_verts[0].co, face_verts[1].co, face_verts[2].co, face_verts[3].co
        n1 = (v1 - v0).cross(v2 - v0).normalized()
        n2 = (v2 - v0).cross(v3 - v0).normalized()
        normal = (n1 + n2).normalized()
    else:
        raise ValueError("Face must be triangle or quad")
    return normal

def createPoly(curr_bm, pos, rot, verts, faces):
    vertCount = len(curr_bm.verts)
    for v in verts:
        v = Vector(v)
        v = Matrix.Rotation((rotCorrection[rot] % 4) * math.pi / 2., 3, 'Z') @ v
        v = (v[0]+pos[0],v[1]+pos[1],v[2]+pos[2])
        curr_bm.verts.new(v)
    curr_bm.verts.ensure_lookup_table()
    for face in faces:
        verts = [curr_bm.verts[i+vertCount] for i in face]
        newFace = curr_bm.faces.new(verts)
        newFace.normal = compute_face_normal(verts)

def checkIfRenderFace(thisFlag, thatFlag):
    sum = thisFlag + thatFlag
    flags = thisFlag & thatFlag
    return flags != thisFlag or sum == 0

# only add faces that aren't blocked
# bottom(0,1,2,3) top(4,5,6,7) xFace (1,2,5,4) mxface (3,0,7,4), yFace(2,3,7,6), myface(0,1,4,5)
def renderOuterFaces(faces, pos, tileGrid, bottomFace, topFace, xFace, mxFace, yFace, myFace):
    # tilecoverfalgs: bot,top,for,left,back,right
    currTile = tileGrid[pos]
    topPos = (pos[0],pos[1],pos[2]+1)
    bottomPos = (pos[0],pos[1],pos[2]-1)
    positions = [(pos[0]+1,pos[1],pos[2]),(pos[0],pos[1]-1,pos[2]),(pos[0]-1,pos[1],pos[2]),(pos[0],pos[1]+1,pos[2])]
    xPos = positions[(0 - rotCorrection[currTile["rot"]]) % 4]
    mxPos = positions[(2 - rotCorrection[currTile["rot"]]) % 4]
    yPos = positions[(3 - rotCorrection[currTile["rot"]]) % 4]
    myPos = positions[(1 - rotCorrection[currTile["rot"]]) % 4]
    if topFace:
        if topPos in tileGrid:
            topTile = tileGrid[topPos]
            if currTile["type"] in tileCoverFlags and topTile["type"] in tileCoverFlags:
                if checkIfRenderFace(tileCoverFlags[currTile["type"]][1], tileCoverFlags[topTile["type"]][0]):
                    faces.append(topFace)
            else:
                faces.append(topFace)
        else:
            faces.append(topFace)
    if bottomFace:
        if bottomPos in tileGrid:
            bottomTile = tileGrid[bottomPos]
            if currTile["type"] in tileCoverFlags and bottomTile["type"] in tileCoverFlags:
                if checkIfRenderFace(tileCoverFlags[currTile["type"]][0], tileCoverFlags[bottomTile["type"]][1]):
                    faces.append(bottomFace)
            else:
                faces.append(topFace)
        else:
            faces.append(bottomFace)
    if xFace:
        if xPos in tileGrid:
            xTile = tileGrid[xPos]
            thisRot = 2 + 2 # (3 + rotCorrection[currTile["rot"]]) % 4
            thatRot = 2 + 0# (1 + rotCorrection[xTile["rot"]]) % 4
            if currTile["type"] in tileCoverFlags and xTile["type"] in tileCoverFlags:
                if checkIfRenderFace(tileCoverFlags[currTile["type"]][thisRot], tileCoverFlags[xTile["type"]][thatRot]):
                    faces.append(xFace)
            else:
                faces.append(xFace)
        else:
            faces.append(xFace)
    if mxFace:
        if mxPos in tileGrid:
            mxTile = tileGrid[mxPos]
            thisRot = 2 + 2 #(1 + rotCorrection[currTile["rot"]]) % 4
            thatRot = 2 + 0#(3 + rotCorrection[mxTile["rot"]]) % 4
            if currTile["type"] in tileCoverFlags and mxTile["type"] in tileCoverFlags:
                if checkIfRenderFace(tileCoverFlags[currTile["type"]][thisRot], tileCoverFlags[mxTile["type"]][thatRot]):
                    faces.append(mxFace)
            else:
                faces.append(mxFace)
        else:
            faces.append(mxFace)
    if yFace:
        if yPos in tileGrid:
            yTile = tileGrid[yPos]
            thisRot = 2 + 3#(0 + rotCorrection[currTile["rot"]]) % 4
            thatRot = 2 + 1#(2 + rotCorrection[yTile["rot"]]) % 4
            if currTile["type"] in tileCoverFlags and yTile["type"] in tileCoverFlags:
                if checkIfRenderFace(tileCoverFlags[currTile["type"]][thisRot],tileCoverFlags[yTile["type"]][thatRot]):
                    faces.append(yFace)
            else:
                faces.append(yFace)
        else:
            faces.append(yFace)
    if myFace:
        if myPos in tileGrid:
            myTile = tileGrid[myPos]
            thisRot = 2 + 3#(2 + rotCorrection[currTile["rot"]]) % 4
            thatRot = 2 + 1#(0 + rotCorrection[myTile["rot"]]) % 4
            if currTile["type"] in tileCoverFlags and myTile["type"] in tileCoverFlags:
                if checkIfRenderFace(tileCoverFlags[currTile["type"]][thisRot],tileCoverFlags[myTile["type"]][thatRot]):
                    faces.append(myFace)
            else:
                faces.append(myFace)
        else:
            faces.append(myFace)
    return faces

# bottom(0,1,2,3) top(4,5,6,7) xFace (1,2,6,5) mxface (3,0,7,4), yFace(2,3,7,6), myface(0,1,4,5)
def createSlope(curr_bm, tileGrid, pos, rot):
    verts = [(-0.5,-0.5,-0.5), (0.5,-0.5,-0.5), (0.5,0.5,-0.5), (-0.5,0.5,-0.5),(-0.5,-0.5,0.5), (0.5,-0.5,0.5), (0.5,0.5,0.5), (-0.5,0.5,0.5), ]
    faces = [(4,5,2,3)]
    renderOuterFaces(faces, pos, tileGrid, (3,2,1,0), None, (1,2,5), (4,3,0), (0,1,5,4), None)
    createPoly(curr_bm, pos, rot, verts, faces)
    return len(faces)

def createDownSlope(curr_bm, tileGrid, pos, rot):
    verts = [(-0.5,-0.5,0.5), (0.5,-0.5,0.5), (0.5,0.5,0.5), (-0.5,0.5,0.5),(-0.5,-0.5,-0.5), (0.5,-0.5,-0.5), (0.5,0.5,-0.5), (-0.5,0.5,-0.5), ]
    faces = [(4,5,1,0)]
    renderOuterFaces(faces, pos, tileGrid, None, (0,1,2,3), (5,2,1), (0,3,4), (3,2,5,4), None)
    createPoly(curr_bm, pos, rot, verts, faces)
    return len(faces)

def createSlab(curr_bm, tileGrid, pos, rot):
    verts = [(-0.5,-0.5,-0.5), (0.5,-0.5,-0.5), (0.5,0.5,-0.5), (-0.5,0.5,-0.5),(-0.5,-0.5,0.), (0.5,-0.5,0.), (0.5,0.5,0.), (-0.5,0.5,0.), ]
    faces = [(4,5,6,7) ]
    renderOuterFaces(faces, pos, tileGrid, (3,2,1,0), None, (1,2,6,5), (4,7,3,0), (2,3,7,6), (0,1,5,4))
    createPoly(curr_bm, pos, rot, verts, faces)
    return len(faces)

def createDownSlab(curr_bm, tileGrid, pos, rot):
    verts = [(-0.5,-0.5,-0.), (0.5,-0.5,-0.), (0.5,0.5,-0.), (-0.5,0.5,-0.),(-0.5,-0.5,0.5), (0.5,-0.5,0.5), (0.5,0.5,0.5), (-0.5,0.5,0.5), ]
    faces = [(3,2,1,0)]
    renderOuterFaces(faces, pos, tileGrid, None, (4,5,6,7), (1,2,6,5), (4,7,3,0), (2,3,7,6), (0,1,5,4))  
    createPoly(curr_bm, pos, rot, verts, faces)
    return len(faces)

def createCorner(curr_bm, tileGrid, pos, rot):
    #2,6 3,7 0,4
    verts = [(-0.5,-0.5,-0.5), (0.5,-0.5,-0.5), (0.5,0.5,-0.5), (-0.5,0.5,-0.5),(-0.5,-0.5,0.5), (0.5,-0.5,0.5), (0.5,0.5,0.5), (-0.5,0.5,0.5), ]
    faces = [(0,1,5), (1,2,5)]
    renderOuterFaces(faces, pos, tileGrid, (3,2,1,0), None, None, (3,0,5), (3,5,2), None)
    createPoly(curr_bm, pos, rot, verts, faces)
    return len(faces)

def createDownCorner(curr_bm, tileGrid, pos, rot):
    verts = [(-0.5,-0.5,0.5), (0.5,-0.5,0.5), (0.5,0.5,0.5), (-0.5,0.5,0.5),(-0.5,-0.5,-0.5), (0.5,-0.5,-0.5), (0.5,0.5,-0.5), (-0.5,0.5,-0.5), ]
    faces = [(5,1,0), (5,2,1)]
    renderOuterFaces(faces, pos, tileGrid, None, (0,1,2,3), None, (5,0,3), (2,5,3), None)
    createPoly(curr_bm, pos, rot, verts, faces)
    return len(faces)

def createInvCorner(curr_bm, tileGrid, pos, rot):
    #7->3?
    verts = [(-0.5,-0.5,-0.5), (0.5,-0.5,-0.5), (0.5,0.5,-0.5), (-0.5,0.5,-0.5),(-0.5,-0.5,0.5), (0.5,-0.5,0.5), (0.5,0.5,0.5), (-0.5,0.5,0.5), ]
    faces = [(4,5,3), (3,5,6)]
    renderOuterFaces(faces, pos, tileGrid, (3,2,1,0), None, (1,2,6,5), (4,3,0), (2,3,6), (0,1,5,4))
    createPoly(curr_bm, pos, rot, verts, faces)
    return len(faces)

def createDownInvCorner(curr_bm, tileGrid, pos, rot):
    verts = [(-0.5,-0.5,0.5), (0.5,-0.5,0.5), (0.5,0.5,0.5), (-0.5,0.5,0.5),(-0.5,-0.5,-0.5), (0.5,-0.5,-0.5), (0.5,0.5,-0.5), (-0.5,0.5,-0.5), ]
    faces = [(3,5,4), (6,5,3)]
    renderOuterFaces(faces, pos, tileGrid, None, (0,1,2,3), (5,6,2,1), (0,3,4), (6,3,2), (4,5,1,0))
    createPoly(curr_bm, pos, rot, verts, faces)
    return len(faces)

def createSlopedCorner(curr_bm, tileGrid, pos, rot):
    # 5,1 core -> 4,0 & 6,2
    # no 7,3 no 6 no 4
    verts = [(-0.5,-0.5,-0.5), (0.5,-0.5,-0.5), (0.5,0.5,-0.5), (-0.5,0.5,-0.5),(-0.5,-0.5,0.5), (0.5,-0.5,0.5), (0.5,0.5,0.5), (-0.5,0.5,0.5), ]
    faces = [(5,2,0)]
    renderOuterFaces(faces, pos, tileGrid, (2,1,0), None, (1,2,5), None, None, (0,1,5))
    #renderOuterFaces(faces, pos, tileGrid, (3,2,1,0), (4,5,6,7), (1,2,6,5), (4,7,3,0), (2,3,7,6), (0,1,5,4))
    createPoly(curr_bm, pos, rot, verts, faces)
    return len(faces)

def createDownSlopedCorner(curr_bm, tileGrid, pos, rot):
    verts = [(-0.5,-0.5,0.5), (0.5,-0.5,0.5), (0.5,0.5,0.5), (-0.5,0.5,0.5),(-0.5,-0.5,-0.5), (0.5,-0.5,-0.5), (0.5,0.5,-0.5), (-0.5,0.5,-0.5), ]
    faces = [(0,2,5)]
    renderOuterFaces(faces, pos, tileGrid, None, (0,1,2), (5,2,1), None, None, (5,1,0))
    createPoly(curr_bm, pos, rot, verts, faces)
    return len(faces)

def createInvSlopedCorner(curr_bm, tileGrid, pos, rot):
    #7 into 3
    verts = [(-0.5,-0.5,-0.5), (0.5,-0.5,-0.5), (0.5,0.5,-0.5), (-0.5,0.5,-0.5),(-0.5,-0.5,0.5), (0.5,-0.5,0.5), (0.5,0.5,0.5), (-0.5,0.5,0.5), ]
    faces = [(4,6,3)]
    #renderOuterFaces(faces, pos, tileGrid, (3,2,1,0), (4,5,6,7), (1,2,6,5), (4,7,3,0), (2,3,7,6), (0,1,5,4))
    renderOuterFaces(faces, pos, tileGrid, (3,2,1,0), (4,5,6), (1,2,6,5), (4,3,0), (2,3,6), (0,1,5,4))
    createPoly(curr_bm, pos, rot, verts, faces)
    return len(faces)

def createDownInvSlopedCorner(curr_bm, tileGrid, pos, rot):
    #7 into 3
    verts = [(-0.5,-0.5,0.5), (0.5,-0.5,0.5), (0.5,0.5,0.5), (-0.5,0.5,0.5),(-0.5,-0.5,-0.5), (0.5,-0.5,-0.5), (0.5,0.5,-0.5), (-0.5,0.5,-0.5), ]
    faces = [(3,6,4)]
    renderOuterFaces(faces, pos, tileGrid, (6,5,4), (0,1,2,3), (5,6,2,1), (0,3,4), (6,3,2), (4,5,1,0))
    createPoly(curr_bm, pos, rot, verts, faces)
    return len(faces)

def createUpperGentle(curr_bm, tileGrid, pos, rot):
    verts = [(-0.5,-0.5,-0.5), (0.5,-0.5,-0.5), (0.5,0.5,-0.5), (-0.5,0.5,-0.5),(-0.5,-0.5,0.5), (0.5,-0.5,0.5), (0.5,0.5,0.), (-0.5,0.5,0.), ]
    faces = [(4,5,6,7)]
    renderOuterFaces(faces, pos, tileGrid, (3,2,1,0), None, (1,2,6,5), (4,7,3,0), (2,3,7,6), (0,1,5,4))
    #renderOuterFaces(faces, pos, tileGrid, (3,2,1,0), (4,5,6,7), (1,2,6,5), (4,7,3,0), (2,3,7,6), (0,1,5,4))
    createPoly(curr_bm, pos, rot, verts, faces)
    return len(faces)

def createDownUpperGentle(curr_bm, tileGrid, pos, rot):
    verts = [(-0.5,-0.5,0.5), (0.5,-0.5,0.5), (0.5,0.5,0.5), (-0.5,0.5,0.5),(-0.5,-0.5,-0.5), (0.5,-0.5,-0.5), (0.5,0.5,-0.), (-0.5,0.5,-0.), ]
    faces = [(7,6,5,4)]
    renderOuterFaces(faces, pos, tileGrid, None, (0,1,2,3), (5,6,2,1), (0,3,7,4), (6,7,3,2), (4,5,1,0))
    createPoly(curr_bm, pos, rot, verts, faces)
    return len(faces)

def createLowerGentle(curr_bm, tileGrid, pos, rot):
    verts = [(-0.5,-0.5,-0.5), (0.5,-0.5,-0.5), (0.5,0.5,-0.5), (-0.5,0.5,-0.5),(-0.5,-0.5,0.), (0.5,-0.5,0.), (0.5,0.5,-0.5), (-0.5,0.5,-0.5), ]
    faces = [(4,5,2,3)]
    renderOuterFaces(faces, pos, tileGrid, (3,2,1,0), None, (1,2,5), (4,3,0), None, (0,1,5,4))
    #renderOuterFaces(faces, pos, tileGrid, (3,2,1,0), (4,5,6,7), (1,2,6,5), (4,7,3,0), (2,3,7,6), (0,1,5,4))
    createPoly(curr_bm, pos, rot, verts, faces)
    return len(faces)

def createDownLowerGentle(curr_bm, tileGrid, pos, rot):
    verts = [(-0.5,-0.5,0.5), (0.5,-0.5,0.5), (0.5,0.5,0.5), (-0.5,0.5,0.5),(-0.5,-0.5,0.), (0.5,-0.5,0.), (0.5,0.5,0.5), (-0.5,0.5,0.5), ]
    faces = [(3,2,5,4)]
    renderOuterFaces(faces, pos, tileGrid, (0,1,2,3), None, (5,2,1), (0,3,4), None, (4,5,1,0))
    createPoly(curr_bm, pos, rot, verts, faces)
    return len(faces)

def createCube(curr_bm, tileGrid, pos, rot):
    verts = [(-0.5,-0.5,-0.5), (0.5,-0.5,-0.5), (0.5,0.5,-0.5), (-0.5,0.5,-0.5),(-0.5,-0.5,0.5), (0.5,-0.5,0.5), (0.5,0.5,0.5), (-0.5,0.5,0.5), ]
    faces = []
    #my = (0,1,4,5)
    renderOuterFaces(faces, pos, tileGrid, (3,2,1,0), (4,5,6,7), (1,2,6,5), (4,7,3,0), (2,3,7,6), (0,1,5,4))
    createPoly(curr_bm, pos, rot, verts, faces)
    return len(faces)

def createVerticalSlope(curr_bm, tileGrid, pos, rot):
    #try 3,7
    verts = [(-0.5,-0.5,-0.5), (0.5,-0.5,-0.5), (0.5,0.5,-0.5), (-0.5,0.5,-0.5),(-0.5,-0.5,0.5), (0.5,-0.5,0.5), (0.5,0.5,0.5), (-0.5,0.5,0.5), ]
    faces = [(0,4,6,2)]
    renderOuterFaces(faces, pos, tileGrid, (2,1,0), (4,5,6), (1,2,6,5), None, None, (0,1,5,4))
    #renderOuterFaces(faces, pos, tileGrid, (3,2,1,0), (4,5,6,7), (1,2,6,5), (4,7,3,0), (2,3,7,6), (0,1,5,4))
    createPoly(curr_bm, pos, rot, verts, faces)
    return len(faces)

def createVerticalSlab(curr_bm, tileGrid, pos, rot):
    verts = [(-0.5,-0.5,-0.5), (0.5,-0.5,-0.5), (0.5,0.,-0.5), (-0.5,0.,-0.5),(-0.5,-0.5,0.5), (0.5,-0.5,0.5), (0.5,0.,0.5), (-0.5,0.,0.5), ]
    faces = []
    renderOuterFaces(faces, pos, tileGrid, (3,2,1,0), (4,5,6,7), (1,2,6,5), (4,7,3,0), (2,3,7,6), (0,1,5,4))
    createPoly(curr_bm, pos, rot, verts, faces)
    return len(faces)

def createFence(curr_bm, tileGrid, pos, rot):
    verts = [(-0.5,-0.5,-0.5), (0.5,-0.5,-0.5), (0.5,-0.5,-0.5), (-0.5,-0.5,-0.5),(-0.5,-0.5,0.5), (0.5,-0.5,0.5), (0.5,-0.5,0.5), (-0.5,-0.5,0.5), ]
    faces = []
    renderOuterFaces(faces, pos, tileGrid, (3,2,1,0), (4,5,6,7), (1,2,6,5), (4,7,3,0), (2,3,7,6), (0,1,5,4))
    createPoly(curr_bm, pos, rot, verts, faces)
    return len(faces)

def createPole(curr_bm, tileGrid, pos, rot):
    verts = [(0,-0.125,-0.5), (0.125,0,-0.5), (0,0.125,-0.5), (-0.125,0,-0.5),(0,-0.125,0.5), (0.125,0,0.5), (0,0.125,0.5), (-0.125,0,0.5), ]
    faces = []
    renderOuterFaces(faces, pos, tileGrid, (3,2,1,0), (4,5,6,7), (1,2,6,5), (4,7,3,0), (2,3,7,6), (0,1,5,4))
    createPoly(curr_bm, pos, rot, verts, faces)
    return len(faces)

def createBars(curr_bm, tileGrid, pos, rot):
    xHasTile = (pos[0]+1,pos[1],pos[2]) in tileGrid
    mxHasTile = (pos[0]-1,pos[1],pos[2]) in tileGrid
    yHasTile = (pos[0],pos[1]+1,pos[2]) in tileGrid
    myHasTile = (pos[0],pos[1]-1,pos[2]) in tileGrid
    startX = -0.125
    endX = 0.125
    startY = -0.125
    endY = 0.125
    if not (xHasTile and mxHasTile and yHasTile and myHasTile):
        verts = [(-0.125,-0.125,-0.5), (0.125,-0.125,-0.5), (0.125,0.125,-0.5), (-0.125,0.125,-0.5),(-0.125,-0.125,0.5), (0.125,-0.125,0.5), (0.125,0.125,0.5), (-0.125,0.125,0.5), ]
        faces = [(3,2,1,0), (4,5,6,7), (0,1,5,4), (2,3,7,6), (4,7,3,0), (1,2,6,5)]
    if xHasTile or mxHasTile:
        if xHasTile:
            startX = -0.5
        if mxHasTile:
            endX = 0.5
        verts = [(startX,-0.125,-0.5), (endX,-0.125,-0.5), (endX,0.125,-0.5), (startX,0.125,-0.5),(startX,-0.125,0.5), (endX,-0.125,0.5), (endX,0.125,0.5), (startX,0.125,0.5), ]
        faces = [(3,2,1,0), (4,5,6,7), (0,1,5,4), (2,3,7,6), (4,7,3,0), (1,2,6,5)]
    if yHasTile or myHasTile:
        if yHasTile:
            startY = -0.5
        if myHasTile:
            endY = 0.5
        verts += [(-0.125,startY,-0.5), (0.125,startY,-0.5), (0.125,endY,-0.5), (-0.125,endY,-0.5),(-0.125,startY,0.5), (0.125,startY,0.5), (0.125,endY,0.5), (-0.125,endY,0.5), ]
        faces += [(11,10,9,8), (12,13,14,15), (8,9,13,12), (10,11,15,14), (12,15,11,8), (9,10,14,13)]
    createPoly(curr_bm, pos, rot, verts, faces)
    return len(faces)

def createWater(curr_bm, tileGrid, pos, rot):
    verts = [(-0.5,-0.5,-0.5), (0.5,-0.5,-0.5), (0.5,0.5,-0.5), (-0.5,0.5,-0.5),(-0.5,-0.5,0.375), (0.5,-0.5,0.375), (0.5,0.5,0.375), (-0.5,0.5,0.375), ]
    faces = []
    renderOuterFaces(faces, pos, tileGrid, (3,2,1,0), (4,5,6,7), (1,2,6,5), (4,7,3,0), (2,3,7,6), (0,1,5,4))
    createPoly(curr_bm, pos, rot, verts, faces)
    return len(faces)
#flags: bottom right clockwise, repeat for inbetween, then do special ones
# 2-10-7-11-3
# |         |
# 6         4
# |         |
# 1--9-5--8-0
# order: bootom, top, forward, left, back, right
tileCoverFlags = {
     2: [4095,0, 0, 871, 4095, 871], 3: [0,4095,0,3278,4095,3278], 4: [4095,0,883,883,883,883],
     5: [0,4095,3292,3292,3292,3292], 6: [4095,0,0,0,871,871], 7: [0,4095,0,0,3278,3278],
     8: [4095, 0, 4095,4095, 827, 827], 9 : [0, 4095, 4095, 4095, 3229, 3229],
    10: [3278,0,0,0,871,871], 11: [0,3278,0,0,3278,3278], 12: [4095, 0, 4095,4095, 827, 827],
    13: [0, 4095, 4095, 4095, 3229, 3229], 14: [4095,0,883,887,4095,887],
    15: [0,4095,3292,3294,4095,3294], 16: [4095,0,0,867,883,867], 17: [0,4095,0,3276,3292,3276],
    18: [4095, 4095, 4095, 4095, 4095, 4095, 4095], 19: [3278,3278,0,0,4095,4095],
    20: [1766,1766,0, 1766, 4095, 1766], 21: [4095,4095,4095,4095,4095,4095],
    22: [4095, 4095, 4095, 4095, 4095, 4095, 4095], 23: [0,0,0,0,0,0],
    24: [0,0,0,0,0,0], 25: [0,0,4000,4000,4000,4000], 26: [0,0,0,0,0,0]
}

idToCreateTileMesh = {2: createSlope, 3: createDownSlope, 4: createSlab, 5: createDownSlab, 6: createCorner,
    7: createDownCorner, 8: createInvCorner, 9: createDownInvCorner, 10: createSlopedCorner,
    11: createDownSlopedCorner, 12: createInvSlopedCorner, 13: createDownInvSlopedCorner, 14: createUpperGentle,
    15: createDownUpperGentle, 16: createLowerGentle, 17: createDownLowerGentle, 
    18: createCube, 19: createVerticalSlope, 20: createVerticalSlab, 21: lambda: None, 22: createCube, 23: createFence,
    24: createPole, 25: createBars, 26: createWater,
}

themePresets = {0 : {"name": "GENERIC", "mats": [12,44,29,58,104,85,13,20,116,121], "topMats": [0,44,23,59,104,85,8,10,116,121], 
        "topMatsEnabled": [True,False,False,True,False,False,True,True,False,False]}, "pole": 23,
    1 : {"name": "SSL", "mats": [13,45,41,61,73,121,45,12,116,120], "topMats": [8,45,41,61,73,121,100,0,116,120], 
        "topMatsEnabled": [True,False,False,False,False,False,True,True,False,False]}, "pole": 100,
    2 : {"name": "RHR", "mats": [32,46,35,68,79,96,84,123,116,118], "topMats": [42,42,35,68,79,96,68,123,116,118],
        "topMatsEnabled": [True,True,False,False,False,False,True,False,False,False]}, "pole": 84,
    3 : {"name": "HMC", "mats": [15,47,24,78,47,22,108,125,116,120], "topMats": [4,25,24,66,4,4,108,125,116,120],
        "topMatsEnabled": [True,True,False,True,True,True,False,False,False,False]}, "pole": 22,
    4 : {"name": "CASTLE", "mats": [88,51,81,88,106,103,82,99,116,55], "topMats": [60,60,71,102,106,103,71,99,116,55],
        "topMatsEnabled": [True,True,True,True,False,False,True,False,False,False], "pole": 81},
    5 : {"name": "VIRTUAPLEX", "mats": [74,69,13,70,101,131,109,74,116,122], "topMats": [74,69,0,63,101,131,109,10,116,122],
        "topMatsEnabled": [False,False,True,True,False,False,False,True,False,False], "pole": 109},
    6 : {"name": "SNOW", "mats": [20,55,39,57,106,85,130,129,119,116], "topMats": [10,72,39,63,106,85,130,129,119,116],
        "topMatsEnabled": [True,True,False,True,True,False,False,False,False,False], "pole": 57},
    7 : {"name": "BBH", "mats": [52,92,76,52,93,87,75,83,116,107], "topMats": [75,92,86,96,93,87,75,75,116,107], 
        "topMatsEnabled": [True,False,True,True,False,False,False,True,False,False], "pole": 52},
    8 : {"name": "JRB", "mats": [43,56,38,65,90,97,125,30,120], "topMats": [9,56,38,64,91,98,125,30,120],
        "topMatsEnabled": [True,False,False,True,True,True,True,False,False,False], "pole": 109},
    9 : {"name": "RETRO", "mats": [132,133,135,136,137,138,139,140,141,142], "topMats": [132,133,134,136,137,138,139,140,141,142], 
        "topMatsEnabled": [False,False,True,False,False,False,False,False,False,False], "pole": 133},
    10 : None,
    11 : {"name": "MC", "mats": [143,145,146,148,149,150,151,152,154,155], "topMats": [144,145,146,147,149,150,151,152,153,155], 
        "topMatsEnabled": [True,False,False,True,False,False,False,False,True,False], "pole": 148},
}

imbueIdToName = {0: "None", 1: "Star", 2: "3x Coins", 3: "Coin", 4: "Green Coin", 5: "Blue Coin",
    6: "Red Switch", 7: "Blue Switch", 8: "Red Coin", 9: "Star Trigger", 10: "Crowbar", 11: "Bullet Mask",
    12: "Badge"
}

# -------------------------------------------------------------------
#  Operator
# -------------------------------------------------------------------

class ImportMB64(bpy.types.Operator, ImportHelper):
    """Import MB64 Files into Blender"""
    bl_idname = "import_file.mb64"
    bl_label = "Import MB64"
    bl_options = {'REGISTER', 'UNDO'}

    filter_glob: StringProperty(
        default="*.mb64",
        options={'HIDDEN'},
    )

    filepath: StringProperty(subtype='FILE_PATH')

    def execute(self, context):
        self.passNo = 0
        # 1. Read file
        try:
            with open(self.filepath, 'rb') as f:
                mb_header = f.read(10)           # valid file check
                mb_version = f.read(1)[0]
                mb_author = f.read(31)
                mb_piktchr = f.read(64*64*2)
                mb_costume = f.read(1)[0]
                
                self.mb_seq = []
                for i in range(5):
                    self.mb_seq.append(f.read(1))
                
                self.mb_envfx = f.read(1)[0]
                self.mb_theme = f.read(1)[0]
                self.mb_bg = f.read(1)[0]
                self.mb_boundaryMat = f.read(1)[0]
                self.mb_boundary = f.read(1)[0]
                self.mb_boundaryHeight = f.read(1)[0]
                self.mb_coinStar = f.read(1)[0]
                self.mb_size = f.read(1)[0]
                self.mb_waterLevel = f.read(1)[0]
                self.mb_secret = f.read(1)[0]
                self.mb_gameMode = f.read(1)[0]
                self.mb_toolbar = f.read(18)
                self.mb_unknownb1 = f.read(1)[0]
                
                # Convert these two to integers!
                self.mb_tileCount = int.from_bytes(f.read(2), 'big')
                self.mb_objectCount = int.from_bytes(f.read(2), 'big')
                
                self.mb_materials = []
                self.mb_topMaterials = []
                self.mb_topMaterialEnabled = []
                
                for i in range(10):
                    self.mb_materials.append(f.read(1)[0])
                for i in range(10):
                    self.mb_topMaterials.append(f.read(1)[0])
                for i in range(10):
                    self.mb_topMaterialEnabled.append(f.read(1)[0])
                
                self.mb_fence = f.read(1)[0]
                self.mb_pole = f.read(1)[0]
                self.mb_bars = f.read(1)[0]
                self.mb_water = f.read(1)[0]
                self.mb_trajectoryData = f.read(20 * 50 * 4)
                self.mb_padding = f.read(12)
                
                # Now these work because mb_tileCount and mb_objectCount are integers
                self.mb_tileData = f.read(self.mb_tileCount * 4)
                self.mb_objData = f.read(self.mb_objectCount * 8)
        except Exception as e:
            self.report({'ERROR'}, f"Could not read file: {e}")
            return {'CANCELLED'}

        # 2. Parse header (example based on your format)
        fileHeader = mb_header.decode("utf-8")[:9]
        if fileHeader != "MB64-v1.1":
            self.report({'ERROR'}, f"Invalid file header: '{fileHeader}'.")
            return {'CANCELLED'}

        self.report({'INFO'}, f"Loading {self.mb_tileCount} tiles.")

        self.chunks = []
        
        # create level data
        bpy.ops.object.empty_add(type='PLAIN_AXES', radius=1, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        level = bpy.context.active_object
        bpy.context.object.name = "Level"
        bpy.context.object.sm64_obj_type = 'Level Root'
        background = idToBackground[self.mb_bg]
        if background in ["VOID", "NONE"]:
            bpy.context.object.useBackgroundColor = True
        else:
            bpy.context.object.background = background
        
        # create area data as child    
        bpy.ops.object.empty_add(type='PLAIN_AXES', radius=1, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        bpy.context.object.name = "Area"
        bpy.context.object.sm64_obj_type = 'Area Root'
        if self.mb_seq[0] in idToSequence:
            seqType = idToSequence[self.mb_seq[0]]
            bpy.context.object.musicSeqEnum = seqType
        else:
            bpy.context.object.musicSeqEnum = 'Custom'
        bpy.context.object.envOption = idToEnvFX[self.mb_envfx]
        self.area = bpy.context.active_object
        self.area.parent = level
        self.area.matrix_parent_inverse = level.matrix_world.inverted()
        
        # override custom theme
        themeData = themePresets[self.mb_theme]
        if themeData:
            self.mb_materials = themeData["mats"]
            self.mb_topMaterials = themeData["topMats"]
            self.mb_topMaterialEnabled = themeData["topMatsEnabled"]
            self.mb_pole = themeData["pole"]
        
        # Create Materials
        self.materials = []

        # get unique materials update references
        self.uniqueMaterials = []
        for i in range(10):
            if self.mb_materials[i] not in self.uniqueMaterials:
                self.uniqueMaterials.append(self.mb_materials[i])
                self.mb_materials[i] = len(self.uniqueMaterials) - 1
            else:
                self.mb_materials[i] = self.uniqueMaterials.index(self.mb_materials[i])
        for i in range(10):
            if self.mb_topMaterialEnabled[i] != 0:
                if self.mb_topMaterials[i] not in self.uniqueMaterials:
                    self.uniqueMaterials.append(self.mb_topMaterials[i])
                    self.mb_topMaterials[i] = len(self.uniqueMaterials) - 1
                else:
                    self.mb_topMaterials[i] = self.uniqueMaterials.index(self.mb_topMaterials[i])
        
        # precreate final geometry objects
        self.geometry = bpy.data.objects.new(f"MB64 Geometry", bpy.data.meshes.new(f"MB64 Geoemtry"))
        context.collection.objects.link(self.geometry)
        context.view_layer.objects.active = self.geometry
        
        self.matRefs = []

        # materials
        bpy.ops.object.editmode_toggle()
        for i in range(len(self.uniqueMaterials)):
            bpy.ops.object.create_f3d_mat()
            self.matRefs.append(bpy.context.object.active_material)
            matData = idToMatData[self.uniqueMaterials[i]]
            renderToMaterialSetup[matData["render"]]()
            bpy.context.object.active_material.collision_type_simple = matData["surface"]
            bpy.context.object.active_material.f3d_mat.default_light_color = matData["color"]
            bpy.context.object.active_material.name = matData["name"]
        
        #fence material
        bpy.ops.object.create_f3d_mat()
        bpy.context.object.active_material.name = "Fence"
        self.matRefs.append(bpy.context.object.active_material)
        bpy.context.object.active_material.f3d_mat.default_light_color = (0.3804, 0.251, 0.11, 1)
        renderToMaterialSetup["cutout"]()
        #fence material
        bpy.ops.object.create_f3d_mat()
        bpy.context.object.active_material.name = "Pole"
        self.matRefs.append(bpy.context.object.active_material)
        matData = idToMatData[self.mb_pole]
        bpy.context.object.active_material.f3d_mat.default_light_color = matData["color"]
        renderToMaterialSetup[matData["render"]]()
        #bars material
        bpy.ops.object.create_f3d_mat()
        bpy.context.object.active_material.name = "Bars"
        self.matRefs.append(bpy.context.object.active_material)
        renderToMaterialSetup["cutout"]()
        bpy.context.object.active_material.f3d_mat.default_light_color = (0.7059, 0.7059, 0.7059, 1)
        #water material?
        bpy.ops.object.create_f3d_mat()
        bpy.context.object.active_material.name = "Water"
        self.matRefs.append(bpy.context.object.active_material)
        bpy.context.object.active_material.collision_type_simple = "SURFACE_WATER"
        bpy.context.object.active_material.f3d_mat.default_light_color = (0.2471, 0.3294, 0.6745, 1)
        renderToMaterialSetup["transparent"]()
        
        # troll materials
        for i in range(len(self.uniqueMaterials)):
            self.matRefs.append(bpy.context.object.active_material)
            bpy.ops.object.create_f3d_mat()
            matData = idToMatData[self.uniqueMaterials[i]]
            bpy.context.object.active_material.collision_type_simple = "SURFACE_INTANGIBLE"
            bpy.context.object.active_material.f3d_mat.default_light_color = matData["color"]
            bpy.context.object.active_material.name = matData["name"] + " (Intangible)" 
            renderToMaterialSetup[matData["render"]]()
        bpy.ops.object.editmode_toggle()

        # predefine tileGrid
        self.tileGrid = {}

        self.current_index = 0
        wm = context.window_manager
        wm.progress_begin(0, self.mb_tileCount)
        self._timer = wm.event_timer_add(0.01, window=context.window)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        if event.type != 'TIMER':
            return {'PASS_THROUGH'}
        # third pass: create objects & boundary
        if self.passNo == 2:
            # create objects
            chunk_size = 100
            end = min(self.current_index + chunk_size, self.mb_objectCount)
            
            for i in range(self.current_index, end):
                off = i * 8
                bParam = self.mb_objData[off]
                pos = (-self.mb_objData[off+1]+32, self.mb_objData[off+2], self.mb_objData[off+3]-32)
                type = self.mb_objData[off+4]
                rot = self.mb_objData[off+5]
                imbue = self.mb_objData[off+6]
                pad = self.mb_objData[off+7]
                rotation = rotCorrection[rot] * math.pi / 2
                objectName = ""
                bpy.ops.object.empty_add(type='PLAIN_AXES', radius=1, align='WORLD',
                    location=(pos[0], pos[2], pos[1]), scale=(1, 1, 1), rotation=(0,0,rotation))
                currObj = bpy.context.active_object
                if type in idToObjData:
                    objData = idToObjData[type]
                    bpy.context.object.sm64_obj_type = objData["type"]
                    if objData["type"] == 'Object':
                        bpy.context.object.sm64_model_enum = objData["model"]
                        bpy.context.object.sm64_behaviour_enum = objData["behavior"]
                    elif objData["type"] == 'Macro':
                        bpy.context.object.sm64_macro_enum = objData["preset"]
                    bpy.context.object.name = objData["name"]
                    if objData["hasParams"]:
                        objData["paramHandler"](self, objData, bParam)
                else:
                    bpy.context.object.sm64_obj_type = 'None'
                    bpy.context.object.name = f"Unknown Object ID#{type}"
                if imbue > 0:
                    bpy.context.object.name += f"[{imbueIdToName[imbue]}]"
                currObj.parent = self.area
                currObj.matrix_parent_inverse = self.area.matrix_world.inverted()
                
            
            self.current_index = end
            context.window_manager.progress_update(self.current_index)
             
            if self.current_index >= self.mb_objectCount:
                bpy.context.view_layer.objects.active = self.geometry
                self.geometry.select_set(True)
                for mat in self.matRefs:
                    with bpy.context.temp_override(material=mat):
                        bpy.ops.material.update_f3d_nodes()
                
                boundaryBM = bmesh.new()
                doCreateObject = False
                # create boundary planes
                if self.mb_boundary == 0: # void
                    self.createDeathPlane(8)
                    # no ground
                    # no walls
                    # no ceil
                elif self.mb_boundary == 1: # plain
                    # no death
                    self.createGroundPlane(boundaryBM, 0)
                    # no walls
                    # no ceil
                    doCreateObject = True
                elif self.mb_boundary == 1: # valley
                    # no death
                    self.createGroundPlane(boundaryBM, 0)
                    self.createWallPlanes(boundaryBM, -1, 0, self.mb_boudnaryHeight)
                    # no ceil
                    doCreateObject = True
                elif self.mb_boundary == 2: # chasm
                    self.createDeathPlane(0)
                    self.createGroundPlane(boundaryBM, 0)
                    self.createWallPlanes(boundaryBM, -6, self.mb_boundaryHeight)
                    # no ceil
                    doCreateObject = True
                elif self.mb_boundary == 3: #plateau
                    self.createDeathPlane(8)
                    self.createGroundPlane(boundaryBM, -6)
                    self.createWallPlanes(boundaryBM, 1, -6, 0)
                    # no ceil
                    doCreateObject = True
                else: #interior
                    # no death
                    self.createGroundPlane(boundaryBM, 0)
                    self.createWallPlanes(boundaryBM, -1, 0, self.mb_boundaryHeight)
                    self.createCeilingPlane(boundaryBM)
                    doCreateObject = True
                
                if doCreateObject:
                    mesh = bpy.data.meshes.new("BoundaryMesh")
                    boundaryBM.to_mesh(mesh)
                    boundaryBM.free()
                    boundaryObj = bpy.data.objects.new("BoundaryMesh", mesh)
                    bpy.context.collection.objects.link(boundaryObj)
                    slotGround = self.mb_materials[self.mb_boundaryMat]
                    slotTop = self.mb_topMaterials[self.mb_boundaryMat]
                    boundaryObj.data.materials.append(self.geometry.material_slots[slotGround].material)
                    boundaryObj.data.materials.append(self.geometry.material_slots[slotTop].material)
                    boundaryObj.parent = self.area
                    boundaryObj.matrix_parent_inverse = self.area.matrix_world.inverted()
                
                context.window_manager.progress_end()
                context.window_manager.event_timer_remove(self._timer)
                return {'FINISHED'}
        # first pass: create tileDataGrid
        if self.passNo == 0:
            # Process a chunk of tiles (e.g., 100 per frame)
            chunk_size = 100
            end = min(self.current_index + chunk_size, self.mb_tileCount)

            imported_objects = []
            current_bm = bmesh.new()
            
            # tiles
            for i in range(self.current_index, end):
                off = i * 4
                tile_val = int.from_bytes(self.mb_tileData[off:off+4], 'big')
                # Extract fields (big endian, MSB to LSB)
                x = (tile_val >> 26) & 0x3F
                y = (tile_val >> 20) & 0x3F
                z = (tile_val >> 14) & 0x3F
                typ = (tile_val >>  9) & 0x1F
                mat = (tile_val >>  5) & 0x0F
                rot = (tile_val >>  2) & 0x07
                water = (tile_val >>  1) & 0x01
            
                self.tileGrid[(-x+32, z-32, y)] = {"type": typ, "mat": mat, "rot": rot, "water": water}
            
            self.current_index = end
            context.window_manager.progress_update(self.current_index)
            
            if self.current_index >= self.mb_tileCount:
                self.passNo = 1
                self.current_index = 0
                context.window_manager.progress_end()
                wm = context.window_manager
                wm.progress_begin(0, self.mb_objectCount)

        # second pass: generate geometry
        if self.passNo == 1:
            # Process a chunk of tiles (e.g., 100 per frame)
            chunk_size = 100
            end = min(self.current_index + chunk_size, self.mb_tileCount)

            imported_objects = []
            current_bm = bmesh.new()
            
            # tiles
            for i in range(self.current_index, end):
                off = i * 4
                tile_val = int.from_bytes(self.mb_tileData[off:off+4], 'big')
                # Extract fields (big endian, MSB to LSB)
                x = (tile_val >> 26) & 0x3F
                y = (tile_val >> 20) & 0x3F
                z = (tile_val >> 14) & 0x3F
                typ = (tile_val >>  9) & 0x1F
                mat = (tile_val >>  5) & 0x0F
                rot = (tile_val >>  2) & 0x07
                water = (tile_val >>  1) & 0x01
                
                if typ == 21: # cull marker
                    continue
                if typ == 26: # water tile
                    newFaces = idToCreateTileMesh[typ](current_bm, self.tileGrid, (-x+32, z-32, y), rot)
                    for face in current_bm.faces[-newFaces:]:
                        face.material_index = len(self.uniqueMaterials) + 3
                    bpy.ops.object.empty_add(type='PLAIN_AXES', radius=0.5, align='WORLD', location=(-x+32, z-32, y), scale=(1, 1, 1))
                    bpy.context.object.sm64_obj_type = 'Water Box'
                    currObj = bpy.context.active_object
                    currObj.parent = self.area
                    currObj.matrix_parent_inverse = self.area.matrix_world.inverted()
                    continue

                newFaces = idToCreateTileMesh[typ](current_bm, self.tileGrid, (-x+32, z-32, y), rot)
                
                current_bm.faces.ensure_lookup_table()
                generalMatIdx = self.mb_materials[mat]
                topMatIdx = generalMatIdx
                
                current_bm.faces.ensure_lookup_table()
                if self.mb_topMaterialEnabled[mat] != 0:
                    topMatIdx = self.mb_topMaterials[mat]
                    #bmesh.ops.recalc_face_normals(current_bm, faces=current_bm.faces[-newFaces:])
                for face in current_bm.faces[-newFaces:]:
                    if face.normal.dot((0, 0, 1)) > 0.1:
                        face.material_index = topMatIdx
                    else:
                        face.material_index = generalMatIdx
                    # special override
                    if typ == 22: #intangible
                        face.material_index += len(self.uniqueMaterials) + 4
                    if typ == 23: # fence
                        face.material_index = len(self.uniqueMaterials) # fence mat
                    if typ == 24: # pole
                        face.material_index = len(self.uniqueMaterials) + 1 # pole mat
                    if typ == 25: # bars
                        face.material_index = len(self.uniqueMaterials) + 2 # bars mat
                
                # fill position with water if waterlogged
                if water > 0:
                    newFaces = idToCreateTileMesh[26](current_bm, self.tileGrid, (-x+32, z-32, y), rot)
                    for face in current_bm.faces[-newFaces:]:
                        face.material_index = len(self.uniqueMaterials) + 3
                    bpy.ops.object.empty_add(type='PLAIN_AXES', radius=0.5, align='WORLD', location=(-x+32, z-32, y), scale=(1, 1, 1))
                    bpy.context.object.sm64_obj_type = 'Water Box'
                    currObj = bpy.context.active_object
                    currObj.parent = self.area
                    currObj.matrix_parent_inverse = self.area.matrix_world.inverted()
               
                current_bm.faces.ensure_lookup_table()
            #bmesh.ops.recalc_face_normals(current_bm, faces=current_bm.faces)
            mesh = bpy.data.meshes.new(f"MB64 Geoemtry_{len(self.chunks)}")
            current_bm.to_mesh(mesh)
            self.chunks.append(mesh)
            current_bm.free()
            
            self.current_index = end
            context.window_manager.progress_update(self.current_index)
            
            if self.current_index >= self.mb_tileCount:
                self.passNo = 2
                self.current_index = 0
                # Done
                #join
                chunkObj = []
            
                for mesh in self.chunks[0:]:
                    obj = bpy.data.objects.new(f"TempObj", mesh)
                    context.collection.objects.link(obj)
                    chunkObj.append(obj)
                    for slot in self.geometry.material_slots:
                        obj.data.materials.append(slot.material)
                
                for obj in chunkObj:
                    obj.select_set(True)
                self.geometry.select_set(True)
                context.view_layer.objects.active = self.geometry
                bpy.ops.object.join()
                self.geometry = context.active_object
                self.geometry.name = "MB64 Geoemtry" 
                self.geometry.parent = self.area
                self.geometry.matrix_parent_inverse = self.area.matrix_world.inverted()
                self.report({'INFO'}, f"Imported {self.mb_tileCount} tiles")
                context.window_manager.progress_end()
                wm = context.window_manager
                wm.progress_begin(0, self.mb_objectCount)
        return {'PASS_THROUGH'}
    
    def createDeathPlane(self, extraSize):
        # death plane
        bpy.ops.mesh.primitive_plane_add(
            size=1,
            location=(0,0,-10)
        )
        plane = bpy.context.active_object
        size = (self.mb_size * 16 + 32) + extraSize
        plane.scale = (size,size,1)
        plane.name = "MB64 Death Plane"
        bpy.ops.object.create_f3d_mat()
        bpy.ops.object.editmode_toggle()
        bpy.context.object.active_material.f3d_mat.draw_layer.sm64 = '5'
        bpy.context.object.active_material.f3d_mat.combiner1.D_alpha = '0'
        bpy.context.object.active_material.collision_type_simple = "SURFACE_DEATH_PLANE"
        bpy.ops.object.editmode_toggle()
        plane.parent = self.area
        plane.matrix_parent_inverse = self.area.matrix_world.inverted()
    
    def createGroundPlane(self, boundaryBM, offset):
        size = self.mb_size * 16 + 32
        verts = [(size*0.5,-size*0.5,h),(size*0.5,size*0.5,h),(-size*0.5,size*0.5,h),(-size*0.5,-size*0.5,h) ]
        bm_verts = [boundaryBM.verts.new(v) for v in verts]
        boundaryBM.verts.ensure_lookup_table()
        face = boundaryBM.faces.new(bm_verts)
        face.material_index = 1

    def createCeilingPlane(self, boundaryBM):
        size = self.mb_size * 16 + 32
        h = self.mb_boundaryHeight
        verts = [(-size*0.5,-size*0.5,offset), (-size*0.5,size*0.5,offset),(size*0.5,size*0.5,offset),(size*0.5,-size*0.5,offset)]
        bm_verts = [boundaryBM.verts.new(v) for v in verts]
        boundaryBM.verts.ensure_lookup_table()
        face = boundaryBM.faces.new(bm_verts)
        face.material_index = 0

    def createWallPlanes(self, boundaryBM, normalDir, lower, higher):
        vertCount = len(boundaryBM.verts)
        size = self.mb_size * 16 + 32
        verts = [(-size*0.5,-size*0.5,lower), (-size*0.5,size*0.5,lower),(-size*0.5,-size*0.5,higher),(-size*0.5,size*0.5,higher),
            (-size*0.5,-size*0.5,lower), (size*0.5,-size*0.5,lower),(-size*0.5,-size*0.5,higher),(size*0.5,-size*0.5,higher),
            (-size*0.5,size*0.5,lower), (size*0.5,size*0.5,lower),(-size*0.5,size*0.5,higher),(size*0.5,size*0.5,higher),
            (size*0.5,size*0.5,lower), (size*0.5,-size*0.5,lower),(size*0.5,size*0.5,higher),(size*0.5,-size*0.5,higher),
        ]
        if normalDir >= 0:
            faces = [(2,3,1,0),(5,7,6,4),(10,11,9,8),(14,15,13,12)]
        else:
            faces = [(0,1,3,2),(4,6,7,5),(8,9,11,10),(12,13,15,14)]
        for v in verts:
            boundaryBM.verts.new(v)
        boundaryBM.verts.ensure_lookup_table()
        for face in faces:
            verts = [boundaryBM.verts[i+vertCount] for i in face]
            face = boundaryBM.faces.new(verts)
            face.material_index = 0

# -------------------------------------------------------------------
#  Menu Registration
# -------------------------------------------------------------------

def menu_func_import(self, context):
    self.layout.operator(ImportMB64.bl_idname, text="Mario Builder 64 file (.mb64)")

def register():
    bpy.utils.register_class(ImportMB64)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)

def unregister():
    bpy.utils.unregister_class(ImportMyScene)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)

if __name__ == "__main__":
    register()