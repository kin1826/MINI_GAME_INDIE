import pygame
import sys
import lib
import json
import random
import copy

from level_config import win_blocks, coins_levels, obstacles_levels, platforms_levels, backgrounds, players, slime_purple_attacks, figure

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (178, 178, 178)
RED   = (255, 0, 0)
BLUE  = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# image
done_img = pygame.image.load("IMG/done_img.png")
done_img = pygame.transform.scale(done_img, (100, 100))

lock_img = pygame.image.load("IMG/function/lock.png")
lock_img = pygame.transform.scale(lock_img, (40, 40))

level_button_img = pygame.image.load("IMG/function/level_btn.png")
level_button_img = pygame.transform.scale(level_button_img, (120, 100))
level_button_red_img = pygame.image.load("IMG/function/level_btn_red.png")
level_button_red_img = pygame.transform.scale(level_button_red_img, (120, 100))

# sounds
coin_sound = pygame.mixer.Sound("SOUND/coin.wav")
jump_sound = pygame.mixer.Sound("SOUND/jump.wav")
hurt_sound = pygame.mixer.Sound("SOUND/hurt.wav")
win_sound = pygame.mixer.Sound("SOUND/win.wav")
gameover_sound = pygame.mixer.Sound("SOUND/gameover.wav")
monster_injured_sound = pygame.mixer.Sound("SOUND/zb_attacked.mp3")
player_men_injured_sound = pygame.mixer.Sound("SOUND/player_men_injured.mp3")

pygame.mixer.music.load("SOUND/background_music.mp3")  # hoặc .ogg nếu muốn tối ưu
pygame.mixer.music.set_volume(0.1)  # âm lượng nhạc nền (0.0 -> 1.0)
pygame.mixer.music.play(-1)

# fugire
# Sprite sheet walk
walk_sheet = pygame.image.load("FIGURE/Orc/Orc-Walk.png").convert_alpha()
walk_frames = []
frame_width = 100
frame_height = 100

facing_right = False

for i in range(8):  # có 8 frame
    raw_frame = walk_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
    scaled_frame = pygame.transform.scale(raw_frame, (180, 180))

    # Tạo một khung 40x40 trong suốt
    final_frame = pygame.Surface((40, 40), pygame.SRCALPHA)

    # Tính toán vị trí để căn giữa ảnh vào khung
    x = (40 - scaled_frame.get_width()) // 2
    y = (40 - scaled_frame.get_height()) // 2

    # Blit vào khung
    final_frame.blit(scaled_frame, (x - 10, y + 5))

    walk_frames.append(final_frame)

frame_index = 0
animation_timer = 0
animation_speed = 100  # ms

# Sprite sheet hurt
is_blinking = False
blink_frame_index = 0
blink_timer = 0
blink_count = 0

hurt_animation_speed = 0

hurt_sheet = pygame.image.load("FIGURE/Orc/Orc-Hurt.png").convert_alpha()
hurt_frames = []

death_sheet = pygame.image.load("FIGURE/Orc/Orc-Death.png").convert_alpha()
death_frames = []
death_animation_speed = 0

for i in range(4):  # có 4 frame
    raw_frame = hurt_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
    scaled_frame = pygame.transform.scale(raw_frame, (180, 180))

    # Tạo một khung 40x40 trong suốt
    final_frame = pygame.Surface((60, 40), pygame.SRCALPHA)

    # Tính toán vị trí để căn giữa ảnh vào khung
    x = (40 - scaled_frame.get_width()) // 2
    y = (40 - scaled_frame.get_height()) // 2

    # Blit vào khung
    final_frame.blit(scaled_frame, (x + 10, y + 5))

    hurt_frames.append(final_frame)

for i in range(4):  # có 4 frame
    raw_frame = death_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
    scaled_frame = pygame.transform.scale(raw_frame, (180, 180))

    # Tạo một khung 40x40 trong suốt
    final_frame = pygame.Surface((60, 40), pygame.SRCALPHA)

    # Tính toán vị trí để căn giữa ảnh vào khung
    x = (40 - scaled_frame.get_width()) // 2
    y = (40 - scaled_frame.get_height()) // 2

    # Blit vào khung
    final_frame.blit(scaled_frame, (x + 10, y + 5))

    death_frames.append(final_frame)

# Sprite sheet idle
is_idle = True
idle_sheet = pygame.image.load("FIGURE/Orc/Orc-Idle.png").convert_alpha()
idle_frames = []
idle_animation_speed = 0

for i in range(6):  # có 6 frame
    raw_frame = idle_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
    scaled_frame = pygame.transform.scale(raw_frame, (180, 180))

    # Tạo một khung 40x40 trong suốt
    final_frame = pygame.Surface((40, 40), pygame.SRCALPHA)

    # Tính toán vị trí để căn giữa ảnh vào khung
    x = (40 - scaled_frame.get_width()) // 2
    y = (40 - scaled_frame.get_height()) // 2

    # Blit vào khung
    final_frame.blit(scaled_frame, (x - 10, y + 5))

    idle_frames.append(final_frame)

# attack
damage_texts = []

attack_damage = 0
attack_frame_index = 0
attack_animation_timer = 0
attack_animation_speed = 100
last_attack_frame_time = 0

is_attack = False
is_attacked = False
attack_sheet = pygame.image.load("FIGURE/Orc/Orc-Attack01.png").convert_alpha()
attack_frames = []

for i in range(6):  # có 6 frame
    raw_frame = attack_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
    scaled_frame = pygame.transform.scale(raw_frame, (180, 180))

    # Tạo một khung 40x40 trong suốt
    final_frame = pygame.Surface((40, 40), pygame.SRCALPHA)

    # Tính toán vị trí để căn giữa ảnh vào khung
    x = (40 - scaled_frame.get_width()) // 2
    y = (40 - scaled_frame.get_height()) // 2

    # Blit vào khung
    final_frame.blit(scaled_frame, (x, y))

    attack_frames.append(final_frame)


