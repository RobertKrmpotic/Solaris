import yaml
import glob

from classes.card import Card
from classes.planet import Planet

def read_yaml_file(full_path:str):
        with open(full_path, 'r') as stream:
            try:
                return yaml.safe_load(stream) 
            except yaml.YAMLError as exc:
                print(exc)

def create_deck_dict( folder_name:str ):
    ''' Creates a dictionary of cards'''
    deck_dict = {}
    files = glob.glob(f"C:/Users/Robert/Downloads/Cheating is learning/Solaris pygame/yamls/{folder_name}/*.yml") 
    for file in files:
        card_dict = read_yaml_file(file)
        for key in card_dict:
            deck_dict[key] = card_dict[key]
    return deck_dict

def create_deck_list(deck_dict:dict, type:str = ""):
    deck_list = []
    for card in deck_dict:
        if type == "planet":
            deck_list.append(Planet(deck_dict[card]))
        else:
            deck_list.append(Card(deck_dict[card]))
    return deck_list