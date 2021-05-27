# To be the entry point of the bot
import discord
import os
from itertools import cycle
from discord.ext import commands, tasks

client = commands.Bot(command_prefix = '?')

# constant declarations
TOKEN = os.environ['TOKEN']
API_TOKEN = os.environ['API_TOKEN']

# lists
status = cycle([
  'TOP == -1',
  'ptr->data=\'ur lonely\'',
  'MaxPooling Questions',
  'ptr = head->next',
  'Giving you PTSD',
  'Segmentation Fault',
  'Spam and Eggs',
  'Chillin at $'
])
@client.event
async def on_ready():
  print('Bot is ready')
  change_status.start()

@client.command()
async def load(ctx, extension):
  client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
  client.unload_extension(f'cogs.{extension}')

@client.command()
async def reload(ctx, extension):
  client.unload_extension(f'cogs.{extension}')
  client.load_extension(f'cogs.{extension}')

@client.command()
async def ping(ctx):
  await ctx.send('4 packets recieved gracefully in ' + str(round(client.latency, 4)*1000) + 'ms')

@tasks.loop(minutes=30)
async def change_status():
  await client.change_presence(activity=discord.Game(next(status)))

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    load(client, f'cogs.{filename[:-3]}')

client.run(TOKEN)