# coin
coin_frame_index = 0
coin_animation_timer = 0
coin_animation_speed = 100  # ms

coin_sheet = pygame.image.load("IMG/coin.png").convert_alpha()
coin_frames = []

coin_height = 16
coin_width = 16

for i in range(12):  # có 6 frame
    raw_frame = coin_sheet.subsurface(pygame.Rect(i * coin_height, 0, coin_height, coin_height))
    scaled_frame = pygame.transform.scale(raw_frame, (30, 30))  # to lên tùy ý

    # Tạo một khung 30x30 trong suốt
    final_frame = pygame.Surface((30, 30), pygame.SRCALPHA)
    final_frame.blit(scaled_frame, (0, 0))

    coin_frames.append(final_frame)

# slime green
slime_frame_index = 0
slime_animation_timer = 0
slime_animation_speed = 100  # ms

slime_sheet = pygame.image.load("IMG/slime_green.png").convert_alpha()
slime_frames = []

slime_height = 24
row = 1  # hàng thứ 2 (chỉ số 1)

for col in range(4):  # có 4 hình trong hàng
    x = col * slime_height
    y = row * slime_height
    raw_frame = slime_sheet.subsurface(pygame.Rect(x, y, slime_height, slime_height))
    scaled_frame = pygame.transform.scale(raw_frame, (50, 50))  # scale nếu muốn
    final_frame = pygame.Surface((30, 30), pygame.SRCALPHA)

    # Tính toán vị trí để căn giữa ảnh vào khung
    x = (30 - scaled_frame.get_width()) // 2
    y = (30 - scaled_frame.get_height()) // 2

    # Blit vào khung
    final_frame.blit(scaled_frame, (x,  y - 8))
    slime_frames.append(final_frame)

# slime purple
slime_attack_frame_index = 0
slime_attack_animation_timer = 0
slime_attack_animation_speed = 250  # ms
slime_attack_blood = 100
slime_damage = 0
slime_last_damage_time = 0
slime_cooldown = 0

slime_attacks = copy.deepcopy(slime_purple_attacks)

slime_attack_sheet = pygame.image.load("IMG/slime_purple.png").convert_alpha()
slime_attack_frames = []
slime_attacked_frames = []
slime_die_frames  = []

slime_attack_height = 24
row = 1  # hàng thứ 2 (chỉ số 1)

for col in range(4):
    x = col * slime_attack_height
    y = row * slime_attack_height
    raw_frame = slime_attack_sheet.subsurface(pygame.Rect(x, y, slime_attack_height, slime_attack_height))
    scaled_frame = pygame.transform.scale(raw_frame, (50, 50))  # scale nếu muốn
    final_frame = pygame.Surface((30, 30), pygame.SRCALPHA)

    # Tính toán vị trí để căn giữa ảnh vào khung
    x = (30 - scaled_frame.get_width()) // 2
    y = (30 - scaled_frame.get_height()) // 2

    # Blit vào khung
    final_frame.blit(scaled_frame, (x,  y - 8))
    slime_attack_frames.append(final_frame)

for col in range(1):
    x = (col + 2) * slime_attack_height
    y = (row + 1) * slime_attack_height
    raw_frame = slime_attack_sheet.subsurface(pygame.Rect(x, y, slime_attack_height, slime_attack_height))
    scaled_frame = pygame.transform.scale(raw_frame, (50, 50))  # scale nếu muốn
    final_frame = pygame.Surface((30, 30), pygame.SRCALPHA)

    # Tính toán vị trí để căn giữa ảnh vào khung
    x = (30 - scaled_frame.get_width()) // 2
    y = (30 - scaled_frame.get_height()) // 2

    # Blit vào khung
    final_frame.blit(scaled_frame, (x,  y - 8))
    slime_attacked_frames.append(final_frame)

for col in range(3):
    x = col * slime_attack_height
    y = (row - 1) * slime_attack_height
    raw_frame = slime_attack_sheet.subsurface(pygame.Rect(x, y, slime_attack_height, slime_attack_height))
    scaled_frame = pygame.transform.scale(raw_frame, (50, 50))  # scale nếu muốn
    final_frame = pygame.Surface((30, 30), pygame.SRCALPHA)

    # Tính toán vị trí để căn giữa ảnh vào khung
    x = (30 - scaled_frame.get_width()) // 2
    y = (30 - scaled_frame.get_height()) // 2

    # Blit vào khung
    final_frame.blit(scaled_frame, (x,  y - 8))
    slime_die_frames.append(final_frame)

# spiket
speket_img = pygame.image.load("IMG/Spikes.png")
speket_img = pygame.transform.scale(speket_img, (32, 20))


# level
level_now = 0
count_level = 6

level_buttons = []

level_done = {}

CONFIG_FILE = "lib/progress.json"

config = {
    "level_done": {
        "1": False,
        "2": False,
        "3": False
    },
    "sound_on": True,
    "music_on": False,
    "high_score": 0
}

# player
player_lv1 = pygame.Rect(0, 0, 0, 0)
start_pos = player_lv1.copy()
figure = []

player_speed = 5

score = 0

type_attack = {}
weapon = {}
weapon_frames = []
projectile = []

# get platform
tileset = pygame.image.load("IMG/world_tileset.png").convert_alpha()

hearts = 5
font_heart = pygame.font.SysFont("Segoe UI Emoji", 20)
font22 = pygame.font.SysFont("comicsans", 22)
font11 = pygame.font.SysFont("comicsans", 11)
font1 = pygame.font.SysFont("comicsans", 30)
font2 = pygame.font.SysFont("comicsans", 60)

