import discord
from discord.ext import commands
from discord.ui import Button, View
from random import randint
from dotenv import load_dotenv

import os

# Client
client = commands.Bot(command_prefix="?", intents=discord.Intents.all())


#Text Channel ID's ######################################
##############################################################
##############################################################

#server
lists = {
    "general": 123123123123123
}


lister = [values for keys, values in lists.items() if keys == "general"]
##############################################################
##############################################################
##############################################################




# # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # 
# Database 
import pyodbc

conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=')
cursor = conn.cursor()
cursor.execute('select * from Table1')
listed = list(cursor)

# database functions
def db_names():
    number = 0
    for id, name, link in listed:
        number +=1
        yield "{}:\t{}\n".format(number, name)

def db_insert(input_name, link):
    cursor.execute("insert into Table1 (name, links) values(?,?)",(input_name,link))
    cursor.commit()
    return "{} with the link of:\t{}\nhas been inserted!".format(input_name,link)

def db_link(input_name):
    for id, name, link in listed:
        if name == input_name:
            yield "{}'s link is:\n{}\n".format(input_name,link.strip('#'))

def db_delete(name):
    cursor.execute(("DELETE FROM Table1 WHERE name = ?"), name)
    cursor.commit()
    return f"{name} has been deleted!"
    
def db_close():
    cursor.close()
    conn.close()
    return "db has successfuly been closed..."


# Database Client Commands
@client.command()
async def l_name(ctx):
    await ctx.send("".join(db_names()))
@client.command()
async def l_insert(ctx, input_name, input_link):
    await ctx.send(db_insert(input_name, input_link))
@client.command()
async def l_link(ctx, input_name):
    await ctx.send("".join(db_link(input_name)))
@client.command()
async def l_delete(ctx, name):
    await ctx.send(db_delete(name))
@client.command()
async def l_close(ctx):
    await ctx.send(db_close())
# # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # 




# Functions
def league():
    modez = ["Blind", "Urf", "ranked"]
    x = randint(0,1)
    return modez[x]

def spind():
    modez = ["penguin game", "put yourself together", "crab game", "unsolved case", "DYO"]
    modez2 = ["come with me", "one armed cook", "bro falls", "scp secret laboratory", "escape memoirs", 
              "escape room, - der kranke", "in sink", "with you", "the timelsess child", "the two of us", 
              "flash party","smithworks", "vr chat?", "put yourself together", "Beavers be damned",
              "cry of fear", "fears to fathom", "We were here: expeditions friendship", "Handshakes", "put yourself together"]
    x = randint(0,19)
    return modez2[x]


@client.command()
async def spinda(ctx):
    await ctx.send(spind())

@client.command()
async def gamemode(ctx):
    await ctx.send(league())

def magic8ball():
    messages = ["Try again", "Yes", "No", "Maybe", "Follow your heart", "Luck befalls you", "You will be unlucky",
                "Be aggressive", "Pull back a bit"]
    x = randint(0,8)
    return messages[x]

def c_flipper():
    coin = ["Heads!", "Tails!"]
    x = randint(0,1)
    return coin[x]

def roshambo(hand):
    hand = hand.upper()
    opt_bhand = [":rock:", ":hand_splayed:", ":scissors:"]
    ra =  randint(0,2)
    b_hand = opt_bhand[ra]
    if (hand=="ROCK"):
        emj_hand = ":ROCK:"
    elif (hand=="PAPER"):
        emj_hand = ":HAND_SPLAYED:"
    elif (hand=="SCISSORS"):
        emj_hand = ":SCISSORS:"
    else:
        return f"You can't use {hand.lower()}, stupid :joy:"
        
    if (b_hand.upper()==emj_hand):
        return f"{b_hand} \nIt's a Tie! :knot:"
    elif (b_hand.upper() == ":ROCK:" and hand == "SCISSORS") or \
        (b_hand.upper() == ":HAND_SPLAYED:" and hand == "ROCK") or \
        (b_hand.upper() == ":SCISSORS:" and hand == "PAPER"):
        return f"{b_hand} \nI Win! :blush:"
    else:
        return f"{b_hand} \nI Lose :cry:"

def compliments():
    compliments = ["You are awesome :)", "You are amazing!", "You're fantastic!", "Well done!", "You're a great guy",
                   "You're simply... The BEST!", "No one is going to top you! :D", "You are very huggable", "I love everything about you :)",
                   "No"]
    return compliments[randint(0,len(compliments))]

    

    
# Client Events
# On Ready
@client.event
async def on_ready():
    print("Bot is Ready! \n")

    for key in lister:
            
        channel = await client.fetch_channel(key)
        messages = [message async for message in channel.history(limit=5)]

        print("{:-^30}".format(str(channel.guild)))
        for message in messages:
            print(message.author, message.content)
        print("\n")


# On Message
@client.event
async def on_message(message):
        channel = message.channel
        if str(message.author) != "bot#123" and "compliment me" in message.content:
            await channel.send(compliments())

# Client Commands
@client.command()
async def m8ball(ctx):
    await ctx.send(magic8ball())
@client.command()
async def coinflip(ctx):
    await ctx.send(c_flipper())
@client.command()
async def copy(ctx, *greg):
    await ctx.send(" ".join(greg))
@client.command()
async def goodnight(ctx):
    await ctx.send("Good Night!")
@client.command()
async def rps(ctx):
    Rbutton = Button(label="Rock", style=discord.ButtonStyle.primary,emoji="✊")
    Pbutton = Button(label="Paper", style=discord.ButtonStyle.primary,emoji="✋")
    Sbutton = Button(label="Scissors", style=discord.ButtonStyle.primary,emoji="✌")
    Banbutton = Button(label="Banana", style=discord.ButtonStyle.primary,emoji="🍌")
    async def Rock(interaction):
        await interaction.response.send_message(roshambo("Rock"))
    async def Paper(interaction):
        await interaction.response.send_message(roshambo("Paper"))
    async def Scissor(interaction):
        await interaction.response.send_message(roshambo("Scissors"))
    async def Banana(interaction):
        await interaction.response.send_message(roshambo("Banana"))
    Rbutton.callback = Rock
    Pbutton.callback = Paper
    Sbutton.callback = Scissor
    Banbutton.callback = Banana
    view = View()
    
    view.add_item(Rbutton)
    view.add_item(Pbutton)
    view.add_item(Sbutton)
    view.add_item(Banbutton)
    await ctx.send("Rock, Paper, Scissors!", view=view)


if __name__ == "__main__":
    load_dotenv()
    client.run(os.getenv('TOKEN'))
