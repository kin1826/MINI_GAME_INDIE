import pygame
import copy

# players = {
#     1: pygame.Rect(50, 50, 40, 40),
#     2: pygame.Rect(50, 50, 40, 40),
#     3: pygame.Rect(400, 50, 40, 40),
#     4: pygame.Rect(400, 50, 40, 40),
# }

weapon = {
    "Arrow": {
        "image": pygame.image.load("WEAPON/Arrow.png"),
        "count_frame": 1,
        "frame_speed": 100,
        "frame_size": 32,
        "scale_size": None
    },
    "Magic": {
        "image": pygame.image.load("WEAPON/Rocket_Fire_25r.png"),
        "count_frame": 20,
        "frame_speed": 40,
        "frame_size": 150,
        "scale_size": None
    }
}

attack_type = {
    "Melee": {
        "name": "Melee",
        "distance": 0,
        "weapon": None
    },
    "Ranged": {
        "name": "Ranged",
        "distance": 128,
        "speed": 5,
        "weapon": weapon["Arrow"],
    },
    "Magic": {
        "name": "Magic",
        "distance": 192,
        "speed": 4,
        "weapon": weapon["Magic"],
    },
}

figure = {
    # Orc
    "Orc": [
        {
            "name": "Orc",
            "frame_width": 100,
            "frame_height": 100,
            "scale_size": 180,
            "offset_walk_idle": (-10, 5),
            "offset_attack": (-15, 5),
            "offset_hurt": (0, 5),
            "walk_sheet": pygame.image.load("FIGURE/Orc/Orc-Walk.png"),
            "hurt_sheet": pygame.image.load("FIGURE/Orc/Orc-Hurt.png"),
            "idle_sheet": pygame.image.load("FIGURE/Orc/Orc-Idle.png"),
            "attack_sheet": pygame.image.load("FIGURE/Orc/Orc-Attack01.png"),
            "death_sheet": pygame.image.load("FIGURE/Orc/Orc-Death.png"),
            "walk_count_frames": 8,
            "hurt_count_frames": 4,
            "idle_count_frames": 6,
            "attack_count_frames": 6,
            "death_count_frames": 4,
            "walk_speed_frames": 100,
            "hurt_speed_frames": 100,
            "idle_speed_frames": 100,
            "attack_speed_frame": 80,
            "death_speed_frame": 300,
            "speed" : 5,
            "type_attack": attack_type["Melee"],
            "blood": 200,
            "max_blood": 200,
        }
    ],
    # Wizard
    "Wizard": [
        {
            "name": "Wizard",
            "frame_width": 100,
            "frame_height": 100,
            "scale_size": 53,
            "offset_walk_idle": (0, -5),
            "offset_attack": (0, -5),
            "offset_hurt": (0, -5),
            "walk_sheet": pygame.image.load("FIGURE/Wizard/Chr_Wizard_Walk.png"),
            "hurt_sheet": pygame.image.load("FIGURE/Wizard/Chr_Wizard_Hurt.png"),
            "idle_sheet": pygame.image.load("FIGURE/Wizard/Chr_Wizard_Idle.png"),
            "attack_sheet": pygame.image.load("FIGURE/Wizard/Chr_Wizard_Attack.png"),
            "death_sheet": pygame.image.load("FIGURE/Wizard/Chr_Wizard_Death.png"),
            "walk_count_frames": 6,
            "hurt_count_frames": 1,
            "idle_count_frames": 4,
            "attack_count_frames": 3,
            "death_count_frames": 3,
            "walk_speed_frames": 150,
            "hurt_speed_frames": 150,
            "idle_speed_frames": 200,
            "attack_speed_frame": 140,
            "death_speed_frame": 300,
            "speed" : 3,
            "type_attack": attack_type["Magic"],
            "blood": 100,
            "max_blood": 100,
        }
    ],
    # Soldier
    "Soldier": [
        {
            "name": "Soldier",
            "frame_width": 100,
            "frame_height": 100,
            "scale_size": 180,
            "offset_walk_idle": (0, 5),
            "offset_attack": (0, 5),
            "offset_hurt": (0, 5),
            "walk_sheet": pygame.image.load("FIGURE/Soldier/Soldier-Walk.png"),
            "hurt_sheet": pygame.image.load("FIGURE/Soldier/Soldier-Hurt.png"),
            "idle_sheet": pygame.image.load("FIGURE/Soldier/Soldier-Idle.png"),
            "attack_sheet": pygame.image.load("FIGURE/Soldier/Soldier-Attack03.png"),
            "death_sheet": pygame.image.load("FIGURE/Soldier/Soldier-Death.png"),
            "walk_count_frames": 8,
            "hurt_count_frames": 4,
            "idle_count_frames": 6,
            "attack_count_frames": 9,
            "death_count_frames": 4,
            "walk_speed_frames": 150,
            "hurt_speed_frames": 100,
            "idle_speed_frames": 100,
            "attack_speed_frame": 100,
            "death_speed_frame": 300,
            "speed" : 4,
            "type_attack": attack_type["Ranged"],
            "blood": 150,
            "max_blood": 150,
        }
    ],
    "Ghost_black": {
            "name": "Ghost_black",
            "frame_width": 100,
            "frame_height": 100,
            "scale_size": 180,
            "offset_walk_idle": (0, 5),
            "offset_attack": (0, 5),
            "offset_hurt": (0, 5),
            "walk_sheet": pygame.image.load("FIGURE/Ghost_black/Ghost_walk_faster_smallerCanv.png"),
            "hurt_sheet": pygame.image.load("FIGURE/Ghost_black/Ghost_hurt_smallerCanv.png"),
            "idle_sheet": pygame.image.load("FIGURE/Ghost_black/Ghost_idleRedEyes_smalleCanv.png"),
            "attack_sheet": pygame.image.load("FIGURE/Ghost_black/Ghost_attack2_ranged_smallerCanv.png"),
            "death_sheet": pygame.image.load("FIGURE/Ghost_black/Ghost_death_smallerCanv.png"),
            "walk_count_frames": 5,
            "hurt_count_frames": 6,
            "idle_count_frames": 7,
            "attack_count_frames": 9,
            "death_count_frames": 12,
            "walk_speed_frames": 150,
            "hurt_speed_frames": 100,
            "idle_speed_frames": 100,
            "attack_speed_frame": 100,
            "death_speed_frame": 300,
            "speed" : 4,
            "type_attack": attack_type["Magic"],
            "blood": 200,
            "max_blood": 200,
    }
}