clock = pygame.time.Clock()
game_over = False
game_win = False
already_shown_game_over = False
already_shown_game_win = False

# button
play_again_btn = pygame.Rect(0, 0, 0, 0)
setting_btn_image = pygame.image.load("IMG/function/setting_btn.png")
setting_btn_image = pygame.transform.scale(setting_btn_image, (50, 50))
setting_btn = setting_btn_image.get_rect(topleft=(WIDTH - 60, 10))

# setting dashboard
is_setting_open = False
setting_dashboard_image = pygame.image.load("IMG/function/setting_UI/setting_dashboard.png")
setting_btn_music = pygame.image.load("IMG/function/music_btn.png")
setting_btn_music = pygame.transform.scale(setting_btn_music, (55, 55))
setting_btn_music_rect = pygame.Rect(0, 0, 0, 0)
setting_btn_sound = pygame.image.load("IMG/function/sound_btn.png")
setting_btn_sound = pygame.transform.scale(setting_btn_sound, (55, 55))
setting_btn_sound_rect = pygame.Rect(0, 0, 0, 0)
setting_btn_home = pygame.image.load("IMG/function/home_btn.png")
setting_btn_home = pygame.transform.scale(setting_btn_home, (55, 55))
setting_btn_home_rect = pygame.Rect(0, 0, 0, 0)
setting_btn_language = pygame.image.load("IMG/function/setting_UI/language_btn.png")
setting_btn_language = pygame.transform.scale(setting_btn_language, (300, 60))
setting_btn_language_rect = pygame.Rect(0, 0, 0, 0)
setting_btn_about = pygame.image.load("IMG/function/setting_UI/about_btn.png")
setting_btn_about = pygame.transform.scale(setting_btn_about, (300, 60))
setting_btn_about_rect = pygame.Rect(0, 0, 0, 0)
setting_btn_exit = pygame.image.load("IMG/function/setting_UI/exit_btn.png")
setting_btn_exit = pygame.transform.scale(setting_btn_exit, (300, 60))
setting_btn_exit_rect = pygame.Rect(0, 0, 0, 0)

# Nhảy và rơi
is_jumping = False
jump_velocity = -15
gravity = 1
vertical_speed = 0

is_menu_open = True

# Load config từ file
def load_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

# Lưu config vào file
def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)


def get_platform():
    global level_now, tileset

    tile_size = 16
    cols = {
        1: 0,
        2: 2,
        3: 4,
        4: 7,
        5: 4,
    }

    platform_tile = tileset.subsurface(pygame.Rect(cols[level_now] * tile_size, 0, tile_size, tile_size))
    platform_tile = pygame.transform.scale(platform_tile, (tile_size * 2, tile_size * 2))

    return platform_tile

def draw_platform(plat_rect):
    platform_tile = get_platform()
    tile_width = platform_tile.get_width()
    count = plat_rect.width // tile_width
    for i in range(count):
        screen.blit(platform_tile, (plat_rect.x + i * tile_width, plat_rect.y))

def draw_spike(obs_rect):
    tile_width = speket_img.get_width()
    count = obs_rect.width // tile_width
    for i in range(count):
        screen.blit(speket_img, (obs_rect.x + i * tile_width, obs_rect.y))

def load_animation(anim_type, sheet, frame_width, frame_height, count,
                   scale_size=None, offset_walk_idle=None, offset_attack=None, offset_hurt=None):
    frames = []

    # Nếu không truyền scale thì tự scale theo frame gốc
    scale_size = (scale_size, scale_size)

    # if scale_size is None:
    #     scale_size = (frame_width * 1.8, frame_height * 2)

    offset = offset_walk_idle

    # Nếu là hurt → khung Surface rộng hơn để không bị cắt
    is_hurt = anim_type == "death" or anim_type == "attack"
    surface_size = (60, 40) if is_hurt else (40, 40)

    if is_hurt:
        surface_size = (60, 40)
        offset = offset_hurt
    if anim_type == "attack":
        surface_size = (50, 40)
        offset = offset_attack

    for i in range(count):
        sheet_width = sheet.get_width()
        if (i + 1) * frame_width > sheet_width:
            break

        raw_frame = sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
        scaled_frame = pygame.transform.scale(raw_frame, scale_size)

        surface = pygame.Surface(surface_size, pygame.SRCALPHA)

        x = (surface.get_width() - scaled_frame.get_width()) // 2 + offset[0]
        y = (surface.get_height() - scaled_frame.get_height()) // 2 + offset[1]
        surface.blit(scaled_frame, (x, y))

        frames.append(surface)

    return frames

