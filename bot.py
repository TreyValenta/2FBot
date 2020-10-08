import datetime
import random
from datetime import datetime
import os
import discord
import Levenshtein
import re
from os import path

TOKEN = os.environ.get('2FBOT_TOKEN')

client = discord.Client()

command_prefix = "!!"
cringe_words = ["cringe", "based"]
cringe_copypasta = ["\"Hurr, Cringe! Durr, Cringe! Cringe!\"",
                    "Is that all you shitposting fucks can say?!",
                    "\"ugh, based based based cringe cringe cringe based based cringe cringe\"",
                    "I feel like I'm in a fucking asylum full of dementering old people, that can do nothing but "
                    "repeat the same fucking words and look like a fucking broken record!",
                    "\"Cringe cringe cringe cringe! cringe based based! onions onions snoy! onions LOL onions! Cringe "
                    "boomer Le zoomer! I am boomer?! No zoom zoom zoomies, zoomer going zoomies!\"",
                    "AGH I FUCKING HATE THE INTERNET SO GOD DAMN MUCH!! FUCK SHITPOSTING HONEST GOD-FUCKING I HOPE "
                    "YOUR MOTHER CHOKES ON HER OWN FECES IN HELL! YOU COCKSUCKER!",
                    "OH BUT I KNOW MY POST IS CRINGED ISN'T IT? CRINGE CRINGE CRINGEY-CRINGE BASED CRINGE REDDIT "
                    "CRINGE BASED REDDIT ONIONS BASED ONIONS CRINGE REDDIT CRINGE"]
