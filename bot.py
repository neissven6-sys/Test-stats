import discord
from discord.ext import tasks
import requests
import xml.etree.ElementTree as ET
import json
import os

# ====== KONFIGURATION ======
CHANNEL_ID = 1456387309631963268  # DEIN Channel
OGAME_STATS_URL = "https://sXXX-de.ogame.gameforge.com/api/stats.xml?category=1&type=0"
LOSS_THRESHOLD = 1_000_000
CHECK_INTERVAL_MINUTES = 30
DATA_FILE = "players.json"

intents = discord.Intents.default()
client = discord.Client(intents=intents)

# ====== DATEN ======
def load_old_data():
    import os, json
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# ====== STATISTIK CHECK ======
@tasks.loop(minutes=CHECK_INTERVAL_MINUTES)
async def check_stats():
    channel = client.get_channel(CHANNEL_ID)
    if channel is None:
        return

    try:
        response = requests.get(OGAME_STATS_URL, timeout=30)
        root = ET.fromstring(response.text)
    except Exception as e:
        await channel.send(f"Fehler beim Abrufen der Stats: {e}")
        return

    old_data = load_old_data()
    new_data = {}

    for player in root.findall("player"):
        pid = player.attrib["id"]
        name = player.attrib["name"]
        points = int(player.attrib["score"])
        new_data[pid] = {"name": name, "points": points}

        if pid in old_data:
            diff = old_data[pid]["points"] - points
            if diff >= LOSS_THRESHOLD:
                await channel.send(f"📉 **{name}** hat **{diff:,} Punkte verloren!**")

    save_data(new_data)

# ====== EVENTS ======
@client.event
async def on_ready():
    print(f"Bot online als {client.user}")
    check_stats.start()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
client.run(DISCORD_TOKEN)
