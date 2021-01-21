"""
Knowherbot
-shamelessly assembled from the flesh of Bababot
"""

import logging
import os
import random
from itertools import product

import discord
from dotenv import load_dotenv

# Create a custom logger that logs to file and to stream
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create separate stream and file handlers
stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler('error.log')
stream_handler.setLevel(logging.DEBUG)
file_handler.setLevel(logging.WARNING)

# Create formatters and add to handlers
log_format = logging.Formatter('%(asctime)s %(levelname)s:%(name)s:%(message)s', datefmt='%d-%b-%y %H:%M:%S')
stream_handler.setFormatter(log_format)
file_handler.setFormatter(log_format)

# Add handlers to the logger
logger.addHandler(stream_handler)
logger.addHandler(file_handler)


# Load env vars
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
USER_ID_TO_DM_ON_ERROR = os.getenv('USER_ID_TO_DM_ON_ERROR')

# Init client
client = discord.Client()


@client.event
async def on_ready():
    logger.info(f'{client.user} has connected to Discord')


@client.event
async def on_message(message):
    # prevent infinite knowing of her:(
    if message.author == client.user:
        return

    #to do: add case for when its add the end of a sentence (so there won't be a space.
    #to do: add case for when it is followed by some kind of punctuation

    if 'er ' in message.content:
        widx = message.content.find('er ')
        widx = widx + 2
        sliced = message.content[0:widx + 1]
        reversedstring = sliced[::-1]
        spaceidx = reversedstring.find(' ')
        if spaceidx == -1:  # no spaces found, it was the first word.
            finalword = sliced
        else:
            reversedstring = reversedstring[0:spaceidx]
            finalword = reversedstring[::-1]


    if 'ire ' in message.content:
        widx = message.content.find('ire ')
        widx = widx + 2
        sliced = message.content[0:widx+1]
        reversedstring = sliced[::-1]
        spaceidx = reversedstring.find(' ')
        if spaceidx == -1: #no spaces found, it was the first word.
            finalword = sliced
        else:
            reversedstring = reversedstring[0:spaceidx]
            finalword = reversedstring[::-1]




        await message.channel.send(finalword + '? I hardly know her!', tts=True)

        random_float = random.random()
        if random_float < 0.1:
            await message.channel.send('p.s. remember that women are human beings and deserve to be respected.', tts=True)
        if random_float < 0.15:
            await message.channel.send('lol sorry to roast you like that bro.',tts=True)
        if random_float < 0.45:
            await message.channel.send('oh wait that actually works.',tts=True)




@client.event
async def on_error(event, *args, **kwargs):
    logger.exception("Ruh roh! unhandled exception:")

    # DM user that an error occurred if specified
    user = await client.fetch_user(int(USER_ID_TO_DM_ON_ERROR)) if USER_ID_TO_DM_ON_ERROR else None
    if user:
        await user.send('knowherbot error! check logs')

client.run(TOKEN)