def setup_played(level):
    global walk_frames, hurt_frames, idle_frames, attack_frames, death_frames
    global walk_sheet, hurt_sheet, idle_sheet, attack_sheet, death_sheet
    global frame_width, frame_height, player_lv1
    global animation_speed, hurt_animation_speed, idle_animation_speed, attack_animation_speed, player_speed, type_attack, weapon, weapon_frames, figure, death_animation_speed
    player = players[level][0]  # lấy dict đầu tiên

    player_lv1 = player["index"]
    figure = player["figure"][0]

    frame_width = figure["frame_width"]
    frame_height = figure["frame_height"]
    scale_size = figure["scale_size"]
    offset_walk_idle = figure["offset_walk_idle"]
    offset_attack = figure["offset_attack"]
    offset_hurt = figure["offset_hurt"]

    walk_sheet = figure["walk_sheet"].convert_alpha()
    hurt_sheet = figure["hurt_sheet"].convert_alpha()
    death_sheet = figure["death_sheet"].convert_alpha()
    idle_sheet = figure["idle_sheet"].convert_alpha()
    attack_sheet = figure["attack_sheet"].convert_alpha()

    animation_speed = figure["walk_speed_frames"]
    hurt_animation_speed = figure["hurt_speed_frames"]
    idle_animation_speed = figure["idle_speed_frames"]
    attack_animation_speed = figure["attack_speed_frame"]
    death_animation_speed = figure["death_speed_frame"]

    player_speed = figure["speed"]

    type_attack = figure["type_attack"]
    weapon = type_attack["weapon"]

    if weapon is not None:
        weapon_frames = load_weapon_frames(
            weapon["image"],
            weapon["count_frame"],
            weapon["frame_size"],
            weapon["scale_size"]
        )

    # Load animation từng loại
    walk_frames = load_animation("walk", walk_sheet, frame_width, frame_height,
                                 figure["walk_count_frames"], scale_size, offset_walk_idle, offset_attack, offset_hurt)
    hurt_frames = load_animation("hurt", hurt_sheet, frame_width, frame_height,
                                 figure["hurt_count_frames"], scale_size, offset_walk_idle, offset_attack, offset_hurt)
    idle_frames = load_animation("idle", idle_sheet, frame_width, frame_height,
                                 figure["idle_count_frames"], scale_size, offset_walk_idle, offset_attack, offset_hurt)
    attack_frames = load_animation("attack", attack_sheet, frame_width, frame_height,
                                   figure["attack_count_frames"], scale_size, offset_walk_idle, offset_attack, offset_hurt)
    death_frames = load_animation("death", death_sheet, frame_width, frame_height,
                                 figure["death_count_frames"], scale_size, offset_walk_idle, offset_attack, offset_hurt)