cringe_copypasta_cooldown = 300  # cooldown in seconds
command_list = ["help", "hello", "stand <stand name>"]
stand_list = []
stand_aliases = {
    "Stairway to Heaven": "Made in Heaven",
    "THE WORLD (Part 7)": "THE WORLD (Steel Ball Run)",
    "Death 13": "Death Thirteen",
    "Shining Diamond": "Crazy Diamond",
    "Reverb ACT1": "Echoes ACT1",
    "Reverb ACT2": "Echoes ACT2",
    "Reverb ACT3": "Echoes ACT3",
    "Show Off": "Surface",
    "Love Extra": "Love Deluxe",
    "Worse Company": "Bad Company",
    "Chili Pepper": "Red Hot Chili Pepper",
    "Opal Jam": "Pearl Jam",
    "Pole Jam": "Pearl Jam",
    "Heaven's Gate": "Heaven's Door",
    "Achtug Baby": "Achtung Baby",
    "Heart Father": "Atom Heart Father",
    "BoyManMan": "Boy II Man",
    "Boy to Man": "Boy II Man",
    "Boy 2 Man": "Boy II Man",
    "Terra Ventus": "Earth Wind and Fire",
    "Highway Go Go": "Highway Star",
    "Feral Cat": "Stray Cat",
    "Catgrass": "Stray Cat",
    "Misterioso": "Enigma",
    "Deadly Queen": "Killer Queen",
    "Heart Attack": "Sheer Heart Attack",
    "Bite the Dust": "Bites the Dust",
    "Killer Queen (Part 8)": "Killer Queen (Jojolion)",
    "Sheer Heart Attack (Jojolion)": "Killer Queen (Jojolion)",
    "Sheer Heart Attack (Part 8)": "Killer Queen (Jojolion)",
    "D4C": "Dirty Deeds Done Dirt Cheap",
    "D4C Love Train": "Dirty Deeds Done Dirt Cheap Love Train",
    "Love Train": "Dirty Deeds Done Dirt Cheap Love Train",
    "Golden Wind": "Gold Experience",
    "Golden Wind Requiem": "Gold Experience Requiem",
    "Zipper Man": "Sticky Fingers",
    "Moody Jazz": "Moody Blues",
    "Six Bullets": "Sex Pistols",
    "Li'l Bomber": "Aerosmith",
    "Purple Smoke": "Purple Haze",
    "Spicy Lady": "Spice Girl",
    "Shadow Sabbath": "Black Sabbath",
    "Tender Machine": "Soft Machine",
    "Kraftwerk": "Kraft Work",
    "Craft Work": "Kraft Work",
    "Arts & Crafts": "Kraft Work",
    "Tiny Feet": "Little Feet",
    "Mirror Man": "Man in the Mirror",
    "Thankful Dead": "The Grateful Dead",
    "The Thankful Death": "The Grateful Dead",
    "Grand Death": "The Grateful Dead",
    "Fisher Man": "Beach Boy",
    "Babyhead": "Baby Face",
    "White Ice": "White Album",
    "Gently Weeps": "White Album",
    "White Album Gently Weeps": "White Album",
    "White Ice Gently Weeps": "White Album",
    "Metallic": "Metallica",
    "Crush": "Clash",
    "Talking Mouth": "Talking Head",
    "Notorious Chase": "Notorious B.I.G",
    "Sanctuary": "Oasis",
    "Green Tea": "Green Day",
    "Emperor Crimson": "King Crimson",
    "Epitaph": "King Crimson",
    "Eulogy": "King Crimson",
    "Chariot Requiem": "Silver Chariot Requiem",
    "Prophecy Stones": "Rolling Stones",
    "Stone Ocean": "Stone Free",
    "Smack": "Kiss",
    "F.F.": "Foo Fighters",
    "Weather Forecast": "Weather Report",
    "Cry Cry Dolls": "Goo Goo Dolls",
    "Pale Snake": "Whitesnake",
    "Highway to Death": "Highway to Hell",
    "Burning Down": "Burning Down the House",
    "Diver Drive": "Diver Down",
    "Jail House Lock": "Jail House Rock",
    "Full Moon": "C-Moon",
    "Maiden Heaven": "Made in Heaven",
    "Tomb of the Noise": "Tomb of the Boom",
    "Listen to My Rhythm": "Boku no Rhythm wo Kiitekure",
    "Oh Lonesome Me": "Oh! Lonesome Me",
    "Frightening Monsters": "Scary Monsters",
    "Mando": "Mandom",
    "Snow Mountain": "Sugar Mountain",
    "Tubular": "Tubular Bells",
    "Filthy Acts at a Reasonable Price": "Dirty Deeds Done Dirt Cheap",
    "King Bed": "California King Bed",
    "Going Underground": "Born This Way",
    "Autumn Leaves": "Les Feuilles",
    "Nuts N. Bolts": "Nut King Call",
    "Nat King Cole": "Nut King Call",
    "Paper Moon": "Paper Moon King",
    "Flower Park": "Paisley Park",
    "King of Nothingness": "King Nothing",
    "I, Rock": "I Am a Rock",
    "Ozone Baby": "Ozon Baby",
    "DocToR Woo": "Doctor Wu",
    "Satoru Akefu": "Wonder of U"
}
parts = {"3": "*Stardust Crusaders*",
         "4": "*Diamond is Unbreakable*",
         "5": "*Vento Aureo*",
         "6": "*Stone Ocean*",
         "7": "*Steel Ball Run*",
         "8": "*Steel Ball Run*"}


def current_time():
    return datetime.utcnow()


def list_to_linebroken_string(string_list):
    output = ""
    for item in string_list:
        output += (item + "\n")
    return output


def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text


def remove_suffix(text, suffix):
    if text.endswith(suffix):
        return text[:(-1 * len(suffix))]
    return text


def most_similar_string(query, search_list):
    similarity_min = 10000
    output = ""
    for item in search_list:
        if Levenshtein.distance(query, item) < similarity_min:
            similarity_min = Levenshtein.distance(query, item)
            output = item
    return output


def part_color(part_number):
    try:
        part = int(part_number)
        if part == 3:
            return discord.Color(0x49408B)  # purple
        elif part == 4:
            return discord.Color(0xC5EDEF)  # blue
        elif part == 5:
            return discord.Color(0xDEA143)  # gold
        elif part == 6:
            return discord.Color(0x4A7D52)  # green
        elif part == 7:
            return discord.Color(0xF8A6F3)  # pink
        elif part == 8:
            return discord.Color(0xF3FCFD)  # white
        else:
            return discord.Color.dark_gray()
    except:
        return discord.Color.dark_gray()


