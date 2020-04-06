import random
import copy
import pprint

ABILITY_SYMBOLS = ['Q', 'W', 'E']
ALLOW_RANDOM_ULT_MAX = False


def get_max_order() -> str:
    abilities = {}
    max_order = copy.deepcopy(ABILITY_SYMBOLS)
    random.shuffle(max_order)

    ult_idx = random.randint(0, len(max_order)) if ALLOW_RANDOM_ULT_MAX else 0
    max_order.insert(ult_idx, 'R')

    abilities['max_order'] = max_order

    return abilities


# ---------------------- DEMO ---------------------- #
if __name__ == '__main__':
    pprint.pprint(get_max_order())
