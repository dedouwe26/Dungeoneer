import discord
from discord import app_commands
import os

discord_token = os.environ["DISCORD_TOKEN"]
client_id = os.environ["DISCORD_CLIENT_ID"]

print("Invitation link: "+discord.utils.oauth_url(client_id, permissions=discord.Permissions(18479365422144)))

client = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(client)

class GameView(discord.ui.View):
    @discord.ui.button(label="Click!!")
    async def clickbutton(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.user.send("why didd you click??")

class MyView(discord.ui.View): # Create a class called MyView that subclasses discord.ui.View
    @discord.ui.button(label="Click me!", style=discord.ButtonStyle.primary, emoji="😎") # Create a button with the label "😎 Click me!" with color Blurple
    async def button_callback(self, button, interaction):
        await interaction.response.send_message("You clicked the button!")

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await tree.sync()

@tree.command(name="opengame", description="Opens the game in that channel")
async def opengame(interaction: discord.Interaction):
    # gameEmbed = discord.embeds.Embed()
    # gameEmbed.add_field(name="test", value="test")
    a = await interaction.response.send_message("opened here", view=GameView())

client.run(discord_token)