def check_stand_alias(alias):
    try:
        return stand_aliases[alias]
    except:
        return alias


with open('stand_list.txt') as fp:
    line = fp.readline()
    count = 1
    while line:
        stand_list.append(remove_suffix(line, '\n'))
        line = fp.readline()
        count += 1


def number_to_part(param):
    try:
        return parts[str(param)]
    except:
        return param


def find_rule(rule):
    file = open("MagicCompRules.txt", encoding="utf8")
    if rule.lower() == "random":
        lines = file.read().splitlines()
        random_rule = ""
        while not re.match(r"[0-9][0-9][0-9][.][0-9]+[a-z]+", random_rule):
            random_rule = random.choice(lines)
        return random_rule
    else:
        line = file.readline()
        count = 1
        while line:
            if line.startswith(rule):
                return line
            line = file.readline()
            count += 1
    return "Rule " + rule + " could not be found"


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself

    global time_last_run
    if message.author == client.user:
        return
    else:
        discord_input = message.content
        print(str(message.author) + " in " + str(message.guild) + ": " + str(discord_input))

    if discord_input.lower() == (command_prefix + "help"):
        msg = "Command list:\n" + list_to_linebroken_string(command_list)
        await message.channel.send(msg)

    if discord_input.lower() == (command_prefix + "hello"):
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)

    if discord._input.lower() == (command_prefix + "invite"):
        await message.channel.send("https://discord.com/oauth2/authorize?client_id=532326343753596938&scope=bot")

    if discord_input.lower().startswith(command_prefix + "mtgrule"):
        rule_query = remove_prefix(discord_input.lower(), (command_prefix + "mtgrule "))
        await message.channel.send(find_rule(rule_query))

    if discord_input.lower().startswith(command_prefix + "stand"):
        stand_query = remove_prefix(discord_input, (command_prefix + "stand "))
        stand = check_stand_alias(most_similar_string(stand_query, stand_list))
        stand_file = 'stand_stats/' + stand + '.txt'
        if path.exists(stand_file):
            with open(stand_file) as fp:
                stand_stat_list = []
                line = fp.readline()
                count = 1
                while line:
                    stand_stat_list.append(remove_suffix(line, '\n'))
                    line = fp.readline()
                    count += 1
                description_text = list_to_linebroken_string(
                    stand_stat_list[3:5]) + "**First appears in:** " + number_to_part(stand_stat_list[0])
                embed = discord.Embed(
                    title=stand_stat_list[2],
                    description=description_text,
                    color=part_color(stand_stat_list[0])
                )
                embed.set_thumbnail(url=stand_stat_list[1])
                embed.add_field(name='Stats', value=list_to_linebroken_string(stand_stat_list[5:11]), inline=True)
                embed.add_field(name='Abilities', value=list_to_linebroken_string(stand_stat_list[11:]), inline=True)
                await message.channel.send(embed=embed)
        else:
            if stand == "Flaccid Pancake":
                await message.channel.send("Jesus fucking Christ, just search \"Limp Bizkit\"")
            else:
                await message.channel.send(stand)

    if 'based on' in discord_input.lower():
        return
    elif str(message.guild) == "Royal Rards":
        for i in cringe_words:
            if i in discord_input.lower():
                try:
                    if (datetime.utcnow() - time_last_run).total_seconds() >= cringe_copypasta_cooldown:
                        time_last_run = datetime.utcnow()
                        msg = list_to_linebroken_string(cringe_copypasta)
                        await message.channel.send(msg)
                    else:
                        return
                except NameError:
                    time_last_run = datetime.utcnow()
                    msg = list_to_linebroken_string(cringe_copypasta)
                    await message.channel.send(msg)
        return


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(TOKEN)
