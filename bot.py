from client_secrets import DISCORD_TOKEN

import discord
from discord.ext import commands

import pprint
import json
import random_builds as rb


CHAMP_ICON_BASE_URL = 'http://ddragon.leagueoflegends.com/cdn/10.6.1/img/champion/'

client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
	print('Bot client is ready.')


@client.command()
async def ping(ctx):
    await ctx.send('pong')


async def abuild(ctx, *args):
	is_custom_command = False
	if args:
		args = list(args)
		print(f'Custom args detected: {args}')
		is_custom_command = True
		if args[-1].upper() in rb.VALID_LANE_CHOICES:
			# a lane prechoice was entered
			lane_prechoice = args.pop().upper()
			champion_prechoice = ' '.join(args) or None
		else:
			champion_prechoice = ' '.join(args)
			lane_prechoice = None

	if is_custom_command:
		build = rb.generate_random_loadout(champion_prechoice=champion_prechoice,
			lane_prechoice=lane_prechoice)
	else:
		build = rb.generate_random_loadout()
	embed = discord.Embed(
		title='Champion:',
		description=build['champion'],
		colour=discord.Colour.blue()
		)
	champion_name = ''.join(filter(str.isalnum, build['champion'].split(', ')[0]))
	if champion_name == 'Wukong':
		champion_name = 'MonkeyKing'
	champion_icon_url = CHAMP_ICON_BASE_URL + champion_name + '.png'


	embed.set_author(name='The Ironnovator')
	embed.set_thumbnail(url=champion_icon_url)
	embed.set_image(url=r'https://cdn.discordapp.com/emojis/599027745061863436.png')

	embed.add_field(name='Lane', value=build['lane'], inline=False)
	embed.add_field(name='Boots', value=build['items']['boots'], inline=True)
	embed.add_field(name='Trinket', value=build['items']['trinket'], inline=True)
	embed.add_field(name='Items', value=build['items']['full_items'], inline=False)
	embed.add_field(name='Summoner Spells', value=build['summoner_spells'], inline=True)
	embed.add_field(name='Max Order', value=build['max_order'], inline=True)
	embed.add_field(name='Primary Runes', value=build['runes']['primaries'], inline=False)
	embed.add_field(name='Secondary Runes', value=build['runes']['secondaries'], inline=False)
	embed.add_field(name='Stat Modifier', value=build['runes']['stat_modifier'], inline=False)
	

	await ctx.send(embed=embed)


def wrap_code(text):
	return '```json\n' + json.dumps(text, indent=4) + '```'

client.run(DISCORD_TOKEN)