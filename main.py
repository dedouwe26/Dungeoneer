import discord
from discord import Permissions
import os

discord_token = ""
client_id = ""
with open("discord.txt", "r") as discordfile:
    discord_token = discordfile.readlines()[0]
    client_id = discordfile.readlines()[1]

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(discord_token)
permissions = Permissions.manage_roles | Permissions.read_messages | Permissions.manage_events | Permissions.send_messages | Permissions.create_public_threads | Permissions.send_messages_in_threads| Permissions.send_tts_messages | Permissions.manage_messages | Permissions.manage_threads | Permissions.embed_links | Permissions.attach_files | Permissions.mention_everyone | Permissions.add_reactions | Permissions.use_application_commands | Permissions.use_embedded_activities
print("permissions")
print("Invitation link: "+discord.utils.oauth_url(client_id, permissions=permissions))