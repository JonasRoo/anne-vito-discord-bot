import random
import pprint

# ---------------------- VALID LANE CHOICES GO HERE ---------------------- #
VALID_LANE_CHOICES = ['TOP', 'JUNGLE', 'MID',
                      'ADC', 'SUPPORT', 'FILL', 'ROAMING']


def get_random_lane(lane_prechoice: str=None) -> str:
    lane = {}
    if lane_prechoice:
        assert lane_prechoice.upper() in VALID_LANE_CHOICES, \
            f'Invalid lane prechoice (\"{lane_prechoice}!\")'
        lane['lane'] = lane_prechoice.upper()
    else:
        lane['lane'] = random.choice(VALID_LANE_CHOICES)

    return lane


def is_jungle(lane: str) -> bool:
    return lane.upper() == 'JUNGLE'


def is_support(lane: str) -> bool:
    return lane.upper() == 'SUPPORT'


# ---------------------- DEMO ---------------------- #
if __name__ == '__main__':
    pprint.pprint(get_random_lane())
