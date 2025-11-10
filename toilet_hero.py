#!/usr/bin/env python3
"""
Toilet Hero Deluxe - Pygame RPG with cinematic transitions
1280x720, left/right battle layout, floating damage/heal text, popup item selection
"""

import pygame
import sys
import random

# ===== Pygame Initialization =====
pygame.init()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Toilet Hero Deluxe")
clock = pygame.time.Clock()

# ===== Colors =====
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
YELLOW = (255, 255, 0)

# ===== Fonts =====
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 60)

# ===== Load and Scale Images =====
def load_and_scale(path, width=None, height=None):
    img = pygame.image.load(path).convert_alpha()
    if width and height:
        img = pygame.transform.smoothscale(img, (width, height))
    return img

bg_img = load_and_scale("bathroom_bg.png", WIDTH, HEIGHT)
wizard_img = load_and_scale("wizard.png", 200, 250)
plumber_img = load_and_scale("plumber.png", 200, 250)
gymbro_img = load_and_scale("gymbro.png", 200, 250)
office_worker_img = load_and_scale("office_worker.png", 200, 250)
janitor_img = load_and_scale("janitor.png", 200, 250)
boss_img = load_and_scale("bathroom_boss.png", 250, 300)

item_images = {
    "Energy Drink": load_and_scale("energy_drink.png", 80, 80),
    "Plunger of Power": load_and_scale("plunger.png", 80, 80),
    "Soap of Speed": load_and_scale("soap.png", 80, 80),
    "Protein Bar": load_and_scale("protein_bar.png", 80, 80),
    "Magic Towel": load_and_scale("magic_towel.png", 80, 80),
    "Wrench of Might": load_and_scale("wrench.png", 80, 80)
}

# ===== Character Classes =====
classes = {
    "Plumber": {"Strength": 8, "Agility": 5, "Magic": 2, "HP": 30, "img": plumber_img, "starting_item": "Plunger of Power"},
    "Gym Bro": {"Strength": 10, "Agility": 6, "Magic": 1, "HP": 25, "img": gymbro_img, "starting_item": "Energy Drink"},
    "Wizard": {"Strength": 3, "Agility": 4, "Magic": 10, "HP": 20, "img": wizard_img, "starting_item": "Soap of Speed"}
}

# ===== Enemies =====
enemies = [
    {"name": "Office Worker", "HP": 15, "Strength": 5, "Magic": 1, "img": office_worker_img},
    {"name": "Janitor", "HP": 20, "Strength": 7, "Magic": 2, "img": janitor_img},
    {"name": "Bathroom Boss", "HP": 30, "Strength": 10, "Magic": 4, "img": boss_img}
]

# ===== Items =====
items = {
    "Energy Drink": {"heal": 10, "desc": "Restores 10 HP."},
    "Plunger of Power": {"buff": 3, "desc": "+3 Strength this battle."},
    "Soap of Speed": {"buff": 3, "desc": "+3 Agility this battle."},
    "Protein Bar": {"heal": 15, "desc": "Restores 15 HP (Gym Bro exclusive)."},
    "Magic Towel": {"buff": 5, "desc": "+5 Magic this battle (Wizard exclusive)."},
    "Wrench of Might": {"buff": 5, "desc": "+5 Strength this battle (Plumber exclusive)."}
}

# ===== Helper Functions =====
def draw_text(text, font, color, x, y):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

def draw_button(rect, text, color=BLUE):
    pygame.draw.rect(screen, color, rect)
    draw_text(text, font, WHITE, rect[0]+10, rect[1]+10)

def wait_for_click():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                return pygame.mouse.get_pos()
        pygame.display.update()
        clock.tick(60)

def draw_hp_bar(x, y, current_hp, max_hp, color=GREEN):
    bar_width = 200
    bar_height = 25
    fill = max(0, (current_hp / max_hp) * bar_width)
    pygame.draw.rect(screen, RED, (x, y, bar_width, bar_height))
    pygame.draw.rect(screen, color, (x, y, fill, bar_height))
    pygame.draw.rect(screen, BLACK, (x, y, bar_width, bar_height), 2)

