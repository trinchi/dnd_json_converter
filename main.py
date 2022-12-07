import json

import parser
import transformer


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


def filter_by_equipment_to_output(element):
    if element['title'].lower() in (item.lower() for item in EQUIPMENT_TO_OUTPUT):
        return True
    return False


def modify_equipment_count(equipment_arr):
    out = []
    for equipment in equipment_arr:
        if equipment['title'] in EQUIPMENT_TO_OUTPUT.keys():
            equipment['count'] = EQUIPMENT_TO_OUTPUT[equipment['title']]
        out.append(equipment)
    return out

if __name__ == '__main__':
    output = []

    with open('./dnd-5e-srd/json/04 equipment.json') as json_file:
        equipment_data = json.load(json_file)

        armor_list = parser.parse_armor_list(equipment_data['Equipment']['Armor'])
        output.extend(apply(transformer.transform_armor, armor_list))

        weapon_list = parser.parse_weapon_list(equipment_data['Equipment']['Weapons'])
        output.extend(apply(transformer.transform_weapon, weapon_list))

        gear_list = parser.parse_gear_list(equipment_data['Equipment']['Adventuring Gear'])
        output.extend(apply(transformer.transform_gear, gear_list))

        tool_list = parser.parse_tool_list(equipment_data['Equipment']['Tools']['Tools'])
        output.extend(apply(transformer.transform_tool, tool_list))

        # only include specified equipment
        output = list(filter(filter_by_equipment_to_output, output))

        # change count by specified value
        output = modify_equipment_count(output)

        output_json = json.dumps(output, indent=4, ensure_ascii=False)
        with open("out.json", "w") as outfile:
            outfile.write(output_json)
