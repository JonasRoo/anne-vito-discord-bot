from typing import Union, List, Dict

import random
import pprint
import pandas as pd

# append parent directory to PATH
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import file_utils


# ---------------------- CONSTANTS ---------------------- #
SPELLS_RESOURCE_FILE_NAME = 'summoner_spells.json'

# ---------------------- FUNCTIONS ---------------------- #


def _validate_all_summoner_spells() -> None:
    try:
        _ = ALL_SPELLS.empty
        del _
    except:
        raise SystemError(f'{SPELLS_RESOURCE_FILE_NAME} not properly loaded!')


def load_spells() -> pd.DataFrame:
    # load item DataFrame from file
    spells_raw_data = file_utils.get_ddragon_raw_data(
        SPELLS_RESOURCE_FILE_NAME)
    spells = pd.DataFrame(spells_raw_data['data']).transpose()

    # only consider spells for classic SR games
    spells = spells.loc[spells.modes.apply(lambda x: 'CLASSIC' in x)]

    return spells


def get_random_summoner_spells(is_jungle: bool) -> Dict[str, str]:
    choices = random.sample(ALL_SPELLS.name.to_list(), k=2)

    if is_jungle:
        # we need to take smite
        # also: prevent duplication (['Smite', 'Smite'])
        idx = 0 if choices[0].lower() == 'smite' else 1
        choices[idx] = 'Smite'

    summoner_spells = {'summoners': choices}
    return summoner_spells


# ---------------------- LOADING TO MEMORY ---------------------- #
ALL_SPELLS = load_spells()

# ---------------------- DEMO ---------------------- #
if __name__ == '__main__':
    pprint.pprint((get_random_summoner_spells(is_jungle=False)))
    pprint.pprint((get_random_summoner_spells(is_jungle=True)))
