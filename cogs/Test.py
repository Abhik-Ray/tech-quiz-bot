import discord
from discord.ext import commands
from cogs.Ask import Ask
import time

class Test(commands.Cog):
  
  def __init__(self, client):
    self.client = client


  def advancedEmbed(self, question, description, footer):
    embed = discord.Embed(title=title, description = description, color=0xFF5733)
    embed.set_footer(text = footer)
    return embed

  @commands.command(pass_context=True)
  async def testembed(self, ctx):
    await ctx.send('Test!')
    

def setup(client):
  client.add_cog(Test(client))
