from work_with_wiki import *
from transliterations import *
from bot_config import *

import discord
from discord.ext import commands
from pandas import read_excel
import re




def update_slovnik():
    print("list aploduje se")
    global dfs
    dfs = read_excel(io='https://docs.google.com/spreadsheets/d/e/2PACX-1vQlOf_9YqxCzwFLX6roaz1xQctVW5CTpWpGWUjkJPxWRbsubZP019-qg3KZrBF55RNza1CgVHKDQ7yb/pub?output=xlsx',
                    engine='openpyxl',
                    sheet_name=['words', 'suggestions'])
    dfs['suggestions'].columns = dfs['suggestions'].iloc[0]
    dfs['suggestions'].reindex(dfs['suggestions'].index.drop(0))
    dfs['suggestions'].rename(columns={'ids': 'id'}, inplace=True)

    dfs['words']['id'] = dfs['words']['id'].fillna(0.0).astype(int)
    dfs['suggestions']['isv'] = dfs['suggestions']['isv'].fillna("___").astype(str)
    print("list slov je obnovjeny")
    
 

def iskati(jezyk, slovo, sheet):
    najdene_slova = []
    for i in range(1, len(sheet['isv'])):
        cell = str( sheet[jezyk][i] )
        cell = str.replace( cell, '!', '')
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
        cell = cell.lower()
        cell = transliteration[jezyk](cell)

        if slovo in str.split( re.sub(r'[^\w\s]','', cell) ):
            najdene_slova.append(i)
    return najdene_slova



def formatizer(slovo):
    if slovo[-1] == ' ':
        slovo = slovo[0:-1]
    if '!' not in slovo[0:1]:
        return f" {slovo}"
    if '! ' == slovo[0:2]:
        slovo = str.replace(slovo, '! ', '!')

    slovo = slovo[1:len(slovo)]
    return f" *{slovo}* "


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
    
    embed = discord.Embed( title=f"{i+2} v listu prědloženij ", url = f"https://docs.google.com/spreadsheets/d/1N79e_yVHDo-d026HljueuKJlAAdeELAiPzdFzdBuKbY/edit#gid=1226657383&range={i+2}:{i+2}")

    if not suggestions['isv'][i]:
        suggestions['isv'][i] = "_____"

    embed.add_field(name=f"{suggestions['isv'][i]}\n", value=f"{kartka} ", inline=False)
    embed.set_footer(text = f"Avtor: {suggestions['kto dodal'][i]}, ID: {suggestions['id'][i]}")
    return embed


bot = commands.Bot(command_prefix = settings['prefix']) 


@bot.event
async def on_ready():
    print("Bot jest gotovy")
   

@bot.command(aliases = ['Hello', 'Pozdrav', 'Zdrav', 'Zdrav,', 'hello', 'pozdrav', 'zdrav', 'zdrav,'])
async def pozdravjenje(ctx):                    # Создаём функцию и передаём аргумент ctx.
    author = ctx.message.author                 # Объявляем переменную author и записываем туда информацию об авторе.
    await ctx.send(f'Zdrav, {author.mention}!') 
    
   
@bot.command(aliases = ['id', 'мс', 'ms', 'ru', 'be', 'uk', 'ua', 'pl', 'cs', 'cz', 'sk', 'bg', 'mk', 'sr', 'hr', 'sl', 'ру', 'бе', 'ук', 'бг', 'мк', 'ср', 'en', 'de', 'nl', 'eo' ])
async def najdtislovo(ctx):
    text = ctx.message.content
    print(text)
    text = str.replace(text,'  ', ' ')
    jezycny_kod = text[1:3]
    jezycny_kod = kirilicna_zamena(jezycny_kod)
    slova = text[4:len(text)]
    slova = str.replace(slova,'!', '')
    slova = slova.lower()


    slova = transliteration[jezycny_kod](slova)

    najdene_slova = iskati(jezycny_kod, slova, dfs['words'])
    if najdene_slova:
        if len(najdene_slova) > 4:
            await ctx.send( f"Sut prěmnogo sinonimov:" )
            for i in najdene_slova:
                await ctx.send( f"{dfs['words']['isv'][i]}, <https://docs.google.com/spreadsheets/d/1N79e_yVHDo-d026HljueuKJlAAdeELAiPzdFzdBuKbY/edit#gid=1987833874&range={i}:{i}>" )
        else:
            for i in najdene_slova:
                await ctx.send( embed=embed_words(i) )
            return True
    else:
        najdene_slova = iskati_slovo(jezycny_kod, slova, dfs['words']) 
        if najdene_slova: 
            await ctx.send(f'Imamo jedino:')
            for i in najdene_slova:
                await ctx.send( f"{dfs['words']['isv'][i]}, <https://docs.google.com/spreadsheets/d/1N79e_yVHDo-d026HljueuKJlAAdeELAiPzdFzdBuKbY/edit#gid=1987833874&range={i}:{i}>" )
    najdene_slova_suggestions = iskati_slovo(jezycny_kod, slova, dfs['suggestions'])
    if najdene_slova_suggestions:
        for i in najdene_slova_suggestions:
            await ctx.send(embed=embed_suggestions(i)) 
        return True

    wiki = wiki_titles(jezycny_kod, slova)
    if wiki != False:
        await ctx.send( wiki )
        return True
    await ctx.send("Nažalost, ničto ne jest najdeno.")    


    
@bot.command(aliases = ['kill'])
async def killbot(ctx):
    await ctx.send("Bot jest obstanovjeny")
    await bot.close()


@bot.command(aliases = ['wiki'])
async def wiki1(ctx): 
    await ctx.send(f'Čekaj, to trěbuje časa')                         
    text = ctx.message.content
    jezyk = text.split(" ")[1]
    jezyk = kirilicna_zamena(jezyk)

    start = len("wiki" + " " + jezyk) + 1
    fraza = text[start:len(text)]

    result = wiki_titles(jezyk, fraza)
    if result == False:
        await ctx.send("ne znajemy problem")
        await ctx.send(f"fraza = {fraza},\n jezyk = {jezyk} ")
        return
    await ctx.send(result)


@bot.command(aliases = ['wiki_summary'])
async def wiki2(ctx): 
    await ctx.send(f'Čekaj, to trěbuje časa')                         
    text = ctx.message.content
    jezyk = text.split(" ")[1]
    jezyk = kirilicna_zamena(jezyk)

    start = len("wiki_summary" + " " + jezyk) + 1
    fraza = text[start:len(text)]

    result = wiki_text(jezyk, fraza)
    if result == False:
        await ctx.send("ne znajemy problem\n fraza = {fraza},\n jezyk = {jezyk}")
        return

    if int(len(result)) > 1990:
        for i in result.split("\n"):
            if len(i) > 3:
                await ctx.send(i)
        return True
    await ctx.send(result)




@bot.command(aliases = ['komandy', 'Komandy', 'commands', 'Commands'])
async def pomogti(ctx):
    text = """
iskati po jezyku:
`.ms krugly stol` 
`.ср разумети`, i tako dalje

gleděti slovo po id:
`.id 474`

iskati vo wiki:
`.wiki en katana`
`.wiki_summary ru собака`

avtomatičny prěvod:
`.prěvod_lite fr Allons enfants de la Patrie,
Le jour de gloire est arrivé!
Contre nous de la tyrannie
L'étendard sanglant est levé`

Od problemov: 
`.kill`
    """
    await ctx.send(text) 




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






