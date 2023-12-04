import discord
from discord import app_commands
import os

discord_token = ""
client_id = ""
with open("discord.txt", "r") as discordfile:
    lines = discordfile.readlines()
    discord_token = lines[0]
    client_id = lines[1]

print("Invitation link: "+discord.utils.oauth_url(client_id, permissions=discord.Permissions(18479365422144)))

client = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(client)

# commandTree = discord.app_commands.CommandTree(bot, )

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await tree.sync()

@tree.command(name="opengame", description="Opens the game in that channel")
async def opengame(ctx: discord.Interaction):
    await ctx.channel.send("opened here")

client.run(discord_token)
