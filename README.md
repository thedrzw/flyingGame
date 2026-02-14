# Unnamed Flying Game

A Flappy Bird inspired game written using PyGame in Python. It is currently unfinished.

## Description

The gameplay works similar to Flappy Bird: the player can move around in different directions and must dodge walls coming at them. In later levels, enemies are introduced, which shoot bullets that must be dodged. There is also a skill tree in which players can buy upgrades, allowing them to beat later levels.

## Images

Gameplay in level 3:
- health and time bars can be seen towards the bottom
- the red square is the player
- the purple square is an enemy
![image of gameplay](assets/screenshots/gameplay.png)

<br><br>

Level select screen:
- stars change once levels are compeleted
- descriptions for levels appear when hovering
![image of level select](assets/screenshots/levelSelect.png)

<br><br>

Skill tree
- each node on the tree can be purchased for in-game currency
- descriptions for the tree appear when hovering
![image of skill tree](assets/screenshots/skillTree.png)

## Custom Systems

The PyGame module in Python has a very limited amount of tools for building games, meaning that almost everything you see in the game has been created from scratch.

- **Sprites**: all sprites were custom-made by me; you can find these in the `assets` directory

- **Importing System**: custom importing system for importing fonts and sprites from files into the game (see `H_imports.py`)

- **Save Data and Logging**: custom save system and logging (see `H_log.py` and `H_save_data.py`)

- **Event Handling**: custom event handler (see `H_event_handler.py`)

Additionally, there are also many other custom helper files used in this project: all files that begin with `H` are helpers. Files that start with `S` or `L` are files for menu screens or gameplay levels respectively.

## How to Play

Dependencies: Python 3.12.2+ and PyGame 2.5.2+<br>
Simply download this repository and run the main.py file to play!<br>
- Use the W, A, and D keys to move
- Press escape while in a level to exit it, and escape while on the home screen to quit the game
- Press 1 on the menus to switch between the skill tree and level select screens