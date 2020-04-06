from typing import Dict, List
import os
import json

def get_ddragon_raw_data(file_name: str) -> Dict[any, any]:
    parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    file_path = os.path.join(parent_directory, 'DDRAGON', file_name)
    with open(file_path, 'r', encoding='utf-8') as file:
        raw_data = json.load(file)
    return raw_data


def get_choices_from_dict(dc: Dict[str, List[str]], join_char: str=None) -> List[str]:
    choices = []
    for _, v in dc.items():
        choices.append(random.choice(v))