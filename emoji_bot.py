import asyncio, collections, datetime, nextcord, emojis, json, math, operator, os, re, pprint
from time import time, strftime
import datetime
from operator import itemgetter
from collections import OrderedDict
from logging import error
from nextcord import Message
from nextcord.colour import Color
from nextcord.ext import commands
from nextcord.ext.commands import Context
from nextcord.sticker import Sticker
from nextcord import Client, guild
from nextcord import *
from nextcord import GuildSticker
#from multipledispatch import dispatch

if os.path.exists(os.getcwd() + "/config.json"):
    with open("./config.json") as f:
        configData = json.load(f)

else:
    configTemplate = {"Token": "", "Prefix": "e! "}
    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(configTemplate, f)

if os.path.exists(os.getcwd() + "/triggers.json"):
    with open("./triggers.json") as f:
        global_triggers = json.load(f)

else:
    triggerTemplate = {"":""}
    with open(os.getcwd() + "/triggers.json", "w+") as f:
        json.dump(triggerTemplate, f)


token = configData["Token"]
prefix = configData["Prefix"]

intents = nextcord.Intents.all()
bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix), formatter=None, description='', pm_help=True,owner_id=196728370480939008,intents=intents)
bot.remove_command("help")

# Provides the activity and outputs the servers running in.
@bot.event
async def on_ready():
    game = nextcord.Game('emoji analytics')
    await bot.change_presence(status=nextcord.Status.online,activity=game)
    output = 'Running in the following servers:\n'
    num = 1
    for server in bot.guilds:
        output = f'{output}{num}: {server.name}\n'
        num += 1
    print(f'Logged in as {bot.user.name}\nID: {bot.user.id}\nRunning on version {nextcord.__version__}\n\n{output}')
    


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
    emb = nextcord.Embed(title='Emoji Bot', description='Commands', color=nextcord.Color.red())
    file = open("Emoji_Bot_Help.txt", "r")
    for line in file.readlines():
        l = line.split("-")
        emb.add_field(name=l[0], value=l[1], inline=False)
    await user.send(embed=emb)

# If the author is the bot, return. Otherwise this method loads a JSON file, gives any author who uses the bot 1 xp, and saves the data.
#@bot.event
#async def on_message(ctx):
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
    #await bot.process_commands(ctx)

@bot.event
async def on_message(ctx):
    if ctx.author.bot == True: return
    if "e!" in ctx.content: 
        await bot.process_commands(ctx)
    #message = await ctx.message.content
    #elif "e!" in ctx.content and
    elif "tru" in ctx.content: await send_sticker(ctx)
    elif "http://twitter" in ctx.content: await replace_twitter_link(ctx)
    else:   
        await check_string(ctx)
        #await asyncio.sleep(3)
        #await mock_self_react(ctx)
    #message.add_reaction()

async def process_triggers(message):
    for trigger in global_triggers.keys():
        if (re.search (trigger, message.content)):
            splitup = re.split(":", global_triggers[trigger], maxsplit=1)
            action = splitup[0]
            if (len(splitup) > 1):
                args = splitup[1]
            else:
                args = ""
            print ("match: " + trigger + " | " + global_triggers[trigger])
            print ("Action=" + action + " arguments=" + args)
            await global_actions[action](message, args)


async def apply_automod (message, args):
    print ("Deleting the message for automod")

async def apply_sticker (message, args):
    print ("Applying a sticker, args=" + args)

async def apply_reaction (message, args):
    print ("Applying reactions, args=" + args)


@bot.event
async def on_reaction_add(reaction, user):
    await mock_self_react(reaction, user)


async def mock_self_react(reaction, user): #Reaction and user who added it
    #message = await ctx.fetch_message(ctx.messid)
    poster = reaction.message.author
    emoji = nextcord.utils.get(poster.guild.emojis, name="cringe")
    if poster.id is user.id:
        await reaction.message.reply(f"{poster.mention} self reacted. Cringe!{emoji}")
        await reaction.remove(user)
    
async def send_sticker(ctx):
    #if "tru" in ctx.guild.stickers:
    guild_sticker = nextcord.utils.get(ctx.guild.stickers, name="tru")
    sticker = await ctx.guild.fetch_sticker(guild_sticker.id)
    await ctx.channel.send(content="", reference=ctx, stickers=[sticker])
    #else:

    #pass

async def replace_twitter_link(ctx):
    message_string = ctx.content()
    vx = 'vx'
    #for i in message_string:
    #    if i
    link_list = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', message_string)
    #for link in link_list:
    #    for i in link:
    #        if i == 
    await ctx.reply(link_list)


async def show_triggers(): pass

async def check_string(ctx): #setup a list of trigger words with a text file
    post = ctx.content

