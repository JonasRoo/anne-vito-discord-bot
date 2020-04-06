from client_secrets import DISCORD_TOKEN

import discord
from discord.ext import commands

import pprint
import json
from build_components import build_controller, lane_handler


client = commands.Bot(command_prefix='!')


@client.event
async def on_ready():
    print('All ressources loaded. Bot operational!')


@client.command()
async def build(ctx, *args):
    champion_prechoice, lane_prechoice = None, None
    if args:
        args = list(args)
        if args[-1].upper() in lane_handler.VALID_LANE_CHOICES:
            # a lane prechoice was entered
            lane_prechoice = args.pop().upper()
            champion_prechoice = ' '.join(args) or None
        else:
            # just the champion was pre-chosen, not the lane
            champion_prechoice = ' '.join(args)
            lane_prechoice = None

    build = build_controller.get_random_loadout(
        champion_prechoice=champion_prechoice,
        lane_prechoice=lane_prechoice)
    embed = build_controller.convert_build_to_embed(build=build,
            author=ctx.author)

    await ctx.send(embed=embed)


def wrap_code(text):
    return '```json\n' + json.dumps(text, indent=4) + '```'


if __name__ == '__main__':
    client.run(DISCORD_TOKEN)
