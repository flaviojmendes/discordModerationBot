import discord
import os
from discord.ext import commands
from difflib import SequenceMatcher

from services.image_moderation_service import moderate_image

client = discord.Client()

bot = commands.Bot(command_prefix='.')

# Global Variables
with open('badwords.txt') as f:
    BAD_WORDS = f.read().splitlines()


@bot.command()
async def hello(ctx):
    await ctx.send('Howdy! I\'m your utility belt!')


@bot.event
async def on_message(message):
    if len(message.attachments) > 0:
        await moderate_image(message)
    await moderate_message(message)


@bot.event
async def on_message_edit(before, after):
    await moderate_message(after)


async def moderate_message(message):
    if bot.user.id == message.author.id:
        return

    for word in message.clean_content.split(' '):
        for bad_word in BAD_WORDS:
            similarity = SequenceMatcher(None, bad_word.lower(), word.lower()).ratio()

            if similarity == 1:
                member = await message.author.create_dm()
                await member.send('Oh, you shouldn\'t say this kind of thing.. 😅: \n```' + message.clean_content + '```')
                await message.delete()
                return

            if similarity >= 0.8:
                member = await message.author.create_dm()
                await member.send('Hey, I have removed your message: \n```' +
                                  message.clean_content +
                                  '```\n' +
                                  'due to the similarity with prohibited messages in this server.')
                await message.delete()
                return


bot.run(os.environ['DISCORD_API_KEY'])
