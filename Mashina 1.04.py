#cd C:\Mashina\Mashina-bot

from work_with_wiki import *
from transliterations import *
from bot_config import *
from py_translators import *

import discord
from discord.ext import commands
from pandas import read_excel
import re




def update_slovnik():
    print("list aploduje se")
    global dfs
    dfs = read_excel(io='https://docs.google.com/spreadsheets/d/e/2PACX-1vRsEDDBEt3VXESqAgoQLUYHvsA5yMyujzGViXiamY7-yYrcORhrkEl5g6JZPorvJrgMk6sjUlFNT4Km/pub?output=xlsx',
                    engine='openpyxl',
                    sheet_name=['words', 'suggestions'])
    
    dfs['suggestions'].columns = dfs['suggestions'].iloc[0]
    dfs['suggestions'].reindex(dfs['suggestions'].index.drop(0))
    dfs['suggestions'].rename(columns={'ids': 'id'}, inplace=True)
    #dfs['suggestions']['isv'] = dfs['suggestions']['isv'].fillna("___").astype(str)

    for name in dfs['suggestions'].columns:
        dfs['suggestions'][name] = dfs['suggestions'][name].fillna(" ").astype(str)
        
        
    dfs['words']['id'] = dfs['words']['id'].fillna(0.0).astype(int)

    print("list slov je obnovjeny")
    
 

def iskati(jezyk, slovo, sheet):
    najdene_slova = []
    for i in range(1, len(sheet['isv'])):
        cell = str( sheet[jezyk][i] )
        cell = str.replace( cell, '!', '')
        cell = str.replace( cell, '#', '')
        cell = cell.lower()
        cell = transliteration[jezyk](cell)
        if slovo in str.split( cell, ', ' ):
            najdene_slova.append(i)
    return najdene_slova


def iskati_slovo(jezyk, slovo, sheet):
    najdene_slova = []
    for i in range(1, len(sheet['isv'])):
        cell = str(sheet[jezyk][i])
        cell = str.replace( cell, '!', '')
        cell = str.replace( cell, '#', '')
        cell = cell.lower()
        cell = transliteration[jezyk](cell)
        if slovo in str.split( re.sub(r'[^\w\s]','', cell) ):
            najdene_slova.append(i)
    return najdene_slova



def iskati_any(jezyk, slovo, sheet):
    najdene_slova = []
    for i in range(1, len(sheet['isv'])):
        cell = str( sheet[jezyk][i] )
        cell = str.replace( cell, '!', '')
        cell = str.replace( cell, '#', '')
        cell = cell.lower()
        cell = transliteration[jezyk](cell)
        if slovo in cell:
            najdene_slova.append(i)
    return najdene_slova

# def iskati_contain(jezyk, slovo, sheet):
#     x = sheet[sheet[jezyk].str.contains(slovo, na=False)]
#     return x[x.columns[0]].index  


def formatizer(slovo):
    if slovo[-1] == ' ':
        slovo = slovo[0:-1]
        
    if '!' not in slovo[0:1]:
        return f" {slovo}"
    if '! ' == slovo[0:2]:
        slovo = str.replace(slovo, '! ', '!')

    slovo = slovo[1:len(slovo)]

    return f" *{slovo}*"


def embed_words(i):
    columns = "en ru be uk pl cs sk bg mk sr hr sl".split(" ")
    words = dfs['words']
    kartka = ""
 
    for col in columns:
        kartka = kartka + f"**`{col}` **{ formatizer(words[col][i]) }\n" 
    
    embed = discord.Embed( title=f"{i+2} v slovniku ", url = f"https://docs.google.com/spreadsheets/d/1N79e_yVHDo-d026HljueuKJlAAdeELAiPzdFzdBuKbY/edit#gid=1987833874&range={i+2}:{i+2}") #, color=0xf21f18)
    embed.add_field(name=f"{ formatizer( words['isv'][i] )}\n", value=f"{kartka} ", inline=False)
    embed.set_footer(text = f"ID: {words['id'][i]}")
    return embed


def embed_suggestions(i):
    columns = "en ru be uk pl cs sk bg mk sr hr sl".split(" ")
    suggestions = dfs['suggestions']
    kartka = ""

    for col in columns:
        kartka = kartka + f"**`{col}` **{ formatizer(suggestions[col][i]) }\n" 
    
    embed = discord.Embed( title=f"{i+2} v listu pr??dlo??enij ", url = f"https://docs.google.com/spreadsheets/d/1N79e_yVHDo-d026HljueuKJlAAdeELAiPzdFzdBuKbY/edit#gid=1226657383&range={i+2}:{i+2}")

    if not suggestions['isv'][i]:
        suggestions['isv'][i] = "_____"

    embed.add_field(name=f"{suggestions['isv'][i]}\n", value=f"{kartka} ", inline=False)
    embed.set_footer(text = f"Avtor: {suggestions['kto dodal'][i]}, ID: {suggestions['id'][i]}")
    return embed

