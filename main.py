import json
import yaml

import requests

from EquipmentInput import EquipmentInput
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


# https://rpg-cards.vercel.app/
# Settings:
# - A4
# - Standard, Poker
# - Rounded card corners -> off
# - Default Font Size -> 9px
if __name__ == '__main__':
    output = []
    with open("input.yaml", "r") as stream:
        equipment_list_to_output = EquipmentInput.from_input_list(yaml.safe_load(stream)['equipment'])

    for equipment_to_output in equipment_list_to_output:
        if equipment_to_output.index:
            equipment = requests.get(BASE_URL + '/api/equipment/' + equipment_to_output.index).json()
        elif equipment_to_output.name:
            # search equipment via query parameters
            search_result = requests.get(BASE_URL + '/api/equipment/', params={'name': equipment_to_output.name}).json()
            equipment = requests.get(BASE_URL + search_result['results'][0]['url']).json()
        else:
            continue

        equipment_category = equipment['equipment_category']['index']
        output.append(EQUIPMENT_CATEGORIES[equipment_category](equipment, equipment_to_output.amount))

    output_json = json.dumps(rpgcard_list_to_dict_list(output), indent=4, ensure_ascii=False)
    with open("out.json", "w") as outfile:
        outfile.write(output_json)