players = {
    1: [
        {
            "index": pygame.Rect(50, 50, 40, 40),
            "type_user": "",
            "figure": figure["Orc"],
            "is_injured": False,
            "has_damaged": False,
        }
    ],
    2: [
        {
            "index": pygame.Rect(50, 50, 40, 40),
            "type_user": "",
            "figure": figure["Orc"],
            "is_injured": False,
            "has_damaged": False,
        }
    ],
    3: [
        {
            "index": pygame.Rect(400, 50, 40, 40),
            "type_user": "",
            "figure": figure["Orc"],
            "is_injured": False,
            "has_damaged": False,
        }
    ],
    4: [
        {
            "index": pygame.Rect(10, 450, 40, 40),
            "type_user": "",
            "figure": figure["Soldier"],
        }
    ],
    5: [
        {
            "index": pygame.Rect(10, 450, 40, 40),
            "type_user": "",
            "figure": figure["Wizard"],
        }
    ]
}

backgrounds = {
    1: pygame.image.load("IMG/background/back_lv1.jpg"),
    2: pygame.image.load("IMG/background/back_lv2.png"),
    3: pygame.image.load("IMG/background/back_lv3.png"),
    4: pygame.image.load("IMG/background/back_lv4.jpg"),
    5: pygame.image.load("IMG/background/back_lv5.png"),
}

