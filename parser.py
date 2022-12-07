import pandas as pd
import re

ARMOR_TYPES = [
    'Light Armor',
    'Medium Armor',
    'Heavy Armor',
    'Shield',
]

WEAPON_TYPES = [
    'Simple Melee Weapons',
    'Simple Ranged Weapons',
    'Martial Melee Weapons',
    'Martial Ranged Weapons',
]


def find_content_from_name(dict, name):
    canonicalized_name = re.sub(' \(.+\)$', '', name)
    canonicalized_name = re.sub('^\*(.+)\*$', '\\1', canonicalized_name)
    regex = '^[*]{3}' + canonicalized_name + '\.?[*]{3}'
    for content in dict:
        if type(content) == str and re.match(regex, content, flags=re.IGNORECASE) is not None:
            return re.sub('^[*]{3}.+\.?[*]{3} ', '', content)
    return ''


def parse_armor_list(armor_dict):
    out = []
    for armor_type in ARMOR_TYPES:
        df = pd.DataFrame(armor_dict['Armor List'][armor_type]['table'])
        transposed_dict = df.T.to_dict()
        for key in transposed_dict:
            if armor_type in armor_dict:
                description = find_content_from_name(armor_dict[armor_type]['content'], transposed_dict[key]['Armor'])
                transposed_dict[key]['Description'] = description
            else:
                transposed_dict[key]['Description'] = ''

            transposed_dict[key]['Armor Type'] = armor_type
            out.append(transposed_dict[key])
    return out


def parse_weapon_list(weapon_dict):
    out = []
    for weapon_type in WEAPON_TYPES:
        df = pd.DataFrame(weapon_dict['Weapons List'][weapon_type]['table'])
        transposed_dict = df.T.to_dict()
        for key in transposed_dict:
            transposed_dict[key]['Special'] = ''
            special = find_content_from_name(weapon_dict['Weapon Properties']['Special Weapons']['content'], transposed_dict[key]['Name'])
            if special != '':
                transposed_dict[key]['Special'] = special

            transposed_dict[key]['Properties Dict'] = {}
            for property in transposed_dict[key]['Properties'].split(", "):
                property_description = find_content_from_name(weapon_dict['Weapon Properties']['content'], property)
                if property_description != '':
                    transposed_dict[key]['Properties Dict'][property] = property_description

            transposed_dict[key]['Weapon Type'] = weapon_type
            out.append(transposed_dict[key])
    return out


def parse_gear_list(gear_dict):
    out = []
    df = pd.DataFrame(gear_dict['Adventuring Gear']['table'])
    transposed_dict = df.T.to_dict()
    for key in transposed_dict:
        item_name = re.sub('^\*(.+)\*$', '\\1', transposed_dict[key]['Item'])
        item_name = re.sub(' [0-9]+$', '', item_name)
        transposed_dict[key]['Item'] = item_name

        description = find_content_from_name(gear_dict['content'], item_name)
        transposed_dict[key]['Description'] = description
        out.append(transposed_dict[key])
    return out


def parse_tool_list(tool_dict):
    out = []
    df = pd.DataFrame(tool_dict['content'][00]['table'])
    transposed_dict = df.T.to_dict()
    for key in transposed_dict:
        tool_name = re.sub('^\*(.+)\*$', '\\1', transposed_dict[key]['Item'])
        tool_name = re.sub(' [0-9]+$', '', tool_name)
        transposed_dict[key]['Item'] = tool_name

        description = find_content_from_name(tool_dict['content'], tool_name)
        transposed_dict[key]['Description'] = description
        out.append(transposed_dict[key])
    return out