def embed_words_list(najdene_slova, text):
    embed = discord.Embed( title=text)
    for i in najdene_slova:
        embed.add_field(name=f"{dfs['words']['isv'][i]}", value=f"[{i+2} v slovniku](https://docs.google.com/spreadsheets/d/1N79e_yVHDo-d026HljueuKJlAAdeELAiPzdFzdBuKbY/edit#gid=1987833874&range={i+2}:{i+2})", inline=False )
    return embed


def embed_words_list_contain(najdene_slova, text):
    embed = discord.Embed( title=text)
    for i in najdene_slova:
        #print(najdene_slova.isv[i])  
        print(dfs['words']['isv'][i])
        embed.add_field(name=f"{dfs['words']['isv'][i]}", value=f"[{i+2} v slovniku](https://docs.google.com/spreadsheets/d/1N79e_yVHDo-d026HljueuKJlAAdeELAiPzdFzdBuKbY/edit#gid=1987833874&range={i+2}:{i+2})", inline=False ) 
        #embed.add_field(name=f"{dfs['words']['isv'][i]}", value=f"[{i+2} v slovniku](https://docs.google.com/spreadsheets/d/1N79e_yVHDo-d026HljueuKJlAAdeELAiPzdFzdBuKbY/edit#gid=1987833874&range={i+2}:{i+2})", inline=False )
        if len(embed) > 5000:
            return embed
    return embed



bot = commands.Bot(command_prefix = settings['prefix']) 


@bot.event
async def on_ready():
    print("Bot jest gotovy")
   

@bot.command(aliases = ['Hello', 'Pozdrav', 'Zdrav', 'Zdrav,', 'hello', 'pozdrav', 'zdrav', 'zdrav,'])
async def pozdravjenje(ctx):                    # ?????????????? ?????????????? ?? ???????????????? ???????????????? ctx.
    author = ctx.message.author                 # ?????????????????? ???????????????????? author ?? ???????????????????? ???????? ???????????????????? ???? ????????????.
    await ctx.send(f'Zdrav, {author.mention}!') 

def commands_reader(text):
    text = str.replace(text,'  ', ' ')
    jezycny_kod = text.split(" ")[0]
    jezycny_kod = str.replace(jezycny_kod,'.', '')
    jezycny_kod = kirilicna_zamena(jezycny_kod)

    start = len(text.split(" ")[0] + " ")
    slova = text[start:len(text)]
    slova = str.replace(slova,'!', '')
    slova = slova.lower()    
    if jezycny_kod == "isv":
        slova = kirilica_do_latinici(slova)
    slova = transliteration[jezycny_kod](slova)
    print(f"jezyk = '{jezycny_kod}', slova = '{slova}'")
    return {"slova": slova, "jezyk": jezycny_kod}

 
   
@bot.command(aliases = ['id', 'isv', 'isl', '????', 'ms', 'ru', 'be', 'uk', 'ua', 'pl', 'cs', 'cz', 'sk', 'bg', 'mk', 'sr', 'hr', 'sl', '????', '????', '????', '????', '????', '????', 'en', 'de', 'nl', 'eo' ])
async def najdtislovo(ctx):
    text = ctx.message.content

    jezycny_kod = commands_reader(text)['jezyk']
    slova = commands_reader(text)['slova']  

    najdene_slova = iskati(jezycny_kod, slova, dfs['words'])
    
    if najdene_slova:
        if len(najdene_slova) > 4:
            await ctx.send( embed=embed_words_list(najdene_slova, "Sut pr??mnogo sinonimov:" ))
            return True
        for i in najdene_slova:
            await ctx.send( embed=embed_words(i) )
        return True

    najdene_slova = iskati_slovo(jezycny_kod, slova, dfs['words']) 
    if najdene_slova: 
        await ctx.send( embed=embed_words_list(najdene_slova, "Imamo jedino:" ))
    else:
        #najdene_slova = iskati_contain(jezycny_kod, slova, dfs['words'])
        najdene_slova = iskati_any(jezycny_kod, slova, dfs['words'])
        #if not najdene_slova.empty:
        if najdene_slova:
            print(f"{slova} najdeno")
            for i in najdene_slova:
                print(i)
            await ctx.send( embed=embed_words_list_contain(najdene_slova, "Imamo jedino:" ))
            return True
            
    najdene_slova_suggestions = iskati_slovo(jezycny_kod, slova, dfs['suggestions'])
    if najdene_slova_suggestions:
        for i in najdene_slova_suggestions:
            await ctx.send(embed=embed_suggestions(i)) 
        return True
    
    if jezycny_kod in SLOVJANSKE_VIKI:
        wiki = wiki_titles(jezycny_kod, slova)
        if wiki != False:
            await ctx.send( wiki )
            return True

    if jezycny_kod == "isv":
        await ctx.send("Na??alost, ni??to ne jest najdeno.")
        return False  
    await ctx.send("Na??alost, ni??to ne jest najdeno. ??ekaj dalje.")    
    await ctx.send(translator_light(jezycny_kod, slova))     


    