win_blocks = {
    1: pygame.Rect(600, 420, 50, 50),
    2: pygame.Rect(15, 390, 50, 50),
    3: pygame.Rect(480, 100, 50, 50),
    4: pygame.Rect(10, 229, 50, 50),
    5: pygame.Rect(600, 420, 50, 50),
}

coins_levels = {
    1: [
        {"x": 250, "y": 110, "r": 10, "collected": False},
        {"x": 660, "y": 110, "r": 10, "collected": False},
        {"x": 600, "y": 180, "r": 10, "collected": False},
        {"x": 630, "y": 180, "r": 10, "collected": False},
        {"x": 30, "y": 360, "r": 10, "collected": False},
        {"x": 350, "y": 450, "r": 10, "collected": False},
        {"x": 400, "y": 450, "r": 10, "collected": False},
        {"x": 450, "y": 450, "r": 10, "collected": False},
        {"x": 500, "y": 450, "r": 10, "collected": False},
    ],
    2: [
        {"x": 298, "y": 182, "r": 10, "collected": False},
        {"x": 331, "y": 182, "r": 10, "collected": False},
        {"x": 696, "y": 80, "r": 10, "collected": False},
        {"x": 432, "y": 395, "r": 10, "collected": False},
        {"x": 560, "y": 425, "r": 10, "collected": False},
        {"x": 592, "y": 425, "r": 10, "collected": False},
        {"x": 624, "y": 405, "r": 10, "collected": False},
        {"x": 656, "y": 390, "r": 10, "collected": False},
        {"x": 688, "y": 405, "r": 10, "collected": False},
        {"x": 720, "y": 425, "r": 10, "collected": False},
        {"x": 752, "y": 425, "r": 10, "collected": False},
        {"x": 146, "y": 325, "r": 10, "collected": False},
        {"x": 178, "y": 325, "r": 10, "collected": False},
    ],
    3: [
        {"x": 304, "y": 172, "r": 10, "collected": False},
        {"x": 175, "y": 204, "r": 10, "collected": False},
        {"x": 144, "y": 268, "r": 10, "collected": False},
        {"x": 144, "y": 300, "r": 10, "collected": False},
        {"x": 144, "y": 332, "r": 10, "collected": False},
        {"x": 144, "y": 364, "r": 10, "collected": False},
        {"x": 144, "y": 396, "r": 10, "collected": False},
        {"x": 367, "y": 492, "r": 10, "collected": False},
        {"x": 399, "y": 472, "r": 10, "collected": False},
        {"x": 431, "y": 457, "r": 10, "collected": False},
        {"x": 463, "y": 472, "r": 10, "collected": False},
        {"x": 495, "y": 492, "r": 10, "collected": False},
        {"x": 527, "y": 472, "r": 10, "collected": False},
        {"x": 559, "y": 457, "r": 10, "collected": False},
        {"x": 591, "y": 472, "r": 10, "collected": False},
        {"x": 623, "y": 492, "r": 10, "collected": False},
        {"x": 655, "y": 472, "r": 10, "collected": False},
        {"x": 687, "y": 457, "r": 10, "collected": False},
        {"x": 719, "y": 472, "r": 10, "collected": False},
        {"x": 751, "y": 492, "r": 10, "collected": False},
        {"x": 691, "y": 236, "r": 10, "collected": False},
        {"x": 756, "y": 141, "r": 10, "collected": False},

    ],
    4: [
        {"x": 240, "y": 490, "r": 10, "collected": False},
        {"x": 368, "y": 490, "r": 10, "collected": False},
        {"x": 400, "y": 490, "r": 10, "collected": False},
        {"x": 656, "y": 300, "r": 10, "collected": False},
        {"x": 751, "y": 204, "r": 10, "collected": False},
        {"x": 335, "y": 76, "r": 10, "collected": False},
        {"x": 303, "y": 76, "r": 10, "collected": False},
        {"x": 175, "y": 268, "r": 10, "collected": False},
        {"x": 304, "y": 300, "r": 10, "collected": False},
        {"x": 336, "y": 300, "r": 10, "collected": False},
        {"x": 368, "y": 300, "r": 10, "collected": False},
        {"x": 719, "y": 490, "r": 10, "collected": False},
        {"x": 751, "y": 490, "r": 10, "collected": False},
        {"x": 783, "y": 490, "r": 10, "collected": False},
    ],
    5: [

    ]
}

