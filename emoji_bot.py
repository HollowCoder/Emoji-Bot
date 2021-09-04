import asyncio, collections, datetime, discord, emojis, json, math, operator, os, re
from operator import itemgetter
from collections import OrderedDict
from logging import error
from discord import Message
from discord.colour import Color
from discord.ext import commands
from discord.ext.commands import Context
from discord.sticker import Sticker
from multipledispatch import dispatch

if os.path.exists(os.getcwd() + "/config.json"):

    with open("./config.json") as f:
        configData = json.load(f)

else:
    configTemplate = {"Token": "", "Prefix": "e! "}

    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(configTemplate, f)

token = configData["Token"]
prefix = configData["Prefix"]

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix), formatter=None, description='', pm_help=True,owner_id=196728370480939008,intents=intents)
bot.remove_command("help")
#r10_latest_date = datetime

# Provides the activity and outputs the servers running in.
@bot.event
async def on_ready():
    game = discord.Game('emoji analytics')
    await bot.change_presence(status=discord.Status.online,activity=game)
    output = 'Running in the following servers:\n'
    num = 1
    for server in bot.guilds:
        output = f'{output}{num}: {server.name}\n'
        num += 1
    print(f'Logged in as {bot.user.name}\nID: {bot.user.id}\nRunning on version {discord.__version__}\n\n{output}')


# Uses a text file that will be loaded in JSON format.
async def load(path:str='main'):
    with open(f'C:/bot/{path}.txt') as f:
        data = json.load(f)
    return data

# Saves the relevant data from JSON format to a text file.
async def save(data, path:str='main'):
    with open(f'C:/bot/{path}.txt','w') as f:
        json.dump(data,f)

# This command is used to send an embeded DM to a user who needs help with the commands.
@bot.command(aliases=['h'])
async def help(ctx):
    user = ctx.author
    emb = discord.Embed(title='Emote Bot', description='Commands', Color=discord.Color.red())
    file = open("Emoji_Bot_Help.txt", "r")
    for line in file.readlines():
        l = line.split("-")
        emb.add_field(name=l[0], value=l[1], inline=False)
    await user.send(embed=emb)

# If the author is the bot, return. Otherwise this method loads a JSON file, gives any author who uses the bot 1 xp, and saves the data.
@bot.event
async def on_message(ctx):
    #if ctx.author.bot == True:
    #    return
    #data = await load()
    #data[ctx.author.id]['xp_count'] += 1
    #await save(data)
        #customs = re.findall(r'<:\w*:\d*>', ctx.content)
        #normals = emojis.get(ctx.content)
        #sort_normal = {}
        #sort_custom = {}
        #for e in customs:
        #    sort_custom[e]=customs.count(e)
        #print(ctx.content)
        #for e in normals:
        #    sort_normal[e] = ctx.content.count(e)
        # Might be able to remove the above, have to ask J.
    await bot.process_commands(ctx)
    

@bot.command(aliases=['rs'])
async def return_sticker(ctx, messid:Message):
    #From sticker name send sticker url to author DMs.
    sticker = messid.stickers
    #loop through list of stickers
    sticker_url = sticker.image_url_as(4096)
    await ctx.author.send(sticker_url)


@bot.command(aliases=['ge'])
async def get_emoji(ctx,messid:int):
    c = ctx.channel
    msg = await c.fetch_message(messid)
    customs = re.findall(r'<:\w*:\d*>', msg.content)
    normals = emojis.get(msg.content)
    sort_normal = {}
    sort_custom = {}
    for e in customs:
        sort_custom[e]=customs.count(e)
    for e in normals:
        num = 0
        for i in range(len(msg.content)):
            if (msg.content[i] == e):
                num = num + 1
        sort_normal[e] = num
    await ctx.send(f'Custom emotes: {sort_custom}\nNormal emotes: {sort_normal}')


