import re

from RpgCard import RpgCard

MEDIUM_ARMOR = 'Medium'
HEAVY_ARMOR = 'Heavy'
SHIELD = 'Shield'

WEAPON_RANGE_MELEE = 'Melee'
WEAPON_RANGE_RANGED = 'Ranged'

WEAPON_CATEGORY_SIMPLE = 'Simple'
WEAPON_CATEGORY_MARTIAL = 'Martial'

DMG_TYPE_SLASHING = 'slashing'
DMG_TYPE_PIERCING = 'piercing'
DMG_TYPE_BLUDGEONING = 'bludgeoning'


def determine_armor_icon(armor):
    type = armor['armor_category']
    if type == SHIELD:
        return 'round-shield'
    elif type == HEAVY_ARMOR:
        return 'breastplate'
    elif type == MEDIUM_ARMOR:
        return 'lamellar'
    else:
        return 'leather-armor'


def determine_weapon_icon(weapon):
    weapon_range = weapon['weapon_range']
    weapon_category = weapon['weapon_category']
    damage_type = weapon['damage']['damage_type']['index'] if weapon.get('damage') else None

    if weapon_range == WEAPON_RANGE_RANGED:
        if weapon_category == WEAPON_CATEGORY_SIMPLE:
            return 'pocket-bow'
        elif weapon_category == WEAPON_CATEGORY_MARTIAL:
            return 'crossbow'
    elif weapon_range == WEAPON_RANGE_MELEE:
        if weapon_category == WEAPON_CATEGORY_SIMPLE:
            if damage_type == DMG_TYPE_BLUDGEONING:
                return 'bo'
            if damage_type == DMG_TYPE_PIERCING:
                return 'spear-hook'
            if damage_type == DMG_TYPE_SLASHING:
                return 'gladius'
        elif weapon_category == WEAPON_CATEGORY_MARTIAL:
            if damage_type == DMG_TYPE_BLUDGEONING:
                return 'warhammer'
            if damage_type == DMG_TYPE_PIERCING:
                return 'barbed-spear'
            if damage_type == DMG_TYPE_SLASHING:
                return 'battle-axe'
    else:
        return 'mixed-swords'


def parse_equipment_properties_str(equipment: dict) -> str:
    out = []
    for prop in equipment['properties']:
        prop_str = prop['name']
        if prop['index'] == 'thrown':
            prop_str += f" (range {equipment['throw_range']['normal']}/{equipment['throw_range']['long']})"
        if prop['index'] == 'versatile':
            prop_str += f" ({equipment['two_handed_damage']['damage_dice']})"
        out.append(prop_str)
    return ', '.join(out)


def make_dmg_bold(text):
    return re.sub('([1-9]+d[0-9]+|[0-9]+) [a-zA-Z]+ damage', '<b>\g<0></b>', text)


def transform_armor(armor, amount: int = 1) -> RpgCard:
    out = RpgCard()
    out.count = amount
    out.title = armor['name']
    out.icon = determine_armor_icon(armor)
    out.icon_back = determine_armor_icon(armor)

    armor_category = f"{armor['armor_category']} {armor['equipment_category']['name'] if armor['armor_category'] != SHIELD else ''}"

    armor_class = ''
    if armor['armor_category'] == SHIELD:
        armor_class += f"+"
    armor_class += f"{armor['armor_class']['base']}"
    if armor['armor_class']['dex_bonus']:
        armor_class += ' + Dex modifier'

    stealth_disadvantage = '-'
    if armor['stealth_disadvantage']:
        stealth_disadvantage = 'Disadvantage'

    str_minimum = '-'
    if armor['str_minimum'] != 0:
        str_minimum = armor['str_minimum']

    out.contents = [
        f"subtitle | {armor_category} ({armor['cost']['quantity']} {armor['cost']['unit']})",
        "rule",
        f"property | AC | {armor_class}",
        f"property | Weight | {armor['weight']} lb.",
        f"property | Strength Requirement | {str_minimum}",
        f"property | Stealth | {stealth_disadvantage}",
    ]

    if armor['properties']:
        out.append_content(f"property | Properties | {parse_equipment_properties_str(armor)}")

    out.append_content("rule")

    if armor['desc']:
        for entry in armor['desc']:
            out.append_content(f"text | {entry}")

    out.append_content("fill")
    return out


def transform_weapon(weapon, amount: int = 1) -> RpgCard:
    out = RpgCard()
    out.count = amount
    out.color = 'FireBrick'
    out.title = weapon['name']
    out.icon = determine_weapon_icon(weapon)
    out.icon_back = determine_weapon_icon(weapon)

    subtitle = f"{weapon['weapon_category']} {weapon['weapon_range']} Weapon"
    subtitle += f" ({weapon['cost']['quantity']} {weapon['cost']['unit']})"
    out.append_content(f"subtitle | {subtitle}")
    out.append_content("rule")

    if weapon.get('damage'):
        out.append_content(
            f"property | Damage | {weapon['damage']['damage_dice']} {weapon['damage']['damage_type']['index']}")

    out.append_content(f"property | Weight | {weapon['weight']} lb.")

    if weapon['properties']:
        out.append_content(f"property | Properties | {parse_equipment_properties_str(weapon)}")

    out.append_content("rule")

    if weapon['special']:
        out.append_content(f"description | {weapon['name']} | {weapon['special'][0]}")
        out.append_content("rule")

    # if len(weapon['Properties']) > 0:
    #    for property in weapon['Properties Dict']:
    #        if re.match('^Ammunition.*', property, flags=re.IGNORECASE) is None:
    #            contents.append(f"description | {property} | {weapon['Properties Dict'][property]}")

    if weapon['desc']:
        for entry in weapon['desc']:
            out.append_content(f"text | {entry}")

    out.append_content("fill")
    return out


def transform_gear(gear, amount: int = 1) -> RpgCard:
    out = RpgCard()
    out.count = amount
    out.title = gear['name']
    out.icon = 'swap-bag'
    out.icon_back = 'swap-bag'

    subtitle = f"subtitle | Adventuring Gear"
    if gear['cost']:
        subtitle += f" ({gear['cost']['quantity']} {gear['cost']['unit']})"
    out.append_content(subtitle)

    weight = '-'
    if gear.get('weight'):
        weight = f"{gear['weight']} lb."

    out.extend_content([
        "rule",
        f"property | Weight | {weight}",
        "rule",
    ])

    if gear['desc']:
        for entry in gear['desc']:
            out.append_content(f"text | {entry}")

    out.append_content("fill")
    return out


def transform_tool(tool, amount: int = 1) -> RpgCard:
    out = RpgCard()
    out.count = amount
    out.title = tool['name']
    out.icon = 'dig-dug'
    out.icon_back = 'dig-dug'

    subtitle = f"subtitle | Artisan Tool"
    if tool['cost']:
        subtitle += f" ({tool['cost']['quantity']} {tool['cost']['unit']})"
    out.append_content(subtitle)
    out.append_content("rule")

    weight = '-'
    if tool.get('weight'):
        weight = f"{tool['weight']} lb."
    out.append_content(f"property | Weight | {weight}")
    out.append_content("rule")

    if tool['desc']:
        for entry in tool['desc']:
            out.append_content(f"text | {entry}")

    out.append_content("fill")
    return out