# Obstacles (đụng thì trừ tim)
obstacles_levels = {
    1: [
        pygame.Rect(150, 100, 30, 30),
        pygame.Rect(600, 100, 30, 30),
        pygame.Rect(300, 305, 20, 20),
        pygame.Rect(100, 350, 30, 30),
        pygame.Rect(416, 320, 384, 20),
        pygame.Rect(200, 430, 50, 50)
    ],
    2: [
        pygame.Rect(130, 130, 30, 30),
        pygame.Rect(378, 180, 100, 20),
        pygame.Rect(187, 170, 30, 30),
        pygame.Rect(217, 170, 30, 30),
        pygame.Rect(668, 190, 30, 30),
        pygame.Rect(668, 280, 128, 20),
        pygame.Rect(640, 420, 30, 30),
        pygame.Rect(128, 430, 169, 20),
        pygame.Rect(320, 355, 30, 30),
    ],
    3: [
        # pygame.Rect(130, 130, 30, 30),
        pygame.Rect(0, 300, 32, 20),
        pygame.Rect(416, 482, 30, 30),
        pygame.Rect(544, 482, 30, 30),
        pygame.Rect(672, 482, 30, 30),
        pygame.Rect(448, 335, 64, 20),
        pygame.Rect(534, 140, 32, 20),
    ],
    4: [
        pygame.Rect(672, 482, 30, 30),
        # pygame.Rect(512, 398, 32, 20),
        pygame.Rect(416, 290, 30, 30),
        pygame.Rect(544, 130, 30, 30),
        pygame.Rect(448, 492, 64, 20),
        pygame.Rect(544, 492, 64, 20),
        pygame.Rect(768, 204, 32, 20),
    ],
    5: [

    ],
}

