import json
import re

import requests

import transformer
from RpgCard import RpgCard

BASE_URL = 'https://www.dnd5eapi.co'

EQUPMENT_BLACKLIST = [
]

EQUIPMENT_CATEGORIES = {
    'armor': transformer.transform_armor,
    'weapon': transformer.transform_weapon,
    'adventuring-gear': transformer.transform_gear,
    'tools': transformer.transform_tool,
}

EQUIPMENT_TO_OUTPUT = {
    'Quarterstaff': 1,
    'Clothes, Common': 1,
    'Ink': 1,
    'Backpack': 2,
    'Bedroll': 2,
    'Mess Kit': 2,
    'Tinderbox': 2,
    'Torch': 2,
    'Rations (1 day)': 2,
    'Waterskin': 2,
    'Rope, hempen (50 feet)': 2,
    "Healer's Kit": 2,
    'Component Pouch': 1,
    'Wand': 1,
    'Chain Mail': 1,
    'Greataxe': 1,
    'Handaxe': 1,
    'Shield': 1,
    'Crowbar': 1,
    'Hammer': 1,
    'Piton': 1,
    'Holy Symbol': 1,
    'Holy water (flask)': 1,
    'Menacles': 1,
    'Mirror, steel': 1,
    'Oil (flask)': 1,
    'Warhammer': 1,
}


def apply(fn, arr):
    out = []
    for i in arr:
        out.append(fn(i))
    return out


def rpgcard_list_to_dict_list(cards: list[RpgCard]) -> list[dict]:
    out = []
    for card in cards:
        out.append(card.__dict__)
    return out


def filter_by_equipment_to_output(element: RpgCard):
    if element.title.lower() in (item.lower() for item in EQUIPMENT_TO_OUTPUT):
        return True
    return False


def modify_equipment_count(equipment_arr: list[RpgCard]):
    out = []
    for equipment in equipment_arr:
        if equipment.title in EQUIPMENT_TO_OUTPUT.keys():
            equipment.count = EQUIPMENT_TO_OUTPUT[equipment.title]
        out.append(equipment)
    return out


# https://rpg-cards.vercel.app/
# Settings:
# - A4
# - Standard, Poker
# - Rounded card corners -> off
# - Default Font Size -> 9px
if __name__ == '__main__':
    output = []

    for equipment_category in EQUIPMENT_CATEGORIES:
        equipment_cat_res = requests.get(BASE_URL + '/api/equipment-categories/' + equipment_category)
        for equipment_info_res in equipment_cat_res.json()['equipment']:

            # Exclude all Magic Items
            if re.match('^\/api\/magic\-items\/.+', equipment_info_res['url']) is None:
                # only include specified equipment
                if equipment_info_res['name'].lower() in (item.lower() for item in EQUIPMENT_TO_OUTPUT):
                    equipment = requests.get(BASE_URL + equipment_info_res['url']).json()
                    output.append(EQUIPMENT_CATEGORIES[equipment_category](equipment))

    output = modify_equipment_count(output)
    output_json = json.dumps(rpgcard_list_to_dict_list(output), indent=4, ensure_ascii=False)
    with open("out.json", "w") as outfile:
        outfile.write(output_json)
