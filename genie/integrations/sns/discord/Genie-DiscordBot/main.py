import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
description = """ Genie bot """

intents = discord.Intents.all()

cogs: list = ["functions.guide", "functions.streaming"]

client = commands.Bot(
    command_prefix="!",
    help_command=None,
    description=description,
    intents=intents,
)


@client.event
async def on_ready():
    print("Genie Bot is ready!")

    await client.change_presence(
        status=discord.Status.online, activity=discord.Game("Genie Bot")
    )

    for cog in cogs:
        try:
            print(f"Loading cog {cog}")
            await client.load_extension(cog)
            print(f"Loaded cog {cog}")
        except Exception as e:
            exc = "{} : {}".format(type(e).__name__, e)
            print("Failed to load cog {}\n{}".format(cog, exc))


client.run(os.environ["DISCORD_TOKEN"])