@commands.is_owner()
@bot.command(aliases=['es'])
async def emoji_scan(ctx):
    sort_custom = {}
    sort_normal = {}
    sort_rcustom = {} #custom reactions
    sort_rnormal = {} #normal reactions
    for channel in ctx.guild.text_channels: #for each channel in the guild
        try:
            async for msg in channel.history(limit=None): #for each message in the channel
                customs = []
                normals = []
                r_custom = []
                r_normal = []
                customs = re.findall(r'<:\w*:\d*>', msg.content) #searches a message for unicode patterns that use words and decimal digits, i.e. emojis
                normals = emojis.get(msg.content)

                for e in customs: #for emojis that are custom
                    emote = bot.get_emoji(int(e.split(':')[-1][:-1]))
                    try:
                        try:
                            sort_custom[e]+=customs.count(e)
                        except:
                            sort_custom[e]=customs.count(e)
                    except:
                        pass
                for e in normals: #for emojis that are normal
                    try:
                        sort_normal[e]+=msg.content.count(e)
                    except:
                        sort_normal[e] = msg.content.count(e)
                #for e in 
        except Exception as e:
            print(f'Error: {e}')
            pass
    output = f'Custom Emojis: {sort_custom}\nNormal Emojis: {sort_normal}\nCustom Reactions: {sort_rcustom}\nNormal Reactions: {sort_rnormal}'
    num = math.ceil(len(output) / 1000)
    for x in range(1,num+1):
        await ctx.author.send(output[x*1000-1000:x*1000])

# Returns the emojis any users used as a reaction on a message. Perhaps we can send a single message for a user and their reactions? If one user has multiple reactions then there should be one line for them as well.
@bot.command(aliases=['gr'])
async def get_reactions(ctx, messid:int):
    msg = await ctx.channel.fetch_message(messid)
    output = ''
    output_dict = {} # A dict with list values. Each key is a user and each values is actually a list of values that will be the reactions they used.
    for reaction in msg.reactions:
        async for user in reaction.users():
            if user in output_dict.keys():
                output_dict.update({user:reaction})
            else:
                output += f'{user} reacted with {reaction}'
    await ctx.send(output)

# Returns the emojis any users used as a reaction on a message. This uses a message link but I can't get it to work currently.
# @bot.command(aliases=['gr'])
# async def get_reactions(ctx, messlink:str):
#     messid = messlink.split("/")
#     msg = await ctx.channel.fetch_message(messid)
#     for reaction in msg.reactions:
#         async for user in reaction.users():
#             await ctx.send(f'{user} reacted with {reaction}')

# Allows you to react to the previous message (or any given message ID) with a word in emoji form.
@bot.command(aliases=['wr'])
async def word_reaction(ctx, word, ID:int):
    #if messid is None: #Check the current channel for the most recent message
    channel = bot.get_channel(ID)
    message = await channel.fetch_message(channel.last_message_id)
    emoji_dict = { #custom emojis will need name and ids
        "A" : ["🇦", ":a_:867527125472509952"], "B" : ["🇧", ":b_:867527124969193494"],
        "C" : ["🇨"], "D" : ["🇩"],
        "E" : ["🇪"], "F" : ["🇫"],
        "G" : ["🇬"], "H" : ["🇭"],
        "I" : ["🇮"], "J" : ["🇯"],
        "K" : ["🇰"], "L" : ["🇱"],
        "M" : ["🇲"], "N" : ["🇳"],
        "O" : ["🇴"], "P" : ["🇵"],
        "Q" : ["🇶"], "R" : ["🇷"],
        "S" : ["🇸"], "T" : ["🇹"],
        "U" : ["🇺"], "V" : ["🇻", ":letter_v:858204031833604117"],
        "W" : ["🇼"], "X" : ["🇽"],
        "Y" : ["🇾"], "Z" : ["🇿"],
        "!" : "❕", "?" : "❔",
        "0" : "0️⃣", "1" : "1️⃣",
        "2" : "2️⃣", "3" : "3️⃣",
        "4" : "4️⃣", "5" : "5️⃣", 
        "6" : "6️⃣", "7" : "7️⃣",
        "8" : "8️⃣", "9" : "9️⃣",
        "#" : "#️⃣", "*" : "*️⃣"
        #"10" : "🔟" I don't think this emoji would be possible in the current configuration.
        }
    #used_emojis = []
    word = word.upper()
    output = []
    invalid = []
    for letter in word:
        if letter in emoji_dict:
            output.append(letter)
        else:
            invalid.append(letter)

    if output != []:
        for letter in output:
            await message.add_reaction(emoji_dict[letter])
    if invalid != []:
        bot_message = await ctx.send(f"The following characters cannot be used: {', '.join(invalid)}")
        await asyncio.sleep(15)
        await bot_message.delete()