def menu():
    global btn_lv1, btn_lv2, btn_lv3, is_menu_open, level_buttons, config, level_done, slime_attacks
    config = load_config()
    level_done = {int(k): v for k, v in config["level_done"].items()}
    score_user = config["high_score"]
    menu_surface = pygame.Surface(screen.get_size())

    menu_background = pygame.image.load("IMG/background/menu_back.png")
    menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))
    menu_surface.fill(BLACK)
    menu_surface.blit(menu_background, (0, 0))

    title = font2.render("GAME", True, WHITE)
    menu_surface.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))
    score_user_text = font1.render(f"Your score: {score_user}", True, WHITE)
    menu_surface.blit(score_user_text, (WIDTH // 2 - score_user_text.get_width() // 2, 120))

    level_buttons.clear()
    # for i in range(count_level):
    #     btn_x = 60 + i * 140  # khoảng cách giữa các nút
    #     btn_y = 200
    #     btn_width = 120
    #     btn_height = 100
    #
    #     btn_rect = pygame.Rect(btn_x, btn_y, btn_width, btn_height)
    #     level_buttons.append(btn_rect)
    btn_width = 120
    btn_height = 100
    btn_spacing_x = 20  # khoảng cách ngang giữa các nút
    btn_spacing_y = 30  # khoảng cách dọc
    btn_start_x = 60
    btn_start_y = 200

    btn_x = btn_start_x
    btn_y = btn_start_y

    for i in range(count_level):
        # Nếu nút tiếp theo vượt quá chiều ngang (giả sử màn hình WIDTH = 800)
        if btn_x + btn_width > WIDTH:
            btn_x = btn_start_x  # quay lại đầu dòng
            btn_y += btn_height + btn_spacing_y  # xuống dòng mới

        btn_rect = pygame.Rect(btn_x, btn_y, btn_width, btn_height)
        level_buttons.append(btn_rect)

        btn_x += btn_width + btn_spacing_x  # chuyển sang vị trí nút kế tiếp

    for i, btn in enumerate(level_buttons):
        level_index = i + 1

        # Vẽ nền màu theo trạng thái hoàn thành
        if level_done.get(level_index, False):
            menu_surface.blit(level_button_img, (btn.x, btn.y))
        else:
            menu_surface.blit(level_button_red_img, (btn.x, btn.y))

        # Vẽ chữ "Level X"
        text = font1.render(f"Level {level_index}", True, WHITE)
        menu_surface.blit(text, (btn.x + 10, btn.y + 30))

        # Nếu level > 1 và level trước đó chưa hoàn thành => hiển thị khóa
        if level_index > 1 and not level_done.get(level_index - 1, False):
            menu_surface.blit(lock_img, (btn.x, btn.y))  # Căn giữa nút

    screen.blit(menu_surface, (0, 0))

    pygame.display.flip()

def draw(custom_player_img=None):
    global is_attack, attack_frame_index, is_blinking, blink_timer, blink_frame_index, blink_count, blink_repeat, blink_interval, score, figure, is_attacked

    screen.fill(BLACK)
    background_img = pygame.transform.scale(backgrounds[level_now], (WIDTH, HEIGHT))
    screen.blit(background_img, (0, 0))

    platforms_now = platforms_levels[level_now]
    obstacles_now = obstacles_levels[level_now]
    coins_now = coins_levels[level_now]

    for plat in platforms_now:
        # pygame.draw.rect(screen, GREEN, plat)
        draw_platform(plat)
    for obs in obstacles_now:
        if obs.width == obs.height:  # là hình vuông → slime
            # pygame.draw.rect(screen, RED, (obs.x, obs.y, obs.width, obs.height))
            slime_img = slime_frames[slime_frame_index % len(slime_frames)]
            # Scale khớp với obstacle
            slime_img = pygame.transform.scale(slime_img, (obs.width, obs.height))
            screen.blit(slime_img, (obs.x, obs.y))

        else:  # vẫn vẽ hình chữ nhật đỏ
            draw_spike(obs)

    now = pygame.time.get_ticks()

    for slime_purple in slime_attacks.get(level_now, [])[:]:  # copy để tránh lỗi remove
        slime_pp_rect = slime_purple["index"]
        blood = slime_purple["blood"]
        # pygame.draw.rect(screen, RED, slime_pp_rect)

        if blood <= 0:
            score += slime_purple["score"]
            img = slime_die_frames[slime_attack_frame_index % len(slime_die_frames)]
            img = pygame.transform.scale(img, (slime_pp_rect.width + 10, slime_pp_rect.height + 10))
            screen.blit(img, (slime_pp_rect.x, slime_pp_rect.y))
            slime_attacks[level_now].remove(slime_purple)
            continue

        # Kiểm tra bị thương
        is_injured = "injured_timer" in slime_purple and now - slime_purple["injured_timer"] < 300

        if is_injured:
            img = slime_attacked_frames[0]
        else:
            img = slime_attack_frames[slime_attack_frame_index % len(slime_attack_frames)]

        img = pygame.transform.scale(img, (slime_pp_rect.width + 10, slime_pp_rect.height + 10))
        screen.blit(img, (slime_pp_rect.x, slime_pp_rect.y))

        # Thanh máu
        max_blood = slime_purple["max-blood"]
        bar_width = slime_pp_rect.width + 10
        health_ratio = blood / max_blood
        pygame.draw.rect(screen, (80, 80, 80), (slime_pp_rect.x, slime_pp_rect.y - 7, bar_width, 5))
        pygame.draw.rect(screen, (255, 0, 0), (slime_pp_rect.x, slime_pp_rect.y - 7, int(bar_width * health_ratio), 5))

    for s in coins_now:
        if not s["collected"]:
            coin_img = coin_frames[coin_frame_index]
            # Căn giữa ảnh tại điểm (x, y)
            img_rect = coin_img.get_rect(center=(s["x"], s["y"]))
            screen.blit(coin_img, img_rect.topleft)

    pygame.draw.rect(screen, GRAY, win_blocks[level_now])
    screen.blit(done_img, (win_blocks[level_now].x - 30, win_blocks[level_now].y - 25))

    if not game_over:
        # pygame.draw.rect(screen, GRAY, player_lv1)
        if custom_player_img is not None:
            screen.blit(custom_player_img, (player_lv1.x, player_lv1.y))
        else:
            if is_idle:
                img = idle_frames[frame_index % len(idle_frames)]
            else:
                img = walk_frames[frame_index % len(walk_frames)]

            if not facing_right:
                img = pygame.transform.flip(img, True, False)

            screen.blit(img, (player_lv1.x, player_lv1.y))

        player_blood = figure["blood"]
        player_max_blood = figure["max_blood"]
        player_name = figure["name"]

        health_ratio = player_blood / player_max_blood

        # Kích thước thanh máu
        bar_width = player_lv1.width + 10
        bar_height = 6
        bar_x = player_lv1.x - 5
        bar_y = player_lv1.y - 20

        # Vẽ thanh máu nền
        pygame.draw.rect(screen, (80, 80, 80), (bar_x, bar_y, bar_width, bar_height))
        # Vẽ thanh máu thật
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, int(bar_width * health_ratio), bar_height))

        # Vẽ chữ: "Tên || máu hiện tại / tổng"

        blood_text = f"{player_name} | {player_blood}/{player_max_blood}"
        text_surf = font11.render(blood_text, True, (255, 255, 255))

        # Hiển thị text phía trên thanh máu
        text_x = bar_x + (bar_width - text_surf.get_width()) // 2
        text_y = bar_y - 15
        screen.blit(text_surf, (text_x, text_y))

    text = font_heart.render("❤️ " * hearts, True, RED)
    screen.blit(text, (10, 10))

    score_text = font1.render(f"Your score: {score}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))

    screen.blit(setting_btn_image, setting_btn)

    if is_setting_open:
        show_setting()
    pygame.display.flip()

def blink_effect():
    global facing_right

    for frame in death_frames:
        img = frame
        if not facing_right:
            img = pygame.transform.flip(img, True, False)

        screen.blit(img, (player_lv1.x, player_lv1.y))
        pygame.display.flip()
        draw(custom_player_img=img)
        pygame.time.delay(death_animation_speed)

    figure["blood"] = figure["max_blood"]

def attack_effect():
    global facing_right, is_attack

    for frame in attack_frames:
        img = frame
        if not facing_right:
            img = pygame.transform.flip(img, True, False)

        screen.blit(img, (player_lv1.x, player_lv1.y))
        # pygame.display.flip()
        draw(custom_player_img=img)
        pygame.time.delay(100)

    is_attack = False

def show_game_over():
    global game_over
    game_over = True

    screen.fill(BLACK)
    text = font2.render("YOU LOST", True, RED)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 100))
    text_score = font1.render(f"Score: {score}", True, WHITE)
    screen.blit(text_score, (WIDTH // 2 - text_score.get_width() // 2, HEIGHT // 2 - 20))

    btn_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 60)
    pygame.draw.rect(screen, BLUE, btn_rect)
    btn_text = font1.render("Play again", True, WHITE)
    screen.blit(btn_text, (btn_rect.x + 40, btn_rect.y + 15))

    pygame.display.flip()
    return btn_rect

def show_game_win():
    global game_win
    game_win = True

    screen.fill(BLACK)
    text = font2.render("YOU WIN", True, GREEN)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 100))
    text_score = font1.render(f"Score: {score}", True, WHITE)
    screen.blit(text_score, (WIDTH // 2 - text_score.get_width() // 2, HEIGHT // 2 - 20))

    btn_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 60)
    pygame.draw.rect(screen, BLUE, btn_rect)
    btn_text = font1.render("Next", True, WHITE)
    screen.blit(btn_text, (btn_rect.x + 40, btn_rect.y + 15))

    pygame.display.flip()
    return btn_rect

def show_setting():
    global setting_btn_home_rect
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))

    # Vị trí dashboard trên màn hình
    dash_x = WIDTH // 2 - setting_dashboard_image.get_width() // 2
    dash_y = HEIGHT // 2 - setting_dashboard_image.get_height() // 2

    # Lấy kích thước dashboard
    dash_rect = setting_dashboard_image.get_rect()
    dash_width = dash_rect.width
    dash_height = dash_rect.height

    # Các nút nằm giữa dashboard, cách đều nhau
    btn_spacing = 10  # khoảng cách giữa các nút
    btn_y = dash_height // 2 - 107  # theo chiều dọc giữa dashboard

    # Lấy chiều rộng mỗi nút
    btn_w = setting_btn_sound.get_width()
    btn_h = setting_btn_sound.get_height()

    # Tính tổng chiều rộng của cả 3 nút + khoảng cách
    total_w = btn_w * 3 + btn_spacing * 2
    start_x = (dash_width - total_w) // 2  # bắt đầu vẽ từ trái

    # Vẽ các nút lên dashboard
    setting_dashboard_image.blit(setting_btn_sound, (start_x, btn_y))
    setting_dashboard_image.blit(setting_btn_music, (start_x + btn_w + btn_spacing, btn_y))
    setting_dashboard_image.blit(setting_btn_home, (start_x + (btn_w + btn_spacing) * 2, btn_y))
    setting_btn_home_rect = pygame.Rect(
        dash_x + start_x + (btn_w + btn_spacing) * 2,
        dash_y + btn_y,
        setting_btn_home.get_width(),
        setting_btn_home.get_height()
    )

    # Vẽ dashboard lên giữa màn hình
    overlay.blit(setting_dashboard_image,
                 (WIDTH // 2 - setting_dashboard_image.get_width() // 2,
                  HEIGHT // 2 - setting_dashboard_image.get_height() // 2))

    screen.blit(overlay, (0, 0))


def reset_game():
    global player_lv1, hearts, game_over, already_shown_game_over, level_now
    global is_jumping, vertical_speed, already_shown_game_win, game_win, score, slime_attacks
    player_lv1 = start_pos.copy()
    hearts = 5
    game_over = False
    game_win = False
    already_shown_game_over = False
    already_shown_game_win = False
    is_jumping = False
    vertical_speed = 0
    score = 0
    slime_attacks = copy.deepcopy(slime_purple_attacks)
    figure["blood"] = figure["max_blood"]
    for s in coins_levels[level_now]:
        s["collected"] = False

def is_on_platform(rect):
    """Kiểm tra nếu player đứng trên bất kỳ platform nào"""
    rect.y += 1  # kiểm tra dưới chân
    return any(rect.colliderect(p) for p in platforms_levels[level_now])

def load_weapon_frames(sheet, count, frame_size, scale_size=None):
    frames = []
    output_frame_size = (40, 40)

    for i in range(count):
        # 1. Cắt frame từ sprite sheet
        raw_frame = sheet.subsurface(pygame.Rect(i * frame_size, 0, frame_size, frame_size)).copy()

        # 2. Scale nếu có (phóng hình ảnh lên trước)
        if scale_size:
            raw_frame = pygame.transform.scale(raw_frame, scale_size)

        # 3. Tạo khung cố định nhỏ hơn để căn giữa (ví dụ: 40x40)
        centered_surface = pygame.Surface(output_frame_size, pygame.SRCALPHA)
        raw_rect = raw_frame.get_rect(center=(output_frame_size[0] // 2, output_frame_size[1] // 2))
        centered_surface.blit(raw_frame, raw_rect.topleft)

        frames.append(centered_surface)
    return frames

menu()

just_returned_home = False

while True:
    clock.tick(60)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if play_again_btn.collidepoint(mouse_pos):
                reset_game()
                draw()
                continue
        if game_win and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if play_again_btn.collidepoint(mouse_pos):
                reset_game()
                is_menu_open = True
                menu()
                continue
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if is_setting_open:
                if setting_btn_home_rect.collidepoint(mouse_pos):
                    is_setting_open = False
                    reset_game()
                    is_menu_open = True
                    just_returned_home = True
                    menu()


            if setting_btn.collidepoint(mouse_pos):
                is_setting_open = True
                draw()

            # elif is_setting_open:
            #     is_setting_open = False
            #     draw()



            if is_menu_open and not just_returned_home:
                for i, btn in enumerate(level_buttons):
                    level_to_play = i + 1  # Vì level đánh số từ 1

                    # Level 1 luôn chơi được, các level sau cần kiểm tra level trước đã hoàn thành
                    if level_to_play == 1 or level_done.get(level_to_play - 1, False):
                        if btn.collidepoint(mouse_pos):
                            level_now = level_to_play
                            # player_lv1 = players[level_now]
                            setup_played(level_now)
                            start_pos = player_lv1.copy()
                            reset_game()
                            is_menu_open = False
                            draw()
                            break
    just_returned_home = False

    if not game_over and not game_win and not is_menu_open:
        keys = pygame.key.get_pressed()
        dx = 0
        if keys[pygame.K_a]:
            dx -= player_speed
            facing_right = False
        if keys[pygame.K_d]:
            dx += player_speed
            facing_right = True

        is_idle = (dx == 0)

        if dx != 0:
            animation_timer += clock.get_time()
            if animation_timer >= animation_speed:
                animation_timer = 0
                frame_index = (frame_index + 1) % len(walk_frames)

        # Nhảy
        if (keys[pygame.K_w] or keys[pygame.K_SPACE]) and not is_jumping and is_on_platform(player_lv1):
            is_jumping = True
            vertical_speed = jump_velocity
            jump_sound.play()

        # Rơi xuống
        # Rơi / nhảy theo trục Y
        vertical_speed += gravity
        if vertical_speed > 10:
            vertical_speed = 10

        player_lv1.y += vertical_speed

        for plat in platforms_levels[level_now]:
            if player_lv1.colliderect(plat):
                # đang rơi và đụng mặt trên của platform
                if vertical_speed > 0 and player_lv1.bottom - vertical_speed <= plat.top:
                    player_lv1.bottom = plat.top
                    vertical_speed = 0
                    is_jumping = False
                # đang nhảy và đụng đáy platform
                elif vertical_speed < 0 and player_lv1.top - vertical_speed >= plat.bottom:
                    player_lv1.top = plat.bottom
                    vertical_speed = 0
                    is_jumping = False

                elif player_lv1.right > plat.left and player_lv1.left < plat.left:
                    # Đụng cạnh trái platform
                    player_lv1.right = plat.left
                elif player_lv1.left < plat.right and player_lv1.right > plat.right:
                    # Đụng cạnh phải platform
                    player_lv1.left = plat.right

        if keys[pygame.K_f] and not is_attack:
            is_attack = True
            attack_damage = 0
            attack_frame_index = 0
            last_attack_frame_time = pygame.time.get_ticks()

            if type_attack["name"] == "Ranged" or type_attack["name"] == "Magic":
                direction = 1 if facing_right else -1

                proj_size = min(weapon["frame_size"], 36)  # Giới hạn size vật lý
                proj_rect = pygame.Rect(
                    player_lv1.centerx - proj_size // 2,
                    player_lv1.centery - proj_size // 2,
                    proj_size,
                    proj_size
                )

                # proj_rect = pygame.Rect(
                #     player_lv1.centerx - weapon["frame_size"] // 2,
                #     player_lv1.centery - weapon["frame_size"] // 2 + 6,
                #     weapon["frame_size"],
                #     weapon["frame_size"]
                # )

                projectile.append({
                    "rect": proj_rect,
                    "direction": direction,
                    "speed": type_attack["speed"],
                    "range": type_attack["distance"],
                    "start_pos": player_lv1.centerx,
                    "damage": random.randint(20, 40),
                    "frames": weapon_frames.copy(),
                    "frame_index": 0,
                    "last_frame_time": pygame.time.get_ticks(),
                    "frame_speed": weapon["frame_speed"],
                    "has_hit": False,
                    "is_fired": False,
                })

        now = pygame.time.get_ticks()

        # Cập nhật trạng thái va chạm cho slime (trước tất cả)
        for slime in slime_attacks.get(level_now, []):
            slime_rect = slime["index"]

            # Tạo vùng mở rộng thêm 10px mỗi phía
            expanded_rect = slime_rect.inflate(20, 20)  # 10px mỗi bên (trên, dưới, trái, phải)
            slime["is_touching"] = expanded_rect.colliderect(player_lv1)

        # Xử lý tấn công từ slime gây sát thương cho người chơi
        for slime in slime_attacks.get(level_now, []):
            if slime["is_touching"] and slime["damage"] > 0:
                if now - slime.get("last_attack_time", 0) >= slime["cooldown"]:
                    if figure["blood"] > 0:
                        player_men_injured_sound.play()
                        is_attacked = True
                        figure["blood"] = max(0, figure["blood"] - slime["damage"])
                        slime["last_attack_time"] = now
                    if figure["blood"] == 0:
                        if hearts > 0:
                            hearts -= 1
                            hurt_sound.play()
                        blink_effect()
                        player_lv1 = start_pos.copy()
                        is_jumping = False
                        vertical_speed = 0
                        if hearts == 0 and not already_shown_game_over:
                            play_again_btn = show_game_over()
                            already_shown_game_over = True
                            gameover_sound.play()

        for slime_purple in slime_attacks.get(level_now, []):
            slime_purple_rect = slime_purple["index"]
                # ✅ TÁCH riêng xử lý va chạm vật lý (di chuyển) ra
            if player_lv1.colliderect(slime_purple_rect):
                if vertical_speed > 0 and player_lv1.bottom - vertical_speed <= slime_purple_rect.top:
                    player_lv1.bottom = slime_purple_rect.top
                    vertical_speed = 0
                    is_jumping = False
                elif player_lv1.right > slime_purple_rect.left and player_lv1.left < slime_purple_rect.left:
                    player_lv1.right = slime_purple_rect.left
                elif player_lv1.left < slime_purple_rect.right and player_lv1.right > slime_purple_rect.right:
                    player_lv1.left = slime_purple_rect.right

            if is_attack and attack_damage > 0 and not slime_purple["has_damaged"]:
                if type_attack["name"] == "Melee":
                    slime_center = slime_purple_rect.center
                    player_center = player_lv1.center
                    dist_x = abs(player_center[0] - slime_center[0])
                    dist_y = abs(player_center[1] - slime_center[1])

                    if dist_x < 60 and dist_y < 40:
                        if facing_right and abs(player_lv1.right - slime_purple_rect.left) < 10 or \
                                not facing_right and abs(player_lv1.left - slime_purple_rect.right) < 10 or \
                                vertical_speed > 0 and abs(player_lv1.bottom - slime_purple_rect.top) < 5:
                            slime_purple["injured_timer"] = pygame.time.get_ticks()
                            slime_purple["blood"] = max(0, slime_purple["blood"] - attack_damage)
                            slime_purple["has_damaged"] = True

                            damage_texts.append({
                                "text": str(attack_damage),
                                "pos": [slime_purple_rect.x, slime_purple_rect.y - 30],
                                "timer": pygame.time.get_ticks(),
                                "duration": 1000,
                                "velocity": -0.5
                            })

                            monster_injured_sound.play()

        for project in projectile[:]:
            for slime in slime_attacks.get(level_now, []):
                if not project["has_hit"] and project["rect"].colliderect(slime["index"]):
                    slime["blood"] = max(0, slime["blood"] - project["damage"])
                    slime["injured_timer"] = pygame.time.get_ticks()
                    project["has_hit"] = True

                    damage_texts.append({
                        "text": str(project["damage"]),
                        "pos": [slime["index"].x, slime["index"].y - 30],
                        "timer": pygame.time.get_ticks(),
                        "duration": 1000,
                        "velocity": -0.5
                    })

                    monster_injured_sound.play()
                    projectile.remove(project)
                    is_attack = False
                    break


        # Di chuyển ngang
        player_lv1.x += dx

        # Giữ trong màn hình
        if player_lv1.x < 0: player_lv1.x = 0
        if player_lv1.x + player_lv1.width > WIDTH: player_lv1.x = WIDTH - player_lv1.width

        # print("Số text:", len(damage_texts))

        # Va chạm chướng ngại vật
        hit = any(player_lv1.colliderect(obs) for obs in obstacles_levels[level_now])
        if hit:
            if hearts > 0:
                hearts -= 1
                hurt_sound.play()
            figure["blood"] = 0
            blink_effect()
            player_lv1 = start_pos.copy()
            is_jumping = False
            vertical_speed = 0
            if hearts == 0 and not already_shown_game_over:
                play_again_btn = show_game_over()
                already_shown_game_over = True
                gameover_sound.play()
                continue

        if player_lv1.colliderect(win_blocks[level_now]) and not already_shown_game_win:
            level_done[level_now] = True
            config["level_done"] = {str(k): v for k, v in level_done.items()}
            config["high_score"] = config["high_score"] + score
            save_config(config)

            play_again_btn = show_game_win()
            already_shown_game_win = True
            win_sound.play()
            continue

        for s in coins_levels[level_now]:
            if not s["collected"]:
                # Chuyển hình tròn thành hình chữ nhật để check va chạm
                circle_rect = pygame.Rect(s["x"] - s["r"], s["y"] - s["r"], s["r"] * 2, s["r"] * 2)
                if player_lv1.colliderect(circle_rect):
                    s["collected"] = True
                    score += 1
                    coin_sound.play()

        if is_idle:
            animation_timer += clock.get_time()
            if animation_timer >= idle_animation_speed:
                animation_timer = 0
                frame_index = (frame_index + 1) % len(idle_frames)

        coin_animation_timer += clock.get_time()
        if coin_animation_timer >= coin_animation_speed:
            coin_animation_timer = 0
            coin_frame_index = (coin_frame_index + 1) % len(coin_frames)

        slime_animation_timer += clock.get_time()
        if slime_animation_timer >= slime_animation_speed:
            slime_animation_timer = 0
            slime_frame_index = (slime_frame_index + 1) % len(slime_frames)
        slime_attack_animation_timer += clock.get_time()
        if slime_attack_animation_timer >= slime_attack_animation_speed:
            slime_attack_animation_timer = 0
            slime_attack_frame_index = (slime_attack_frame_index + 1) % len(slime_attack_frames)

        custom_attack_img = None
        # draw()
        if is_attack:
            now = pygame.time.get_ticks()
            if now - last_attack_frame_time >= attack_animation_speed:
                last_attack_frame_time = now
                attack_frame_index += 1

                if attack_frame_index == 2:
                    attack_damage = random.randint(25, 50)
                    # Reset "has_damaged" để chuẩn bị gây đòn
                    for slime in slime_attacks.get(level_now, []):
                        slime["has_damaged"] = False
                else:
                    attack_damage = 0  # các frame khác không gây sát thương

                if attack_frame_index >= len(attack_frames):
                    is_attack = False
                    attack_frame_index = 0
                    attack_damage = 0

            # Gán ảnh để hiển thị
            if attack_frame_index < len(attack_frames):
                img = attack_frames[attack_frame_index]
                if not facing_right:
                    img = pygame.transform.flip(img, True, False)
                custom_attack_img = img

        if is_attacked:
            now = pygame.time.get_ticks()
            if now - last_attack_frame_time >= attack_animation_speed:
                last_attack_frame_time = now
                attack_frame_index += 1

                if attack_frame_index >= len(hurt_frames):
                    is_attacked = False
                    attack_frame_index = 0
                    attack_damage = 0

            # Gán ảnh để hiển thị
            if attack_frame_index < len(hurt_frames):
                img = hurt_frames[attack_frame_index]
                if not facing_right:
                    img = pygame.transform.flip(img, True, False)
                custom_attack_img = img

        draw(custom_player_img=custom_attack_img)

        now = pygame.time.get_ticks()
        for project in projectile[:]:
            if not project["is_fired"]:
                if attack_frame_index >= len(attack_frames) - 1:
                    project["is_fired"] = True  # cho phép bay
                else:
                    continue  # chưa tới frame, skip vòng lặp này
            project["rect"].x += project["speed"] * project["direction"]

            # Cập nhật frame ảnh
            if now - project["last_frame_time"] >= project["frame_speed"]:
                project["last_frame_time"] = now
                project["frame_index"] = (project["frame_index"] + 1) % len(project["frames"])

            # Lấy ảnh hiện tại
            img = project["frames"][project["frame_index"]]
            if project["direction"] == -1:
                img = pygame.transform.flip(img, True, False)

            # Vẽ ra màn hình
            # pygame.draw.rect(screen, RED, project["rect"])
            screen.blit(img, project["rect"])

            # Quá tầm thì xóa
            if abs(project["rect"].x - project["start_pos"]) > project["range"]:
                projectile.remove(project)


        now = pygame.time.get_ticks()
        for dt in damage_texts[:]:
            if now - dt["timer"] > dt["duration"]:
                damage_texts.remove(dt)
            else:
                dt["pos"][1] += dt["velocity"]
                surf = font1.render(dt["text"], True, RED)
                screen.blit(surf, dt["pos"])

        pygame.display.flip()