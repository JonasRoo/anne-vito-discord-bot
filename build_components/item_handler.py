from typing import Union, List, Dict

import random
import pandas as pd
import pprint

# append parent directory to PATH
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import file_utils


# ---------------------- CONSTANTS ---------------------- #
ITEMS_RESOURCE_FILE_NAME = 'items.json'

JOIN_CHAR = ' | '
ITEM_CATEGORIES = {
    'boots': 1,
    'starter_item': 1,
    'trinket': 1,
    'full_item': 5
}

ORNN_ITEMS = {
    '3371': 'Molten Edge',
    '3373': 'Forgefire Cape',
    '3374': 'Rabadon\'s Deathcrown',
    '3379': 'Infernal Mask',
    '3380': 'Obsidian Cleaver',
    '3382': 'Salvation',
    '3383': 'Circlet of the Iron Solari',
    '3384': 'Trinity Fusion',
    '3386': 'Zhonya\'s Paradox',
    '3387': 'Frozen Fist',
    '3388': 'Youmuu\'s Wraithblade',
    '3389': 'Might of the Ruined King',
    '3390': 'Luden\'s Pulse',
}

STARTER_ITEMS = ['doran', 'cull', 'boots of speed', 'corrupting potion']
SMITE_VARIATIONS = ['Challenging Smite', 'Chilling Smite']
JUNGLE_STARTING_ITEMS = ['Hunter\'s Talisman', 'Hunter\'s Machete']

MELEE_ONLY_ITEMS = ['tiamat', 'titanic hydra', 'ravenous hydra']
RANGED_ONLY_ITEMS = ['runaan\'s hurricane']


# ---------------------- FUNCTIONS ---------------------- #
def _validate_all_items() -> None:
    try:
        _ = ALL_ITEMS.info()
    except:
        raise SystemError(f'{ITEMS_RESOURCE_FILE_NAME} not properly loaded!')


def join_item_list(l: List[any]) -> str:
    if isinstance(l, list):
        return JOIN_CHAR.join(l)
    else:
        return l


def listify_column(value: pd.Series) -> List[Union[str]]:
    if isinstance(value, list):
        return value
    elif pd.isna(value):
        return []
    else:
        return [value]


def load_items() -> pd.DataFrame:
    # load item DataFrame from file
    items_raw_data = file_utils.get_ddragon_raw_data(ITEMS_RESOURCE_FILE_NAME)
    items = pd.DataFrame(items_raw_data['data']).transpose()

    # feature engineering
    items['into'] = items['into'].apply(lambda x: listify_column(x))
    items['item_class'] = items.apply(lambda x: classify_item(x), axis=1)
    items['range_restriction'] = items.apply(lambda x: get_item_range_restriction(x),
                                             axis=1)

    return items


def classify_item(item: pd.Series) -> Union[str, None]:
    if item.empty:
        return None

    if not item['maps']['11']:
        # the item is not purchasable on SR
        return None

    if not item['gold']['purchasable']:
        # item can't be purchased in store
        return None

    if 'quick charge' in item['name'].lower():
        # it's a quick charge version of an item > not buildable on classic SR
        return None

    if not pd.isna(item['requiredChampion']) or not pd.isna(item['requiredAlly']):
        # item is champion specific or an Ornn Item
        return None

    if 'Consumable' in item['tags'] or not pd.isna(item['consumed']):
        # Consumable e.g. Pink Ward, Potion
        return None

    if 'Boots' in item['tags'] and not item['into']:
        # item is finished boots
        return 'boots'

    if 'Trinket' in item['tags']:
        # item is a trinket e.g. Warding Totem
        return 'trinket'

    if 'GoldPer' in item['tags']:
        # item is purchasable GoldPer10 support item
        return 'support_item'

    if any([x in item['name'].lower() for x in STARTER_ITEMS]):
        return 'starter_item'

    if 'enchantment' in item['name'].lower():
        # item is a fully-built jungle item
        return 'jungle_item'

    if not item['into'] or (len(item['into']) == 1 and item['into'][0] in ORNN_ITEMS):
        # Two cases:
        #   1) item is built into something else > it's not a full item
        #   2) The item is only built into its Ornn version > lookup
        return 'full_item'

    # None of the above 'positive' cases applied > item is not of interest
    return None


def get_item_range_restriction(item: pd.Series) -> Union[str, None]:
    item_name = item['name'].lower()

    if item_name in RANGED_ONLY_ITEMS:
        return 'ranged_only'
    elif item_name in MELEE_ONLY_ITEMS:
        return 'melee_only'
    else:
        return None


def add_jungle_item_variation(enchantment_item: str) -> str:
    variation_choice = '(' + random.choice(SMITE_VARIATIONS) + ')'
    return ' '.join([enchantment_item, variation_choice])


def select_n_random_of_class(item_class: str, n: int=1, is_melee: bool=False) -> List[str]:
    assert item_class in ALL_ITEMS.item_class.unique(), \
        f'\nInvalid item_class! (\"{item_class}\")'
    if is_melee:
        all_item_names = ALL_ITEMS.loc[(ALL_ITEMS.item_class == item_class) &
                                       (ALL_ITEMS.range_restriction.isin([None, 'melee_only']))].name.to_list()
    else:
        all_item_names = ALL_ITEMS.loc[(ALL_ITEMS.item_class == item_class) &
                                       (ALL_ITEMS.range_restriction.isin([None, 'ranged_only']))].name.to_list()

    return random.sample(all_item_names, k=n)


def get_random_item_set(is_jungle: bool,
                        is_support: bool,
                        is_melee: bool) -> Dict[str, List[str]]:

    _validate_all_items()
    assert not (is_jungle and is_support), \
        'Build can not be both a jungle and a support build!'

    item_set = {}
    for category, amount in ITEM_CATEGORIES.items():
        item_set[category] = select_n_random_of_class(
            item_class=category, n=amount)

    if is_jungle:
        item_set['starter_item'] = [random.choice(JUNGLE_STARTING_ITEMS)]
        jungle_item_idx = random.randint(0, len(item_set['full_item']) - 1)
        jungle_choice = select_n_random_of_class(item_class='jungle_item')[0]
        item_set['full_item'][
            jungle_item_idx] = add_jungle_item_variation(jungle_choice)
    elif is_support:
        item_set['starter_item'] = select_n_random_of_class(
            item_class='support_item')[0]

    # for category, items in item_set.items():
    #     item_set[category] = join_item_list(items)

    return item_set


# ---------------------- LOADING TO MEMORY ---------------------- #
ALL_ITEMS = load_items()

# ---------------------- DEMO ---------------------- #
if __name__ == '__main__':
    pprint.pprint(get_random_item_set(True, False, False))