slime_purple_attacks = {
    1: [],
    2: [],
    3: [
        {
            "index": pygame.Rect(352, 120, 30, 30),
            "blood": 100,
            "max-blood": 100,
            "score": 10,
            "damage": 0,
            "cooldown": 100,
            "last_damage_time": 0,
            "is_injured": False,
            "has_damaged": False,
        },
        {
            "index": pygame.Rect(96, 472, 30, 30),
            "blood": 150,
            "max-blood": 150,
            "score": 15,
            "damage": 0,
            "cooldown": 100,
            "last_damage_time": 0,
            "is_injured": False,
            "has_damaged": False,
        },
        {
            "index": pygame.Rect(96, 185, 30, 30),
            "blood": 120,
            "max-blood": 120,
            "score": 10,
            "damage": 0,
            "cooldown": 100,
            "last_damage_time": 0,
            "is_injured": False,
            "has_damaged": False,
        },
        {
            "index": pygame.Rect(192, 185, 30, 30),
            "blood": 101,
            "max-blood": 101,
            "score": 10,
            "damage": 0,
            "cooldown": 100,
            "last_damage_time": 0,
            "is_injured": False,
            "has_damaged": False,
        },
        {
            "index": pygame.Rect(194, 472, 30, 30),
            "blood": 140,
            "max-blood": 140,
            "score": 15,
            "damage": 0,
            "cooldown": 100,
            "last_damage_time": 0,
            "is_injured": False,
            "has_damaged": False,
        },
        {
            "index": pygame.Rect(290, 472, 30, 30),
            "blood": 160,
            "max-blood": 160,
            "score": 15,
            "damage": 0,
            "cooldown": 100,
            "last_damage_time": 0,
            "is_injured": False,
            "has_damaged": False,
        },
        {
            "index": pygame.Rect(288, 280, 30, 30),
            "blood": 150,
            "max-blood": 150,
            "score": 15,
            "damage": 0,
            "cooldown": 100,
            "last_damage_time": 0,
            "is_injured": False,
            "has_damaged": False,
        },
    ],
    4: [
        {
            "index": pygame.Rect(288, 472, 30, 30),
            "blood": 150,
            "max-blood": 150,
            "score": 15,
            "damage": 30,
            "cooldown": 1600,
            "last_damage_time": 0,
            "is_touching": False,
            "is_injured": False,
            "has_damaged": False,
        },
        {
            "index": pygame.Rect(188, 472, 30, 30),
            "blood": 100,
            "max-blood": 100,
            "score": 15,
            "damage": 10,
            "cooldown": 1600,
            "last_damage_time": 0,
            "is_touching": False,
            "is_injured": False,
            "has_damaged": False,
        },
        {
            "index": pygame.Rect(512, 482, 20, 20),
            "blood": 100,
            "max-blood": 100,
            "score": 10,
            "damage": 10,
            "cooldown": 1600,
            "last_damage_time": 0,
            "is_touching": False,
            "is_injured": False,
            "has_damaged": False,
        },
        {
            "index": pygame.Rect(352, 66, 20, 20),
            "blood": 100,
            "max-blood": 100,
            "score": 15,
            "damage": 10,
            "cooldown": 1600,
            "last_damage_time": 0,
            "is_touching": False,
            "is_injured": False,
            "has_damaged": False,
        },
        {
            "index": pygame.Rect(96, 258, 20, 20),
            "blood": 100,
            "max-blood": 100,
            "score": 15,
            "damage": 10,
            "cooldown": 1600,
            "last_damage_time": 0,
            "is_touching": False,
            "is_injured": False,
            "has_damaged": False,
        },
    ],
    5: [

    ],
}