#@word_reaction.error
#async def word_reaction_error(ctx, error, letter):
#    if isinstance(error, commands.BadArgument):
#        await ctx.send("This character cannot be used. {character}")

# This command posts the word you provide it with emojis. CONVERT CASE TO LOWERCASE
@bot.command(aliases=['s'])
async def shout(ctx, word):
    word = word.casefold()
    output = ""
    for letter in word:
        output = f"{output}:regional_indicator_{letter}: "
    await ctx.send(output)

@shout.error
async def shout_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("Test")

# @bot.command(aliases=['r10'])
# # # async def reaction_top_10(ctx): #Searches every message in every channel for users that have the most reactions for a top 10 list. NEED TO ADD UPDATE FEATURE! Needs pointer for current and previous updates to scan between them. Previous update pointer is stored in Reaction_Leaderboard_Update.txt. This function should also save the previous update from each server it is in.
    # guild_id = discord.Guild.id
    # current_date = datetime.datetime.now() # Current date
    # if os.path.isfile("Reaction_Leaderboard_Update.txt")!= True:
        # f = open("Reaction_Leaderboard_Update.txt", "w")
        # f.write(f"Name: {discord.Guild.name} Date: {current_date} ID: {guild_id}")
        # f.close()
    # with open("Reaction_Leaderboard_Update.txt", "r") as f:
        # for line in f:
            # if guild_id
    # else:
        # f = open("Reaction_Leaderboard_Update.txt", "r")
        # previous_date = f.readlines()
        # f.close()
    # top_ten = {}
    # reacted_users = {} #unsorted (by count) after first iteration and when new members are added
    # for channel in ctx.guild.text_channels: #for each channel in the guild
        # try:
            # async for msg in channel.history(limit=None, after=previous_date): #for each message in the channel
                # if len(msg.reactions) != 0:
                    # reactions = len(msg.reactions)
                    #reacted_users.update({msg.author})
                    # if msg.author.name in reacted_users.keys():
                        # reactions += reacted_users.get(msg.author.name)
                        # reacted_users.update({msg.author.name: reactions})
                    # else:
                        # reacted_users.update({msg.author.name: reactions})
                # else:
                    # continue
        # except Exception as e:
            # print(f'Error: {e}')
            # pass
    # top_ten = dict(sorted(reacted_users.items(), key=lambda item: item[1], reverse=True))
    # # embed = discord.Embed(title="**Reaction Leaderboard**", description="Shows a list of the top 10 users on the server who have the most reactions.", Color=0xFFD700)
    # for k, v in top_ten.items():
        # if (list(top_ten.keys()).index(k) + 1) % 2 == 0:
            # embed.add_field(name=f"{list(top_ten.keys()).index(k) + 1}. {k}", value=f"{v} reactions", inline=True)
        # elif (list(top_ten.keys()).index(k) + 1) % 2 != 0:
            # embed.add_field(name=f"{list(top_ten.keys()).index(k) + 1}. {k}", value=f"{v} reactions", inline=False)
    # await ctx.send(embed=embed)
    # with open("Reaction_Leaderboard.txt", "w") as f:
        # f = open("Reaction_Leaderboard_Update.txt", "w")
        # f.write(f"{datetime.datetime.now()}")
        # f.close()
