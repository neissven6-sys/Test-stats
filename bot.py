import discord
import os

# Dein Channel, in dem die Nachricht erscheinen soll
CHANNEL_ID = 1456387309631963268

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Bot online als {client.user}")
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("🤖 Test Stats ist online und bereit!")

# Token aus Environment Variable
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
client.run(DISCORD_TOKEN)
