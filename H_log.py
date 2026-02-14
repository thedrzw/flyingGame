import datetime
from pathlib import Path

def log(text: str, print_text: bool = True):
    with open(Path(__file__).parent.__str__() + r'\save data\log.txt', 'a') as file:
        file.write(f'{datetime.datetime.now()}: {text}\n')

    if print_text:
        print(text)