#   if os.path.isfile("Reaction_Leaderboard.txt")!= True:
    #   f = open("Reaction_Leaderboard.txt", "w")
    #   f.write("Reaction Leaderboard\n")
    #   f.close()
#   with open("Reaction_Leaderboard.txt", "w") as file:
    #   file.write("Reaction Leaderboard\n")
    #   for k, v in top_ten.items():
        #   file.write(f"{k} has earned {v} reactions!\n")
#   with open("Reaction_Leaderboard.txt", "r") as file:
    #   await ctx.send(file.read())
    #   file.close()
# @bot.command(aliases=['gst'])
# async def get_sticker_tags(ctx: Context):
    # message = ctx.message
    # message
    # tags = stk.tags
    # await ctx.send(tags)

@bot.command(aliases=['e'])
async def embed_message(ctx, input): #Can be used to embed a message.
    embed = discord.Embed()
    #dict = {"Test":}
    embed.add_field(name="__Test__", value="*Test*")
    await ctx.send(embed=embed)

@bot.command(aliases=['plr'])
async def post_letter_reaction(ctx, ID:int):
    reactions = {"V" : ["🇻", ":letter_v:858204031833604117"]}
    #letter_v = bot.get_emoji(858204031833604117)
    #indicator_v = "🇻"
    #reactions = [letter_v, indicator_v]
    channel = bot.get_channel(ID)
    message = await channel.fetch_message(channel.last_message_id)
    for v in reactions.values():
        for entry in v:
            await message.add_reaction(entry)

@bot.command(aliases=['trl'])
async def test_reaction_letters(ctx, word): #Needs to check if a particular letter reaction is added and if so, post the next letter reaction.
    channel = bot.get_channel(ID)
    message = await channel.fetch_message(channel.last_message_id)
    emoji_dict = {
        "A" : ["🇦", ":a_:867527125472509952"], "B" : ["🇧", ":b_:867527124969193494"],
        "C" : ["🇨", ":c_:867527125341700176"], "D" : ["🇩", ":d_:867527125007335426"],
        "E" : ["🇪", ":e_:867527125380759602"], "F" : ["🇫", ":f_:867527125380890634"],
        "G" : ["🇬", ":g_:867527125383774208"], "H" : ["🇭", ":h_:867527125408940033"],
        "I" : ["🇮", ":i_:867527125405401110"], "J" : ["🇯", ":j_:867527125384298546"],
        "K" : ["🇰"], "L" : ["🇱"],
        "M" : ["🇲"], "N" : ["🇳"],
        "O" : ["🇴"], "P" : ["🇵"],
        "Q" : ["🇶"], "R" : ["🇷"],
        "S" : ["🇸"], "T" : ["🇹"],
        "U" : ["🇺"], "V" : ["🇻", ":letter_v:858204031833604117"],
        "W" : ["🇼"], "X" : ["🇽"],
        "Y" : ["🇾"], "Z" : ["🇿"],
        "!" : "❕", "?" : "❔",
        "0" : "0️⃣", "1" : "1️⃣",
        "2" : "2️⃣", "3" : "3️⃣",
        "4" : "4️⃣", "5" : "5️⃣", 
        "6" : "6️⃣", "7" : "7️⃣",
        "8" : "8️⃣", "9" : "9️⃣",
        "#" : "#️⃣", "*" : "*️⃣"
    }
    word = word.upper()
    output = []
    invalid = []
    for character in word:
        if character in emoji_dict:
            output.append(character)
            
        else:
            invalid.append(character)

    if output != []:
        for letter in output:
            await message.add_reaction(emoji_dict[letter])
            #Remove the en0
    if invalid != []:
        bot_message = await ctx.send(f"The following characters cannot be used: {', '.join(invalid)}")
        await asyncio.sleep(15)
        await bot_message.delete()

bot.run(token)