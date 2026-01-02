import discord
import requests
import os

TOKEN = os.getenv("DISCORD_TOKEN")
SOURCE_CHANNEL_ID = int(os.getenv("SOURCE_CHANNEL_ID"))

TARGET_CHANNELS = {
    "en": int(os.getenv("CHANNEL_EN")),
    "ar": int(os.getenv("CHANNEL_AR")),
    "zh": int(os.getenv("CHANNEL_ZH")),
}

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def translate(text, target):
    r = requests.post(
        "https://libretranslate.de/translate",
        json={"q": text, "source": "auto", "target": target, "format": "text"},
        timeout=10
    )
    return r.json()["translatedText"]

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if message.channel.id != SOURCE_CHANNEL_ID:
        return

    for lang, channel_id in TARGET_CHANNELS.items():
        try:
            translated = translate(message.content, lang)
            channel = client.get_channel(channel_id)
            if channel:
                await channel.send(f"**{message.author.display_name}:** {translated}")
        except Exception as e:
            print(e)

client.run(TOKEN)
