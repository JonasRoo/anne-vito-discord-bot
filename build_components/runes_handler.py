from typing import Union, List, Dict

import random
import copy
import pprint

import pandas as pd

# append parent directory to PATH
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import file_utils


# ---------------------- CONSTANTS ---------------------- #
RUNES_RESOURCE_FILE_NAME = 'runes.json'
STATMOD_RESOURCE_FILE_NAME = 'stat_modifiers.json'

KEYSTONE_VARIABLE_NAME = 'keystones'
VALID_RUNE_LEVELS = ['level_one', 'level_two', 'level_three']

# ---------------------- FUNCTIONS ---------------------- #


def _validate_all_data() -> None:
    try:
        _ = len(ALL_RUNES)
        del _
    except:
        raise SystemError(f'{RUNES_RESOURCE_FILE_NAME} not properly loaded!')
    try:
        _ = len(ALL_STATMODS)
        del _
    except:
        raise SystemError(f'{STATMOD_RESOURCE_FILE_NAME} not properly loaded!')


def load_runes() -> pd.DataFrame:
    # load runes DataFrame from file
    runes = file_utils.get_ddragon_raw_data(RUNES_RESOURCE_FILE_NAME)
    return runes


def load_stat_modifiers() -> pd.DataFrame:
    stat_modifiers = file_utils.get_ddragon_raw_data(
        STATMOD_RESOURCE_FILE_NAME)
    return stat_modifiers


def get_choices_from_dict(dc: Dict[str, List[str]]) -> List[str]:
    choices = []
    for _, v in dc.items():
        choices.append(random.choice(v))

    return choices


def get_random_runes() -> Dict[str, List[str]]:

    _validate_all_data()
    runes = copy.deepcopy(ALL_RUNES)

    primary_tree_choice = random.choice(list(runes.keys()))
    primary_tree = runes.pop(primary_tree_choice)

    secondary_tree_choice = random.choice(list(runes.keys()))
    secondary_tree = runes.pop(secondary_tree_choice)
    secondary_tree.pop(KEYSTONE_VARIABLE_NAME)
    secondary_tree.pop(random.choice(VALID_RUNE_LEVELS))

    rune_choices = {}
    rune_choices['primary_runes'] = get_choices_from_dict(primary_tree)
    rune_choices['secondary_runes'] = get_choices_from_dict(secondary_tree)
    rune_choices['stat_modifiers'] = get_choices_from_dict(ALL_STATMODS)

    return rune_choices


# ---------------------- LOADING TO MEMORY ---------------------- #
ALL_RUNES = load_runes()
ALL_STATMODS = load_stat_modifiers()

# ---------------------- DEMO ---------------------- #
if __name__ == '__main__':
    pprint.pprint(get_random_runes())