def attack_animation(attacker_img, start_x, start_y, end_x):
    steps = 10
    delta = (end_x - start_x) / steps
    for i in range(steps):
        screen.fill(WHITE)
        screen.blit(bg_img, (0,0))
        screen.blit(attacker_img, (start_x + delta*i, start_y))
        pygame.display.update()
        pygame.time.delay(25)
    for i in range(steps):
        screen.fill(WHITE)
        screen.blit(bg_img, (0,0))
        screen.blit(attacker_img, (end_x - delta*i, start_y))
        pygame.display.update()
        pygame.time.delay(25)

def floating_text(text, x, y, color, duration=600):
    start_ticks = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_ticks < duration:
        screen.fill(WHITE)
        screen.blit(bg_img, (0,0))
        draw_text(text, font, color, x, y)
        pygame.display.update()
        clock.tick(60)

def fade_transition():
    fade = pygame.Surface((WIDTH, HEIGHT))
    fade.fill(BLACK)
    for alpha in range(0, 255, 25):
        fade.set_alpha(alpha)
        screen.blit(fade, (0,0))
        pygame.display.update()
        pygame.time.delay(20)
    for alpha in range(255, -1, -25):
        fade.set_alpha(alpha)
        screen.blit(fade, (0,0))
        pygame.display.update()
        pygame.time.delay(20)

def slide_enemy_in(enemy_img, start_x, y):
    for offset in range(200, 0, -20):
        screen.fill(WHITE)
        screen.blit(bg_img, (0,0))
        screen.blit(enemy_img, (start_x + offset, y))
        pygame.display.update()
        pygame.time.delay(20)

def slide_player_in(player_img, start_x, y):
    for offset in range(-200, 0, 20):
        screen.fill(WHITE)
        screen.blit(bg_img, (0,0))
        screen.blit(player_img, (start_x + offset, y))
        pygame.display.update()
        pygame.time.delay(20)

# ===== Popup Item Selection =====
def choose_item_popup(inventory):
    popup_width, popup_height = 500, 300
    popup_x = (WIDTH - popup_width) // 2
    popup_y = (HEIGHT - popup_height) // 2
    popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)

    while True:
        # Draw semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        screen.blit(overlay, (0,0))

        # Draw popup background
        pygame.draw.rect(screen, WHITE, popup_rect)
        pygame.draw.rect(screen, BLACK, popup_rect, 3)
        draw_text("Choose an item (Cancel to go back):", font, BLACK, popup_x + 20, popup_y + 20)

        buttons = []
        for i, item in enumerate(inventory):
            rect = pygame.Rect(popup_x + 50, popup_y + 60 + i*50, popup_width - 100, 40)
            pygame.draw.rect(screen, BLUE, rect)
            draw_text(f"{item} - {items[item]['desc']}", font, WHITE, rect.x + 5, rect.y + 5)
            buttons.append((rect, item))

        cancel_rect = pygame.Rect(popup_x + 50, popup_y + 60 + len(inventory)*50, popup_width - 100, 40)
        pygame.draw.rect(screen, RED, cancel_rect)
        draw_text("Cancel", font, WHITE, cancel_rect.x + 5, cancel_rect.y + 5)

        pygame.display.update()
        pos = wait_for_click()
        for rect, item in buttons:
            if rect.collidepoint(pos):
                return item
        if cancel_rect.collidepoint(pos):
            return None

