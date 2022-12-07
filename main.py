import json

import parser
import transformer


def apply(fn, arr):
    out = []
    for i in arr:
        out.append(fn(i))
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

        output_json = json.dumps(output, indent=4, ensure_ascii=False)
        with open("out.json", "w") as outfile:
            outfile.write(output_json)
