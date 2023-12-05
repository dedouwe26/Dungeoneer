import discord
from discord import app_commands
import os

discord_token = os.environ["DISCORD_TOKEN"]
client_id = os.environ["DISCORD_CLIENT_ID"]

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
