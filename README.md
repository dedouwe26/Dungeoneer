# Dungeoneer
Dungeoneer is an infinite dungeon game with generated dungeons. Generate random levels or use a seed.
It's built in python and can be played on a pc and in discord.
## Discord environment variables
DISCORD_TOKEN = "your discord bot token" <br>
DISCORD_CLIENT_ID = "your discord client id" <br>
## File Format
<code>
{lvl: float}    <br>
{inshop: bool}  <br>
{seed: str}     <br>
{x: float}      <br>
{y: float}      <br>
{health: float} <br>
{maxHealth: float}
</code>         <br>
<b>Example:</b> <br>
<code>
16              <br>
False           <br>
$843E38FFD0     <br>
10              <br>
22.4            <br>
3.1             <br>
</code>