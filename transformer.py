import re

EQUIPMENT_COLOR = 'dimgray'


def determine_armor_icon(armor):
    type = armor['Armor Type']
    if type == 'Shield':
        return 'round-shield'
    elif type == 'Heavy Armor':
        return 'breastplate'
    elif type == 'Medium Armor':
        return 'lamellar'
    else:
        return 'leather-armor'


def determine_weapon_icon(weapon):
    type = weapon['Weapon Type']
    damage_type = weapon['Damage'].split()[-1]
    if type == 'Simple Ranged Weapons':
        return 'pocket-bow'
    elif type == 'Martial Ranged Weapons':
        return 'crossbow'
    elif type == 'Martial Melee Weapons':
        if damage_type == 'bludgeoning':
            return 'warhammer'
        if damage_type == 'piercing':
            return 'barbed-spear'
        if damage_type == 'slashing':
            return 'battle-axe'
    elif type == 'Simple Melee Weapons':
        if damage_type == 'bludgeoning':
            return 'bo'
        if damage_type == 'piercing':
            return 'spear-hook'
        if damage_type == 'slashing':
            return 'gladius'
    else:
        return 'mixed-swords'


def make_dmg_bold(text):
    return re.sub('([1-9]+d[0-9]+|[0-9]+) [a-zA-Z]+ damage', '<b>\g<0></b>', text)


def transform_armor(armor):
    out = {
        'count': 1,
        'color': EQUIPMENT_COLOR,
        'title': armor['Armor'],
        'icon': determine_armor_icon(armor),
        'icon_back': determine_armor_icon(armor),
    }

    contents = [
        f"subtitle | {armor['Armor Type']} ({armor['Cost']})",
        "rule",
        f"property | AC | {armor['Armor Class (AC)']}",
        f"property | Weight | {armor['Weight']}",
        f"property | Strength Requirement | {armor['Strength'].lstrip('Str ')}",
        f"property | Stealth | {armor['Stealth']}",
        "rule",
    ]

    if armor['Description'] != '':
        contents.append(f"text | {armor['Description']}")

    contents.append("fill")
    out['contents'] = contents
    return out


def transform_weapon(weapon):
    out = {
        'count': 1,
        'color': EQUIPMENT_COLOR,
        'title': weapon['Name'],
        'icon': determine_weapon_icon(weapon),
        'icon_back': determine_weapon_icon(weapon),
    }

    contents = [
        f"subtitle | {weapon['Weapon Type']} ({weapon['Cost']})",
        "rule",
        f"property | Damage | {weapon['Damage']}",
        f"property | Weight | {weapon['Weight']}",
        f"property | Properties | {weapon['Properties']}",
        "rule",
    ]
    if weapon['Special'] != '':
        contents.append(f"description | {weapon['Name']} | {weapon['Special']}")
        contents.append("rule")

    # Ignore Properties as there is not enough space on the card
    # if len(weapon['Properties']) > 0:
    #     for property in weapon['Properties Dict']:
    #         contents.append(f"description | {property} | {weapon['Properties Dict'][property]}")

    contents.append("fill")
    out['contents'] = contents
    return out


def transform_gear(gear):
    out = {
        'count': 1,
        'color': EQUIPMENT_COLOR,
        'title': gear['Item'],
        'icon': 'swap-bag',
        'icon_back': 'swap-bag',
    }

    contents = []

    subtitle = f"subtitle | Adventuring Gear"
    if gear['Cost'] != '':
        subtitle += f" ({gear['Cost']})"
    contents.append(subtitle)

    contents.extend([
        "rule",
        f"property | Weight | {gear['Weight']}",
        "rule",
    ])

    if gear['Description'] != '':
        contents.append(f"text | {gear['Description']}")

    contents.append("fill")
    out['contents'] = contents
    return out


def transform_tool(tool):
    out = {
        'count': 1,
        'color': EQUIPMENT_COLOR,
        'title': tool['Item'],
        'icon': 'dig-dug',
        'icon_back': 'dig-dug',
    }

    contents = []

    subtitle = f"subtitle | Artisan Tool"
    if tool['Cost'] != '':
        subtitle += f" ({tool['Cost']})"
    contents.append(subtitle)
    contents.append("rule")

    if tool['Weight'] != '':
        contents.append(f"property | Weight | {tool['Weight']}")
        contents.append("rule")

    if tool['Description'] != '':
        contents.append(f"text | {tool['Description']}")

    contents.append("fill")
    out['contents'] = contents
    return out