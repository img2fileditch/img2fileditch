# main.py
import discord, discord.ext, requests
from discord.ext import commands

# Bot Setup
intents = discord.Intents.all()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix = "?", intents=intents, help_command=None)

def uploadfile(url:str):
    try:
        data = {'url': url}
        response = requests.post('https://img2fileditch.nexcord.pro/api', data=data)

        return response.text
    except:
        return 'fail'

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    
# Commands
@bot.event
async def on_message(ctx):
    if ctx.author == bot.user:
        return
    if bot.user.mentioned_in(ctx):
        if ctx.reference != None:
            referenced_message = await ctx.channel.fetch_message(ctx.reference.message_id)

            images = []

            if referenced_message.attachments or referenced_message.embeds:
                if referenced_message.attachments:
                    for attachment in referenced_message.attachments:
                        images.append(attachment.url)

                if referenced_message.embeds:
                    for embed in referenced_message.embeds:
                        images.append(embed.thumbnail.url)
            else:
                await ctx.channel.send('You need to reply to a Image!')

            for url in images:
                image = uploadfile(url)
                if image != 'fail':
                    await ctx.channel.send(f'Uploaded image: {image}')
                else:
                    await ctx.channel.send('API is down ... L')
                    break
        else:
            await ctx.channel.send('You need to reply to a Image!')

    await bot.process_commands(ctx)

# Run Bot
bot.run('')