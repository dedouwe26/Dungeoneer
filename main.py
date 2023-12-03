import discord
from discord.ext import commands
import os

discord_token = ""
client_id = ""
with open("discord.txt", "r") as discordfile:
    lines = discordfile.readlines()
    discord_token = lines[0]
    client_id = lines[1]

print("Invitation link: "+discord.utils.oauth_url(client_id, permissions=discord.Permissions(18479365422144)))

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='/', description="It's a dungeon game in Discord.", intents=intents)

# commandTree = discord.app_commands.CommandTree(bot, )

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    await bot.tree.sync()

# @bot.event
# async def on_message(message):
#     await bot.process_commands(message)
#     if message.author == bot.user:
#         return

#     if message.content.startswith('$hello'):
#         await message.channel.send('Hello!')
async def argauto():
    return "arg"
@bot.hybrid_command()
async def test(ctx, arg):
    await ctx.send(arg)

@bot.tree.command(name="opengame", description="Opens the game in that channel")
async def opengame(ctx: discord.Interaction):
    print("ok")


# async def opengameAutocomplete()

bot.run(discord_token)
