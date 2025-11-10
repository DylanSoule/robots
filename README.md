# 🚽 Toilet Hero Deluxe

A silly, cinematic Pygame RPG about securing the bathroom, featuring class selection, turn-based combat, floating damage text, and a compelling narrative centered around the most important stall.



## ✨ Features
---
* **Class Selection:** Choose from the **Plumber**, **Gym Bro**, or **Wizard**, each with unique starting stats and gear.
* **Turn-Based Combat:** Engage in battles with enemies like the **Office Worker** and **Bathroom Boss**.
* **Cinematic Transitions:** Includes fade transitions, character slides, and attack animations for a dynamic feel.
* **Floating Text:** Damage, healing, and status changes are displayed with floating text for immediate feedback.
* **Item System:** Use items like the **Energy Drink** or **Plunger of Power** via a clean, popup menu.
* **Specialized Gear:** Each class gains access to unique, stat-boosting items after certain battles.

---

## 🛠️ Installation and Setup
---

This game requires Python and the Pygame library.

### Prerequisites

* Python 3.x
* Pygame library

### Steps

1.  **Clone the Repository (or save the file):**
    Save the provided code as a Python file (e.g., `toilet_hero.py`).

2.  **Install Pygame:**
    Open your terminal or command prompt and run:
    ```bash
    pip install pygame
    ```

3.  **Required Assets (Images):**
    For the game to run correctly, you must have the following image files in the same directory as the Python script. (The script attempts to load these):

    * `bathroom_bg.png` (1280x720 background)
    * `wizard.png`
    * `plumber.png`
    * `gymbro.png`
    * `office_worker.png`
    * `janitor.png`
    * `bathroom_boss.png`
    * `energy_drink.png`
    * `plunger.png`
    * `soap.png`
    * `protein_bar.png`
    * `magic_towel.png`
    * `wrench.png`

    *(Note: The game will crash if these image files are not present.)*

---

## ▶️ How to Play
---

1.  **Run the Game:**
    Open your terminal in the directory where you saved the files and run:
    ```bash
    python toilet_hero.py
    ```

2.  **Character Selection:**
    Select your class (**Plumber**, **Gym Bro**, or **Wizard**) by clicking the corresponding button.

3.  **Combat:**
    The game progresses through three main combat scenarios. In battle, you will see a menu with four options:
    * **Attack:** Deals damage based on your **Strength** and a random roll.
    * **Defend:** Reduces incoming damage from the enemy's attack.
    * **Item:** Opens a popup to use a healing or buff item from your inventory.
    * **Run:** Attempts to escape the battle (random chance).

4.  **Victory:**
    Defeat all enemies to reach the final, crucial choice and become the "Toilet Hero."

---

## ⚙️ Game Mechanics Overview
---

### Classes and Stats

| Class | Strength | Agility | Magic | HP | Starting Item | Special Item |
| :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| **Plumber** | 8 | 5 | 2 | 30 | Plunger of Power | Wrench of Might |
| **Gym Bro** | 10 | 6 | 1 | 25 | Energy Drink | Protein Bar |
| **Wizard** | 3 | 4 | 10 | 20 | Soap of Speed | Magic Towel |

### Items

Items provide temporary buffs for the current battle or instant healing.

| Item | Effect Type | Description |
| :--- | :--- | :--- |
| **Energy Drink** | Healing | Restores 10 HP. |
| **Protein Bar** | Healing | Restores 15 HP (Gym Bro only). |
| **Plunger of Power**| Buff | +3 Strength this battle. |
| **Wrench of Might**| Buff | +5 Strength this battle (Plumber only). |
| **Soap of Speed** | Buff | +3 Agility this battle. |
| **Magic Towel** | Buff | +5 Magic this battle (Wizard only). |

### Combat Formulae (Simplified)

* **Player Attack Damage:** `Player_Strength + random(1 to 6)`
* **Enemy Attack Damage:** `Enemy_Strength + random(1 to 4)`
* **Defend Damage:** `max(0, Enemy_Strength // 2 - random(0 to 3))`