# Platforms (nhân vật đứng lên được)
platforms_levels = {
    1: [
        pygame.Rect(0, 130, 290, 20),
        pygame.Rect(500, 130, 600, 20),
        pygame.Rect(410, 210, 260, 20),
        pygame.Rect(300, 310, 100, 20),
        pygame.Rect(0, 380, 225, 20),
        pygame.Rect(0, 480, 800, 20),

        pygame.Rect(417, 340, 384, 20),
    ],
    2: [
        pygame.Rect(0, 130, 100, 20),
        pygame.Rect(0, 160, 160, 20),
        pygame.Rect(474, 170, 100, 20),
        pygame.Rect(154, 200, 416, 20),
        pygame.Rect(680, 0, 35, 20),
        pygame.Rect(680, 100, 35, 20),
        pygame.Rect(540, 300, 256, 20),
        pygame.Rect(636, 220, 64, 20),
        pygame.Rect(130, 345, 64, 20),
        pygame.Rect(288, 355, 32, 20),
        pygame.Rect(288, 385, 128, 20),
        pygame.Rect(288, 415, 192, 20),

        pygame.Rect(0, 445, 800, 20),
    ],
    3: [
        pygame.Rect(256, 64, 224, 20),
        pygame.Rect(352, 160, 256, 20),
        pygame.Rect(448, 96, 32, 32),
        pygame.Rect(448, 128, 32, 32),
        pygame.Rect(288, 192, 96, 32),
        pygame.Rect(192, 96, 96, 32),
        pygame.Rect(96, 224, 224, 32),
        pygame.Rect(0, 126, 224, 32),
        pygame.Rect(0, 320, 96, 32),
        pygame.Rect(96, 416, 192, 32),
        pygame.Rect(160, 256, 32, 32),
        pygame.Rect(160, 288, 32, 32),
        pygame.Rect(160, 320, 32, 32),
        pygame.Rect(160, 352, 32, 32),
        pygame.Rect(160, 384, 32, 32),
        pygame.Rect(256, 320, 196, 32),
        pygame.Rect(416, 352, 164, 32),
        pygame.Rect(676, 256, 32, 32),
        pygame.Rect(740, 160, 32, 32),

        pygame.Rect(0, 512, 800, 20),
    ],
    4: [
        pygame.Rect(0, 288, 192, 32),

        pygame.Rect(288, 96, 96, 32),
        pygame.Rect(448, 160, 192, 32),
        pygame.Rect(288, 320, 160, 32),
        pygame.Rect(736, 224, 64, 32),
        pygame.Rect(640, 320, 32, 32),
        pygame.Rect(448, 416, 128, 32),

        pygame.Rect(0, 512, 800, 20),
    ],
    5: [
        pygame.Rect(0, 512, 800, 20),
    ],
}
#
# ghost_base = figure["Ghost_black"].copy()
# # Xoá các surface để tránh lỗi deepcopy
# del ghost_base["walk_sheet"]
# del ghost_base["idle_sheet"]
# del ghost_base["attack_sheet"]
# del ghost_base["hurt_sheet"]
# del ghost_base["death_sheet"]
#
# monsters = {
#     "Ghost_black": [
#         {
#             **ghost_base,
#             "score": 40,
#
#             "is_jumping": False,
#             "jump_force": -10,
#             "vertical_speed": 0,
#             "gravity": 0.5,
#
#             "attack_range": 50,
#             "damage": 15,
#             "cooldown": 1000,
#             "last_attack_time": 0,
#             "is_attacking": False,
#             "attack_frame_index": 0,
#             "attack_frame_speed": 100,
#             "has_damaged": False,
#
#             "injured_timer": 0,
#             "is_injured": False,
#
#             "state": "idle"
#         }
#     ],
#     "Orc": [
#         {
#             **copy.deepcopy(figure["Orc"]),
#             "score": 30,
#
#             "is_jumping": False,
#             "jump_force": -10,
#             "vertical_speed": 0,
#             "gravity": 0.5,
#
#             "attack_range": 50,
#             "damage": 15,
#             "cooldown": 1000,
#             "last_attack_time": 0,
#             "is_attacking": False,
#             "attack_frame_index": 0,
#             "attack_frame_speed": 100,
#             "has_damaged": False,
#
#             "injured_timer": 0,
#             "is_injured": False,
#
#             "state": "idle"
#         }
#     ]
# }
#
# monster_in_levels = {
#     1: [],
#     2: [],
#     3: [],
#     4: [],
#     5: [
#         {
#             **copy.deepcopy(monsters["Ghost_black"][0]),
#             "index": pygame.Rect(300, 400, 40, 60),
#             "start_pos": (300, 400),
#             "patrol_range": (250, 500),
#             "direction": 1,
#             "speed": 2,
#
#             "size_walk": 100,               # quãng đường mỗi lần đi
#             "walked_distance": 0,          # đã đi được bao xa
#             "idle_time": 1000,             # thời gian nghỉ sau khi đi xong
#             "last_idle_time": 0,           # thời gian bắt đầu nghỉ
#
#             "is_dead": False,
#             "death_timer": 0
#         },
#         {
#             **copy.deepcopy(monsters["Orc"][0]),
#             "index": pygame.Rect(300, 400, 40, 60),
#             "start_pos": (300, 400),
#             "patrol_range": (250, 500),
#             "direction": 1,
#             "speed": 2,
#
#             "size_walk": 100,               # quãng đường mỗi lần đi
#             "walked_distance": 0,          # đã đi được bao xa
#             "idle_time": 1000,             # thời gian nghỉ sau khi đi xong
#             "last_idle_time": 0,           # thời gian bắt đầu nghỉ
#
#             "is_dead": False,
#             "death_timer": 0
#         },
#     ],
# }