# ===== Character Selection =====
def choose_class():
    while True:
        screen.fill(WHITE)
        draw_text("Choose Your Class", large_font, BLACK, 400, 50)
        buttons = []
        for i, c in enumerate(classes):
            rect = pygame.Rect(150, 150+i*150, 950, 120)
            pygame.draw.rect(screen, BLUE, rect)
            cls_text = f"{c} – Strength: {classes[c]['Strength']} | Agility: {classes[c]['Agility']} | Magic: {classes[c]['Magic']} | HP: {classes[c]['HP']}"
            draw_text(cls_text, font, WHITE, rect.x + 20, rect.y + 20)
            screen.blit(classes[c]['img'], (rect.right - 220, rect.y + 10))
            buttons.append((rect, c))
        pygame.display.update()

        pos = wait_for_click()
        for rect, c in buttons:
            if rect.collidepoint(pos):
                player_data = classes[c].copy()
                inventory = [player_data.pop("starting_item")]
                player_data["img"] = classes[c]["img"]
                return c, player_data, inventory

# ===== Combat System =====
def combat(player, enemy, inventory, max_player_hp, max_enemy_hp):
    slide_enemy_in(enemy["img"], WIDTH-350, HEIGHT-350)
    slide_player_in(player["img"], 100, HEIGHT-350)

    while enemy["HP"] > 0 and player["HP"] > 0:
        screen.fill(WHITE)
        screen.blit(bg_img, (0,0))
        screen.blit(player["img"], (100, HEIGHT-350))
        screen.blit(enemy["img"], (WIDTH-350, HEIGHT-350))
        draw_text(f"{enemy['name']} HP: {enemy['HP']}", font, RED, WIDTH-350, HEIGHT-380)
        draw_text(f"Your HP: {player['HP']}", font, GREEN, 100, HEIGHT-380)
        draw_hp_bar(100, HEIGHT-350, player["HP"], max_player_hp)
        draw_hp_bar(WIDTH-350, HEIGHT-350, enemy["HP"], max_enemy_hp)

        actions = ["Attack", "Defend", "Item", "Run"]
        buttons = []
        for i, act in enumerate(actions):
            rect = pygame.Rect(50, 50+i*70, 250, 50)
            draw_button(rect, act)
            buttons.append((rect, act))
        pygame.display.update()

        action = None
        while not action:
            pos = wait_for_click()
            for rect, act in buttons:
                if rect.collidepoint(pos):
                    action = act

        if action == "Attack":
            attack_animation(player["img"], 100, HEIGHT-350, WIDTH-600)
            dmg = player["Strength"] + random.randint(1,6)
            enemy["HP"] -= dmg
            floating_text(f"-{dmg}", WIDTH-250, HEIGHT-400, RED)

        elif action == "Defend":
            dmg = max(0, enemy["Strength"]//2 - random.randint(0,3))
            player["HP"] -= dmg
            floating_text(f"-{dmg}", 100, HEIGHT-400, RED)

        elif action == "Item":
            if not inventory:
                floating_text("Inventory empty!", 100, HEIGHT-400, RED)
                continue
            chosen_item = choose_item_popup(inventory)
            if chosen_item is None:
                continue
            inventory.remove(chosen_item)
            if chosen_item in item_images:
                screen.blit(item_images[chosen_item], (WIDTH//2-40, HEIGHT//2-40))
                pygame.display.update()
                pygame.time.delay(400)
            if "heal" in items[chosen_item]:
                player["HP"] += items[chosen_item]["heal"]
                if player["HP"] > max_player_hp:
                    player["HP"] = max_player_hp
                floating_text(f"+{items[chosen_item]['heal']}", 100, HEIGHT-400, GREEN)
            elif "buff" in items[chosen_item]:
                if "Strength" in items[chosen_item]["desc"]:
                    player["Strength"] += items[chosen_item]["buff"]
                elif "Agility" in items[chosen_item]["desc"]:
                    player["Agility"] += items[chosen_item]["buff"]
                elif "Magic" in items[chosen_item]["desc"]:
                    player["Magic"] += items[chosen_item]["buff"]
                floating_text(f"+{items[chosen_item]['buff']} {items[chosen_item]['desc'].split()[1]}", 100, HEIGHT-400, YELLOW)

        elif action == "Run":
            if random.randint(1,6) > 3:
                floating_text("Escaped!", 100, HEIGHT-400, YELLOW)
                return True
            else:
                floating_text("Failed to escape!", 100, HEIGHT-400, RED)

        if enemy["HP"] > 0:
            attack_animation(enemy["img"], WIDTH-350, HEIGHT-350, WIDTH-600)
            dmg = enemy["Strength"] + random.randint(1,4)
            player["HP"] -= dmg
            floating_text(f"-{dmg}", 100, HEIGHT-400, RED)

    if player["HP"] <= 0:
        screen.fill(WHITE)
        draw_text("You collapse... The bathroom is lost.", large_font, RED, 150, HEIGHT//2-50)
        pygame.display.update()
        pygame.time.delay(3000)
        pygame.quit()
        sys.exit()

    return False

# ===== Game Areas =====
def haunted_restroom(player, inventory, cls, max_player_hp):
    fade_transition()
    enemy = enemies[0].copy()
    enemy["img"] = office_worker_img
    max_enemy_hp = enemy["HP"]
    combat(player, enemy, inventory, max_player_hp, max_enemy_hp)
    inventory.append("Protein Bar" if cls=="Gym Bro" else "Energy Drink")

def enchanted_stall(player, inventory, cls, max_player_hp):
    fade_transition()
    enemy = enemies[1].copy()
    enemy["img"] = janitor_img
    max_enemy_hp = enemy["HP"]
    combat(player, enemy, inventory, max_player_hp, max_enemy_hp)
    if cls=="Wizard": inventory.append("Magic Towel")
    elif cls=="Plumber": inventory.append("Wrench of Might")
    else: inventory.append("Plunger of Power")

def final_showdown(player, inventory, max_player_hp):
    fade_transition()
    enemy = enemies[2].copy()
    enemy["img"] = boss_img
    max_enemy_hp = enemy["HP"]
    combat(player, enemy, inventory, max_player_hp, max_enemy_hp)

    # Boss choice
    choice_made = False
    while not choice_made:
        screen.fill(WHITE)
        draw_text("Do you [USE] the stall or [WAIT] for others?", font, BLACK, 250, HEIGHT//2-100)
        use_button = pygame.Rect(300, HEIGHT//2, 250, 60)
        wait_button = pygame.Rect(700, HEIGHT//2, 250, 60)
        draw_button(use_button, "USE")
        draw_button(wait_button, "WAIT")
        pygame.display.update()

        pos = wait_for_click()
        if use_button.collidepoint(pos):
            screen.fill(WHITE)
            draw_text("💩 You have achieved glory! You are the Toilet Hero! 💩", font, GREEN, 150, HEIGHT//2-50)
            pygame.display.update()
            # wait for player acknowledgement (click) before proceeding
            wait_for_click()
            choice_made = True
        elif wait_button.collidepoint(pos):
            screen.fill(WHITE)
            draw_text("You waited... someone else took the stall. Game Over.", font, RED, 150, HEIGHT//2-50)
            pygame.display.update()
            # wait for player acknowledgement (click) before proceeding
            wait_for_click()
            choice_made = True

    wait_for_exit()

# ===== Persistent Window =====
def wait_for_exit():
    screen.fill(WHITE)
    draw_text("Thanks for playing Toilet Hero!", large_font, GREEN, 250, HEIGHT//2-50)
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                waiting = False
        clock.tick(60)

# ===== Main Loop =====
def main():
    cls, player, inventory = choose_class()
    max_player_hp = player["HP"]
    haunted_restroom(player, inventory, cls, max_player_hp)
    enchanted_stall(player, inventory, cls, max_player_hp)
    final_showdown(player, inventory, max_player_hp)
    pygame.quit()
    sys.exit()

# ===== Run =====
if __name__ == "__main__":
    main()
