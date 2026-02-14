'''
ok im not using this file cause i made things wayyyyy more complicated than they have to be
look in H_save_data.py for what i did instead
im keeping this file here because the code i wrote here is actually pretty lit
'''
import json
from pathlib import Path

#self-explainatory functions tbh

#gets player data - leave keys as None to get the full dictionary, or specify a key/iterable of keys
#rare python one-liner used
def get_player_data(keys = None) -> dict:
    with open(Path(__file__).parent.__str__() + r'\save data\save_data.json', 'r') as file:
        save_data = json.load(file)
    
    if keys:
        if type(keys) == 'tuple' or type(keys) == 'list':
            return [save_data[key] for key in keys] #chat is this real
        else:
            return save_data[keys]
    
    return save_data

#a cockroach with no braincells could understand this function
#also you should use the set_player_data function instead of this one cause its just better
def save_all_player_data(save_data: dict) -> None:
    with open(Path(__file__).parent.__str__() + r'\save data\save_data.json', 'w') as file:
        json.dump(save_data, file, indent = 4)

#input the key and the value to change it to - leave key as None to replace ALL save data with the value
def set_player_data(key, value) -> None:
    if key:
        save_data = get_player_data()
        save_data[key] = value
        save_all_player_data(save_data)
    else:
        save_all_player_data(value)

#input a key in the save data and a function which updates the value of that key
#eg "update_player_data('money', lambda x: x + 1)""
def update_player_data(key, update):
    value = get_player_data(key)
    value = update(value)
    set_player_data(key, value)

# set_player_data('upgrades', ['among us', 'ohio'])
# update_player_data('upgrades', lambda list: list + ['test'])