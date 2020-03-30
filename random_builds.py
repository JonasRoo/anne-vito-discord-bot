from typing import Dict, List

from collections import Counter
from pprint import pprint
import json
import random
import copy

import pandas as pd


# the default join char for rendering lists as strings
JOIN_CHAR = ' | '

def load_data():

	# ---------------------------- CHAMPIONS ----------------------------
	CHAMPIONS_FILE_PATH = r'C:\Users\Jonas\Desktop\dev\ironnovator-bot\DDRAGON\champions.json'

	with open(CHAMPIONS_FILE_PATH, 'r', encoding='utf-8') as champions_file:
	    champions_raw_data = json.load(champions_file)
	champions = pd.DataFrame(champions_raw_data['data']).transpose()

	# ---------------------------- ITEMS ----------------------------
	ITEMS_FILE_PATH = r'C:\Users\Jonas\Desktop\dev\build_randomizer\DDRAGON\items.json'

	with open(ITEMS_FILE_PATH, 'r', encoding='utf-8') as items_file:
	    items_raw_data = json.load(items_file)
	items = pd.DataFrame(items_raw_data['data']).transpose()

	list_cols = ['from', 'into']
	for col in list_cols:
	    items[col] = items[col].apply(lambda x: x if isinstance(x, list) else [])

	# list of all 'end' items
	full_items = items[items.apply(
	    # is not precursor to any other item
	    lambda r: (len(r['into']) == 0) &
	    # is not champion specific
	    (pd.isna(r['requiredChampion'])) &
	    # is not an Ornn item
	    (pd.isna(r['requiredAlly'])) &
	    # is not a consumable
	    (pd.isna(r['consumed'])) &
	    # is not a consumable alternate notation
	    ('Consumable' not in r['tags']) &
	    # is not a boots item
	    ('Boots' not in r['tags']) &
	    # is not a trinket item
	    ('Trinket' not in r['tags']) &
	    # is a valid item on summoner's rift
	    (r['maps']['11']) &
	    # item is not a doran's item
	    (not 'doran' in r['name'].lower()) &
	    # also no cull
	    (r['name'].lower() != 'cull') &
	    (not 'quick charge' in r['name'].lower()),
	    axis=1)]

	boots = items.loc[items.apply(lambda r: ('Boots' in r['tags']) &
                              (len(r['into']) == 0),
                              axis=1)]

	trinkets = items.loc[items.apply(lambda r: ('Trinket' in r['tags']) &
                                 (pd.isna(r['requiredChampion']) &
                                  (r['maps']['11']) &
                                  (r['gold']['base'] == 0)),
                                 axis=1)]

	# ---------------------------- ITEMS ----------------------------
	SUM_SPELLS_FILE_PATH = r'C:\Users\Jonas\Desktop\dev\build_randomizer\DDRAGON\summoner_spells.json'

	with open(SUM_SPELLS_FILE_PATH, 'r', encoding='utf-8') as ss_file:
	    ss_raw_data = json.load(ss_file)
	summoner_spells = pd.DataFrame(ss_raw_data['data']).transpose()

	return (champions, items, full_items, boots, trinkets, summoner_spells)

def get_random_item_set(is_jungle: bool = False) -> Dict[str, str]:
    item_set = {}
    item_set['boots'] = random.choice(boots.name)
    item_set['full_items'] = random.sample(list(set(full_items.name)), 5)
    if is_jungle:
        if not any(['Enchantment' in item for item in items]):
            # There is currently no jungle item in our item set
            # so we need to replace one of the full items with a jungle item
            jungle_items = full_items.loc[full_items.name.str.contains('enchantment', case=False)]
            jungle_item_choice = random.choice(jungle_items.name)
            item_set['full_items'][random.randint(0, 4)] = jungle_item_choice
    item_set['full_items'] = JOIN_CHAR.join(item_set['full_items'])
    item_set['trinket'] = random.choice(trinkets.name)

    return item_set


def get_random_summoner_spells(game_mode: str = 'CLASSIC', is_jungle: bool = False) -> str:
    ss_mode_subsample = summoner_spells.loc[summoner_spells.modes.apply(
        lambda l: game_mode in l)]
    if is_jungle:
        jungle_choices = list(ss_mode_subsample.name)
        jungle_choices.remove('Smite')
        ss_choice = random.sample(jungle_choices, 1)
        ss_choice.append('Smite')
    else:
        ss_choice = random.sample(list(ss_mode_subsample.name), 2)

    return JOIN_CHAR.join(ss_choice)


VALID_LANE_CHOICES = ['TOP', 'JUNGLE', 'MID',
                      'ADC', 'SUPPORT', 'FILL',
                      'ROAMING']

def get_random_lane() -> str:
    return random.choice(VALID_LANE_CHOICES)


ABILITY_SYMBOLS = ['Q', 'W', 'E']

def get_max_order() -> str:
    max_order = ABILITY_SYMBOLS
    random.shuffle(max_order)
    return ' > '.join(max_order)


