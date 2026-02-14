import json
from pathlib import Path

#a cockroach with no braincells could understand these functions

def load_save_data() -> dict:
    with open(Path(__file__).parent.__str__() + r'\save data\save_data.json', 'r') as file:
        save_data = json.load(file)
    
    return save_data

def save_game(save_data: dict) -> None:
    with open(Path(__file__).parent.__str__() + r'\save data\save_data.json', 'w') as file:
        json.dump(save_data, file, indent = 4)


#just do 'save_data = load_save_data()' at the beginning of all the scripts and 'save_game(save_data)' at the end