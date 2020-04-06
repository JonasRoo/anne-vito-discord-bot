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
CHAMPIONS_RESOURCE_FILE_NAME = 'champions.json'
JOIN_CHAR = ', '

KAYN_FORMS = ['Red', 'Blue']

CHAMP_ICON_BASE_URL = 'http://ddragon.leagueoflegends.com/cdn/10.6.1/img/champion/'
CHAMP_ICON_FILE_TYPE = '.png'

# ---------------------- FUNCTIONS ---------------------- #


def _validate_all_champions() -> None:
    try:
        _ = ALL_CHAMPS.empty()
        del _
    except:
        raise SystemError(f'{CHAMPIONS_RESOURCE_FILE_NAME} not properly loaded!')


def load_champions() -> pd.DataFrame:
    # load item DataFrame from file
    champions_raw_data = file_utils.get_ddragon_raw_data(
        CHAMPIONS_RESOURCE_FILE_NAME)
    champs = pd.DataFrame(champions_raw_data['data']).transpose()

    # feature engineering
    champs['is_melee'] = champs.stats.apply(
        lambda x: 125 <= x['attackrange'] <= 200)
    champs['combined_name'] = champs.apply(lambda x: JOIN_CHAR.join([x['name'], x['title']]),
                                           axis=1)

    return champs


def get_random_kayn_form() -> str:
    return random.choice(KAYN_FORMS)


def get_clean_champ_name(champ_name: str) -> str:
    return ''.join(filter(str.isalnum, champ_name))


def get_champ_icon_url(champ_name: str) -> str:
    real_name = get_clean_champ_name(champ_name.split(JOIN_CHAR)[0])
    return CHAMP_ICON_BASE_URL + real_name + CHAMP_ICON_FILE_TYPE


def get_random_champ(prechoice: str=None) -> Dict[str, Union[str, bool]]:
    _validate_all_champions()

    champ = {}
    if prechoice:
        prechoice = get_clean_champ_name(prechoice).lower()
        choice = ALL_CHAMPS.loc[
            ALL_CHAMPS.name.apply(
                (lambda x: prechoice == get_clean_champ_name(x).lower()))
        ]
        assert len(choice) == 1, f'champion prechoice \"{prechoice}\" invalid!'
    else:
        choice = ALL_CHAMPS.sample(n=1)

    champ['name'] = choice['combined_name'].values[0]
    champ['is_melee'] = choice['is_melee'].values[0]
    champ['icon_url'] = get_champ_icon_url(choice.index.values[0])

    # for Kayn, the form has to be decided too
    if champ['name'].lower().startswith('kayn'):
        champ['form'] = get_random_kayn_form()

    return champ


# ---------------------- LOADING TO MEMORY ---------------------- #
ALL_CHAMPS = load_champions()

# ---------------------- DEMO ---------------------- #
if __name__ == '__main__':
    pprint.pprint(get_random_champ(prechoice=None))
    pprint.pprint(get_random_champ(prechoice='RekSai'))