@bot.command(aliases = ['kill'])
async def killbot(ctx):
    await ctx.send("Bot jest obstanovjeny")
    await bot.close()

@bot.command(aliases = ['obnoviti', '????????????????'])
async def restartbot(ctx):
    await ctx.send("Slovnik aploduje se")
    update_slovnik()
    await ctx.send("Obnovjenje jest usp????no skon??eno")


@bot.command(aliases = ['wiki'])
async def wiki1(ctx):                 
    text = ctx.message.content
    jezyk = text.split(" ")[1]
    jezyk = kirilicna_zamena(jezyk)

    start = len("wiki" + " " + jezyk) + 1
    fraza = text[start:len(text)]

    if jezyk not in wikis:
        await ctx.send("Ne znajemy jezyk")
        return False

    result = wiki_titles(jezyk, fraza)
    if result == False:
        await ctx.send("Na??alost, ni??to ne jest najdeno")
        #await ctx.send(f"fraza = {fraza},\njezyk = {jezyk} ")
        return
    await ctx.send(result)


@bot.command(aliases = ['wiki_summary'])
async def wiki2(ctx): 
    await ctx.send(f'??ekaj, to tr??buje ??asa')                         
    text = ctx.message.content
    jezyk = text.split(" ")[1]
    jezyk = kirilicna_zamena(jezyk)

    start = len("wiki_summary" + " " + jezyk) + 1
    fraza = text[start:len(text)]

    if jezyk not in wikis:
        await ctx.send("Ne znajemy jezyk")
        return False

    result = wiki_text(jezyk, fraza)
    if result == False:
        await ctx.send("Na??alost, ni??to ne jest najdeno")
        #await ctx.send(f"fraza = {fraza},\njezyk = {jezyk} ")
        return

    if int(len(result)) > 1990:
        for i in result.split("\n"):
            if len(i) > 3:
                await ctx.send(i)
        return True
    await ctx.send(result)



@bot.command(aliases = ['pr??vod_lite'])
async def pr??vod1(ctx):
    await ctx.send(f'??ekaj, to tr??buje ??asa')                             
    text = ctx.message.content
    jezyk = text.split(" ")[1]
    jezyk = kirilicna_zamena(jezyk)

    start = len("pr??vod_lite" + " " + jezyk) + 1
    fraza = text[start:len(text)]

    result = translator_light(jezyk, fraza)
    if result == False:
        await ctx.send("ne znajemy problem\n fraza = {fraza},\n jezyk = {jezyk}")
        return
    await ctx.send(result)


@bot.command(aliases = ['komandy', 'Komandy', 'commands', 'Commands'])
async def pomogti(ctx):
    text = """
iskati po jezyku:
`.ms krugly stol` 
`.???? ????????????????`, i tako dalje

gled??ti slovo po id:
`.id 474`

iskati vo wiki:
`.wiki en katana`
`.wiki_summary ru ????????????`

avtomati??ny pr??vod:
`.pr??vod_lite fr Allons enfants de la Patrie,
Le jour de gloire est arriv??!
Contre nous de la tyrannie
L'??tendard sanglant est lev??`

Od problemov: 
`.obnoviti`
`.kill`
    """
    await ctx.send(text) 



# update_slovnik()
# bot.run(settings['token'])


import schedule
import time
import threading


def scheduler_function():
    while True:
        schedule.run_pending()
        time.sleep(5)

def run_shedule():
    schedule.every(240).minutes.do(lambda:update_slovnik())
    scheduler_function()

def run_bot():
    bot.run(settings['token'])
    

if __name__ == "__main__":

    update_slovnik()

    x = threading.Thread(target=run_shedule)
    y = threading.Thread(target=run_bot)
    
    x.start()
    y.start()

    x.join()
    y.join()






