import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import openai

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_KEY = os.getenv('OPENAI_KEY')
SYSTEM_MESSAGE = os.getenv('SYSTEM_MESSAGE')

# set up openai api client

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='!', intents=intents)


def ask_gpt(prompt, system_message):
    openai.api_key = OPENAI_KEY
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt},
            ],
        temperature=0.9,
        )

    return response.choices[0].message.content


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='ask', help='Ask the bot a question')
async def ask(ctx, *, question: str):
    response = await ask_gpt(question, SYSTEM_MESSAGE)
    await ctx.send(response)

# start the bot
bot.run(TOKEN)
