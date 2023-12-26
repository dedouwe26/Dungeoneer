import discord
from discord import app_commands
import os
from Dungeoneer import *

discord_token = os.environ["DISCORD_TOKEN"]
client_id = os.environ["DISCORD_CLIENT_ID"]

print("Invitation link: "+discord.utils.oauth_url(client_id, permissions=discord.Permissions(18479365422144)))

globalGame = Dungeoneer()

client = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(client)

def CreateEmbed(userID: int) -> discord.Embed:
    embed = discord.embeds.Embed(colour=discord.Colour(0xfc9403))
    embed.add_field(name="", value=globalGame.getPlayer(userID).GetImage())
    return embed

class GameView(discord.ui.View):
    @discord.ui.button(emoji="⚙️", )
    async def moveUp(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass
    @discord.ui.button(emoji="⬆️")
    async def moveUp(self, interaction: discord.Interaction, button: discord.ui.Button):
        globalGame.getPlayer(interaction.user.id).Move(0, 1)
        await interaction.response.edit_message(embed=CreateEmbed(interaction.user.id), view=GameView())

    @discord.ui.button(emoji="⬇️")
    async def moveDown(self, interaction: discord.Interaction, button: discord.ui.Button):
        globalGame.getPlayer(interaction.user.id).Move(0, -1)
        await interaction.response.edit_message(embed=CreateEmbed(interaction.user.id), view=GameView())

    @discord.ui.button(emoji="➡️")
    async def moveRight(self, interaction: discord.Interaction, button: discord.ui.Button):
        globalGame.getPlayer(interaction.user.id).Move(1, 0)
        await interaction.response.edit_message(embed=CreateEmbed(interaction.user.id), view=GameView())

    @discord.ui.button(emoji="⬅️")
    async def moveLeft(self, interaction: discord.Interaction, button: discord.ui.Button):
        globalGame.getPlayer(interaction.user.id).Move(-1, 0)
        await interaction.response.edit_message(embed=CreateEmbed(interaction.user.id), view=GameView())
    @discord.ui.button(emoji="🗡️")
    async def moveUp(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

class MenuView(discord.ui.View):
    @discord.ui.button(label="Start")
    async def clickbutton(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=CreateEmbed(interaction.user.id), view=GameView(), ephemeral=True)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await tree.sync()

@tree.command(name="opengame", description="Opens the game in that channel")
async def opengame(interaction: discord.Interaction):
    # gameEmbed = discord.embeds.Embed()
    # gameEmbed.add_field(name="test", value="test")
    await interaction.response.send_message("Dungeoneer Game", view=MenuView())

client.run(discord_token)