@bot.command(aliases=['rs'])
async def return_sticker(ctx, messid:str, *args:str): #Using the message ID send sticker url to author DMs. Implement return error if message id not found. Given a message id, can a message object be found from any channel?
    #await ctx.message.delete()
    message = None
    if messid.isnumeric(): #If a message id is inputted
        message = await ctx.fetch_message(messid)
    elif messid.startswith("https"): #If a message link is inputted
        link = messid.split('/')
        message = await bot.get_guild(int(link[4])).get_channel(int(link[5])).fetch_message(int(link[6]))
    sticker_list = message.stickers
    sticker_item = sticker_list[0] #The first element of the Message sticker list should be the sticker the user wants.
    sticker_url = sticker_item.url
    await ctx.author.send(sticker_url)
    if args[0] == 'rc':
        await delete_call(ctx)


@bot.command(aliases=['ge'])
async def get_emoji(ctx, messid:int):
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

#@bot.command(aliases=['ti'])
#async def time_it(ctx):
#    print(await timeit.timeit(stmt=emoji_scan, setup=ctx, number=1))

@commands.is_owner()
@bot.command(aliases=['es'])
async def emoji_scan(ctx, *args):
    print(f"Starting emoji scan on " + ctx.guild.name)
    sort_custom = {}
    sort_normal = {}
    sort_rcustom = {} #custom reactions
    sort_rnormal = {} #normal reactions
    if "t" in args:
        start_time = time()
    if "dc" in args:
        delete_call(ctx)
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
    if "t" in args:
        end_time = time()
        total_time = end_time - start_time
    output = f'Here are the emojis and reactions used on the server: {ctx.guild.name} \nCustom Emojis: {sorted(sort_custom.items(), key=lambda x:x[1])}\nNormal Emojis: {sort_normal}\nCustom Reactions: {sort_rcustom}\nNormal Reactions: {sort_rnormal}'
    pattern = r'[{\'\[\]\(\)\,}]'
    new_output = re.sub(pattern, '', output)
    num = math.ceil(len(new_output) / 1000)
    emb = nextcord.Embed(title='Emote Bot', description='Emoji Scan', color=nextcord.Color.red())
    for x in range(1,num+1):
        await ctx.author.send(new_output[x*1000-1000:x*1000])
    if "t" in args:
        print(f"Total time: " + str(total_time) + " seconds")

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
    message = await channel.fetch_message(channel.last_message_id) #Passing through the message ID does not work for some reason
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

        #Dict of lists may not work
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
            emoji = emoji_dict[letter]
            await message.add_reaction(emoji)
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
    numbers = {"1":":one:", "2":":two:",
               "3":":three:", "4":":four:",
               "5":":five:", "6":":six:",
               "7":":seven:", "8":":eight:",
               "9":":nine:", "0":":zero:"}
    for letter in word:
        if letter.isnumeric():
            for k in numbers:
                if letter == k:
                    v = numbers.get(k)
                    output = f"{output}{v} "
        elif letter.isalpha():
            output = f"{output}:regional_indicator_{letter}: "
    await ctx.send(output)

@shout.error
async def shout_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("Test")

@bot.command(aliases=['r10'])
async def reaction_top_10(ctx): #Searches every message in every channel for users that have the most reactions for a top 10 list. NEED TO ADD UPDATE FEATURE! Needs pointer for current and previous updates to scan between them. Previous update pointer is stored in Reaction_Leaderboard_Update.txt. This function should also save the previous update from each server it is in.
    guild_id = nextcord.Guild.id
    current_date = datetime.datetime.now() # Current date
    if os.path.isfile("Reaction_Leaderboard_Update.txt")!= True:
        f = open("Reaction_Leaderboard_Update.txt", "w")
        f.write(f"Name: {nextcord.Guild.name} Date: {current_date} ID: {guild_id}")
        f.close()
    #with open("Reaction_Leaderboard_Update.txt", "r") as f:
        #for line in f:
        #    pass
        #    if guild_id
        #    else:
        #        f = open("Reaction_Leaderboard_Update.txt", "r")
        #        previous_date = f.readlines()
        #        f.close()
    top_ten = {}
    reacted_users = {} #unsorted (by count) after first iteration and when new members are added
    for channel in ctx.guild.text_channels: #for each channel in the guild
        try:
            async for msg in channel.history(limit=None, after=previous_date): #for each message in the channel
                if len(msg.reactions) != 0:
                    reactions = len(msg.reactions)
                    reacted_users.update({msg.author})
                    if msg.author.name in reacted_users.keys():
                        reactions += reacted_users.get(msg.author.name)
                        reacted_users.update({msg.author.name: reactions})
                    else:
                        reacted_users.update({msg.author.name: reactions})
                else:
                    continue
        except Exception as e:
            print(f'Error: {e}')
            pass
        top_ten = dict(sorted(reacted_users.items(), key=lambda item: item[1], reverse=True))
        embed = nextcord.Embed(title="**Reaction Leaderboard**", description="Shows a list of the top 10 users on the server who have the most reactions.", Color=0xFFD700)
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

#@bot.command(aliases=['dc'])
async def delete_call(ctx):
    await ctx.message.delete(delay=2)

@bot.command(aliases=['e'])
async def embed_message(ctx, input): #Can be used to embed a message.
    embed = nextcord.Embed()
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

global_actions = {
    "automod" : apply_automod,
    "sticker" : apply_sticker,   
    "react"   : apply_reaction
}

bot.run(token)

#print(timeit.timeit(emoji_scan, number=1))