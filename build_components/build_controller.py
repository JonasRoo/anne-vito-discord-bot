from typing import Union, Dict, List
import pprint

import discord

if __name__ == '__main__':
    import lane_handler
    import champion_handler
    import item_handler
    import max_order_handler
    import runes_handler
    import summoner_spells_handler
else:
    from . import lane_handler, champion_handler, item_handler
    from . import max_order_handler, runes_handler, summoner_spells_handler

DEFAULT_JOIN_CHAR = ' | '
SPECIAL_JOIN_CHARS = {
    'max_order': ' > ',
    'summoners': ' & '
}


def convert_lists_to_strings(
        dc: Dict[str, Union[Dict[str, Union[str, List[str]]]]]) \
        -> Dict[str, Union[str, Dict[str, str]]]:
    for k, v in dc.items():
        if isinstance(v, dict):
            dc[k] = convert_lists_to_strings(v)
        elif isinstance(v, str):
            continue
        elif isinstance(v, list):
            join_char = SPECIAL_JOIN_CHARS.get(k, DEFAULT_JOIN_CHAR)
            dc[k] = join_char.join(v)
        else:
            continue

    # print(dc)
    return dc


def get_random_loadout(
        champion_prechoice: str = None,
        lane_prechoice: str = None,
        do_join: bool = True) -> Dict[str, Dict[str, Union[List[str], str]]]:

    loadout = {}

    loadout['lane'] = lane_handler.get_random_lane(
        lane_prechoice=lane_prechoice)
    is_jungle = lane_handler.is_jungle(loadout['lane']['lane'])
    is_support = lane_handler.is_support(loadout['lane']['lane'])

    loadout['champion'] = champion_handler.get_random_champ(
        prechoice=champion_prechoice)

    loadout['items'] = item_handler.get_random_item_set(
        is_jungle=is_jungle,
        is_support=is_support,
        is_melee=loadout['champion']['is_melee'])

    loadout['max_order'] = max_order_handler.get_max_order()

    loadout['runes'] = runes_handler.get_random_runes()

    loadout['summoner_spells'] = summoner_spells_handler.get_random_summoner_spells(
        is_jungle=is_jungle)

    if do_join:
        loadout = convert_lists_to_strings(loadout)

    return loadout


def convert_build_to_embed(build: Dict[str, Union[str, Dict[str, str]]],
        author=None) -> discord.Embed:

    embed = discord.Embed(
        title='Champion:',
        description=build['champion']['name'],
        colour=discord.Colour.blue()
    )

    embed.set_author(name=f'@{author}' or 'Anne Vito')
    embed.set_thumbnail(url=build['champion']['icon_url'])
    # embed.set_image(
    #     url=r'https://cdn.discordapp.com/emojis/599027745061863436.png')

    embed.add_field(name='Lane',
                    value=build['lane']['lane'],
                    inline=False)

    embed.add_field(name='Starter Item',
                    value=build['items']['starter_item'],
                    inline=True)
    embed.add_field(name='Boots', value=build['items']['boots'],
                    inline=True)
    embed.add_field(name='Trinket',
                    value=build['items']['trinket'],
                    inline=True)

    embed.add_field(name='Items',
                    value=build['items']['full_item'],
                    inline=False)

    embed.add_field(name='Summoner Spells',
                    value=build['summoner_spells']['summoners'],
                    inline=True)
    embed.add_field(name='Max Order',
                    value=build['max_order']['max_order'],
                    inline=True)

    embed.add_field(name='Primary Runes',
                    value=build['runes']['primary_runes'],
                    inline=False)
    embed.add_field(name='Secondary Runes',
                    value=build['runes']['secondary_runes'],
                    inline=False)
    embed.add_field(name='Stat Modifier',
                    value=build['runes']['stat_modifiers'],
                    inline=False)

    return embed

# ---------------------- DEMO ---------------------- #
if __name__ == '__main__':
    pprint.pprint(get_random_loadout())
