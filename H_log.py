import datetime

def log(text: str, print_text: bool = True):
    with open(r'C:\Users\zianr\OneDrive\Desktop\coding things\python\games\fly_game\save data\log.txt', 'a') as file:
        file.write(f'{datetime.datetime.now()}: {text}\n')

    if print_text:
        print(text)