RUNES = {
    'Precision': {
        'keystones': ['Press the Attack', 'Lethal Tempo', 'Fleet Footwork'],
        'level_one': ['Overheal', 'Triumph', 'Presence of Mind'],
        'level_two': ['Legend: Alacrity', 'Legend: Tenacity', 'Legend: Bloodline'],
        'level_three': ['Coup de Grace', 'Last Stand', 'Cut Down'],
    },
    'Domination': {
        'keystones': ['Predator', 'Dark Harvest', 'Electrocute'],
        'level_one': ['Cheapshot', 'Taste of Blood', 'Sudden Impact'],
        'level_two': ['Zombie Ward', 'Ghost Poro', 'Eyeball Collection'],
        'level_three': ['Ravenous Hunter', 'Ingenious Hunter', 'Relentless Hunter', 'Ultimate Hunter'],
    },
    'Sorcery': {
        'keystones': ['Arcane Comet', 'Summon Aery', 'Phase Rush'],
        'level_one': ['Nullifying Orb', 'Manaflow Band', 'Nimbus Cloak'],
        'level_two': ['Transcendence', 'Celerity', 'Absolute Focus'],
        'level_three': ['Scorch', 'Waterwalking', 'Gathering Storm'],
    },
    'Resolve': {
        'keystones': ['Grasp of the Undying', 'Aftershock', 'Guardian'],
        'level_one': ['Demolish', 'Font of Life', 'Shield Bash'],
        'level_two': ['Conditioning', 'Second Wind', 'Bone Plating'],
        'level_three': ['Overgrowth', 'Revitalize', 'Unflinching'],
    },
    'Inspiration': {
        'keystones': ['Prototype: Omnistone', 'Glacial Augment', 'Unsealed Spellbook'],
        'level_one': ['Hextech Flashtraption', 'Magical Footwear', 'Perfect Timing'],
        'level_two': ['Future\'s Market', 'Minion Dematerializer', 'Biscuit Delivery'],
        'level_three': ['Cosmic Insight', 'Approach Velocity', 'Time Warp Tonic'],
    },
    
}

STAT_MODIFIER = {
    'offence': ['Adaptive Force', 'Attack Speed', 'CDR'],
    'flex': ['Adaptive Force', 'Armor', 'Magic Resist'],
    'defense': ['Health', 'Armor', 'Magic Resist'],
}


LEVELS = ['level_one', 'level_two', 'level_three']

def get_random_champ() -> str:
    full_champion_names = champions.index + ', ' + champions.title
    return random.choice(full_champion_names)

def coinflip_kayn_form() -> bool:
    return random.choice(['Red', 'Blue'])


def get_runes() -> Dict[str, str]:
    rune_copy = copy.deepcopy(RUNES)
    primary_tree = random.choice(list(rune_copy.keys()))
    primary_runes = rune_copy.pop(primary_tree)
    
    secondary_tree = random.choice(list(rune_copy.keys()))
    secondary_runes = rune_copy[secondary_tree]
    secondary_runes.pop('keystones')
    # eliminate one random level for secondary tree
    secondary_runes.pop(random.choice(LEVELS))
    
    rune_choices = {}
    rune_choices['primaries'] = get_choices_from_dict(primary_runes, join_char=' > ')
    rune_choices['secondaries'] = get_choices_from_dict(secondary_runes, join_char=' > ')
    rune_choices['stat_modifier'] = get_choices_from_dict(STAT_MODIFIER, join_char=JOIN_CHAR)
    
    return rune_choices


def get_choices_from_dict(dc: Dict[str, List[str]], join_char: str = None) -> List[str]:
    choices = []
    for _, v in dc.items():
        choices.append(random.choice(v))
        
    return join_char.join(choices) if join_char else choices


def generate_random_loadout(game_mode: str = 'CLASSIC',
                           champion_prechoice: str = None,
                           lane_prechoice: str = None) -> Dict[str, str]:
    loadout = {}
    if champion_prechoice:
        champ = champions.loc[champions.name.str.contains(champion_prechoice.lower(), case=False)]
        assert len(champ) == 1, f'Champion prechoice {champion_prechoice} invalid!'
        loadout['champion'] = ', '.join([champ.name.iloc[0], champ.title.iloc[0]])
    else:
        loadout['champion'] = champion_prechoice or get_random_champ()
    if loadout['champion'].startswith('Kayn'):
        loadout['champion'] = loadout['champion'] + f'[{coinflip_kayn_form()}]'
    loadout['lane'] = lane_prechoice or get_random_lane()
    # Case: the lane is jungle
    loadout['items'] = get_random_item_set(
        is_jungle=loadout['lane'].upper() == 'JUNGLE')
    # Case: a jungle item (e.g. Enchantment: Bloodrazor) was randomly generated > we need smite
    is_jungle_build = 'Enchantment' in loadout['items']['full_items'] \
                        or loadout['lane'].upper() == 'JUNGLE'
    loadout['summoner_spells'] = get_random_summoner_spells(game_mode=game_mode,
                                                            is_jungle=is_jungle_build)
    loadout['runes'] = get_runes()
    loadout['max_order'] = get_max_order()

    return loadout

# ---------------------------- PRELOADING ----------------------------
champions, items, full_items, boots, trinkets, summoner_spells = load_data()




