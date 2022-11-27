import isv_tools as isv
from work_with_wiki import *
import transliterations
from bot_config import *
import asyncio
import discord
from discord.ext import commands

def load_data(update=False):
    global slovnik_loaded, words, suggestions, discord_fraznik 

    slovnik_loaded = isv.load_slovnik(obnoviti=update)   
    words = isv.prepare_slovnik(slovnik_loaded['words']) 
    suggestions = isv.prepare_slovnik(slovnik_loaded['suggestions']) 
    discord_fraznik = isv.load_discord_fraznik()

load_data()

def formatizer(slovo):
    if slovo[-1] == ' ':
        slovo = slovo[0:-1]
        
    if '!' not in slovo[0:1]:
        return f" {slovo}"
    if '! ' == slovo[0:2]:
        slovo = str.replace(slovo, '! ', '!')

    slovo = slovo[1:len(slovo)]

    return f" *{slovo}*"
    

def link_na_slovnik(i):
    return f"https://docs.google.com/spreadsheets/d/1N79e_yVHDo-d026HljueuKJlAAdeELAiPzdFzdBuKbY/edit#gid=1987833874&range={i+2}:{i+2}"


def embed_words(i):
    columns = "en ru be uk pl cs sk bg mk sr hr sl".split(" ")
    words = slovnik_loaded['words']
    kartka = ""
 
    for col in columns:
        kartka = kartka + f"**`{col}` **{ formatizer(words[col][i]) }\n" 
    
    embed = discord.Embed( title=f"{i+2} v slovniku ", url = link_na_slovnik(i) )
    embed.add_field(name=f"{ formatizer( words['isv'][i] )}\n", value=f"{kartka} ", inline=False)
    embed.set_footer(text = f"ID: {words['id'][i]}")
    return embed


def embed_suggestions(i):
    columns = "en ru be uk pl cs sk bg mk sr hr sl".split(" ")
    suggestions = slovnik_loaded['suggestions']
    kartka = ""

    for col in columns:
        kartka = kartka + f"**`{col}` **{ formatizer(suggestions[col][i]) }\n" 
    
    embed = discord.Embed( title=f"{i+2} v spisu novyh slov ", url = f"https://docs.google.com/spreadsheets/d/1N79e_yVHDo-d026HljueuKJlAAdeELAiPzdFzdBuKbY/edit#gid=1226657383&range={i+2}:{i+2}")

    if not suggestions['isv'][i]:
        suggestions['isv'][i] = "_____"

    embed.add_field(name=f"{suggestions['isv'][i]}\n", value=f"{kartka} ", inline=False)
    embed.set_footer(text = f"Avtor: {suggestions['kto dodal'][i]}, ID: {suggestions['id'][i]}")
    return embed

def embed_words_list(najdene_slova, text):
    embed = discord.Embed()
    result = "\n\n"
    if len(najdene_slova) == 1:
        i = najdene_slova[0]
        word_id = f"`.id {slovnik_loaded['words']['id'][i]}` "
        result = f"{word_id}" + slovnik_loaded['words']['isv'][i] + "\n"
        embed.add_field(name="Imamo jedino", value=f"{result}" )
        return embed        
    for i in najdene_slova:
        word_id = f"`.id {slovnik_loaded['words']['id'][i]}` "
        new_word = f"{word_id}" + slovnik_loaded['words']['isv'][i] + "\n"
        if len(result) + len(new_word) < 600:
            result = result + new_word
        else:
            embed.set_footer(text = f"I tako dalje....")
            break           
    embed.add_field(name=f"Najdeno {len(najdene_slova)} slov(a)", value=result )    
    return embed

def embed_discord_list(i, tabela):
    embed = discord.Embed( title="Rezultat iz Discord fraznika:", url='https://docs.google.com/spreadsheets/d/1lxLtsJIi-MjimKok7iXHEaAhUFsICq9ePZPPWWCmcBE/edit#gid=0')
    columns = tabela.columns[0:8]
    for col in columns:
        cell = tabela[col][i]
        if cell != " ":
            embed.add_field(name=f"{ col }\n", value=f"{tabela[col][i]} ", inline=False)
    return embed


def commands_reader(text):
    text = str.replace(text,'  ', ' ')
    jezycny_kod = text.split(" ")[0]
    jezycny_kod = str.replace(jezycny_kod,'.', '')
    jezycny_kod = transliterations.kirilicna_zamena(jezycny_kod)

    start = len(text.split(" ")[0] + " ")
    slova = text[start:len(text)]
    slova = str.replace(slova,'!', '')
    slova = slova.lower()    
    if jezycny_kod == "isv":
        slova = transliterations.kirilica_do_latinici(slova)
    slova = isv.transliteration[jezycny_kod](slova)
    print(f"jezyk = '{jezycny_kod}', slova = '{slova}'")
    return {"slova": slova, "jezyk": jezycny_kod}

bot = commands.Bot(command_prefix = settings['prefix']) 
from pouky import *


@bot.command(name = "fraznik", aliases = ['фразник'])
async def najdti_vo_frazniku(ctx):
    text = ctx.message.content

    alias = text.split(" ")[0]
    start = len(f"{alias} ")
    slova = text[start:len(text)]
    print(slova)
    slova = isv.transliteration["isv"](slova)

    if not slova:
        await ctx.send( "ne jest zadano slovo" ) 
        print( "ne jest zadano slovo" ) 
        return False

    najdeno_v_discord_listu = []

    najdeno_v_discord_listu = isv.iskati_discord('Vse varianty v MS', slova, discord_fraznik['tabela'])
    if not najdeno_v_discord_listu: 
        najdeno_v_discord_listu = isv.iskati_discord('Slovo na anglijskom', slova, discord_fraznik['tabela'])

    najdeno_v_discord_listu2 = isv.iskati_discord('Vse varianty v MS', slova, discord_fraznik['nove slova'])
    if not najdeno_v_discord_listu2: 
        najdeno_v_discord_listu2 = isv.iskati_discord('Slovo na anglijskom', slova, discord_fraznik['nove slova'])
    if najdeno_v_discord_listu:
        print("Najdeno") 
        print( najdeno_v_discord_listu )
        print( najdeno_v_discord_listu[0] )

        for i in najdeno_v_discord_listu:
            await ctx.send( embed = embed_discord_list(i, discord_fraznik['tabela']) )  
        return True
    if najdeno_v_discord_listu2:
        print("Najdeno") 
        print( najdeno_v_discord_listu2 )
        print( najdeno_v_discord_listu2[0] )

        for i in najdeno_v_discord_listu2:
            await ctx.send( embed = embed_discord_list(i, discord_fraznik['nove slova']) )  
        return True
    return await ctx.send( "Ničto ne jest najdeno. Tut možeš uviděti vse slova ktore imajemo https://gorlatoff.github.io/fraznik.html")



async def sendmessage(ctx, public, the_message):
    id_server = False
    try:
        id_server = int( ctx.message.guild.id )
    except:
        pass
    author = ctx.message.author 

    free_channels = [879448889051201626, 886233138194448444, 881826197074481182, 913744290826555442, 879456141887832064]
    if (public == True) or (id_server != 879438774323535914) or ( int(ctx.message.channel.id) in free_channels ):
        if str( type(the_message) ) == "<class 'discord.embeds.Embed'>":    
            await ctx.send( embed=the_message)
            return True
        else:
            await ctx.send( the_message)
            return True
    channel = bot.get_channel(913744290826555442)

    await ctx.send(f"Rezultaty sut v kanalu <#913744290826555442>. Da by vyzvati bota v drugyh kanalah, napiši `{ctx.message.content} --public`")
    await channel.send(f"{author.mention}")

    if str( type(the_message) ) == "<class 'discord.embeds.Embed'>":    
        await channel.send( embed=the_message)
        # await ctx.send( embed=the_message)
        return True
    else:
        await channel.send( the_message)
        # await ctx.send( the_message)
        return True


import urllib.parse
def nicetranslator(word):
    url = urllib.parse.quote_plus(word)
    return f"https://nicetranslator.com/translation/ru,be,uk,pl,cs,sk,bg,mk,sr,hr,sl/{url}"

from random import randrange




@bot.command(aliases = ['id', 'isv', 'мс', 'ms', 'ru', 'be', 'uk', 'ua', 'pl', 'cs', 'cz', 'sk', 'bg', 'mk', 'sr', 'hr', 'sl', 'ру', 'бе', 'ук', 'бг', 'мк', 'ср', 'en', 'de', 'nl', 'eo' ])
async def najdtislovo(ctx):
    text = ctx.message.content

    public = False
    if " --public" in text:
        text = str.replace(text,' --public', '')
        public = True

    jezycny_kod = commands_reader(text)['jezyk']
    slova = commands_reader(text)['slova']    

    if (slova == "") or (slova == " "):
        await ctx.send( f"jezyk: {jezycny_kod}, slovo: ne jest zadano" ) 
        return False

    limit = 3
    najdeno_v_discord_listu = []
    
    if jezycny_kod == 'isv':
        najdeno_v_discord_listu = isv.iskati_discord('Vse varianty v MS', slova, discord_fraznik['tabela'])
    if jezycny_kod == 'en': 
        najdeno_v_discord_listu = isv.iskati_discord('Slovo na anglijskom', slova, discord_fraznik['tabela'])
    
    if najdeno_v_discord_listu:
        print("Najdeno") 
        print( najdeno_v_discord_listu )
        print( najdeno_v_discord_listu[0] )

        for i in najdeno_v_discord_listu:
            await ctx.send( embed=embed_discord_list(i, discord_fraznik['tabela'] ) )    
        limit = 2 

    print(f"lang {jezycny_kod}, text {slova}")
    najdene_slova_contain = isv.filtr_contain( slova, jezycny_kod, words )  
       
    if not najdene_slova_contain.empty:
        najdene_slova = isv.iskati(slova, jezycny_kod, najdene_slova_contain)
        if najdene_slova:
            if len(najdene_slova) > limit:
                await sendmessage(ctx, public, embed_words_list(najdene_slova, "Jest prěmnogo sinonimov:" ) )
                return True
            for i in najdene_slova:
                await sendmessage(ctx, public, embed_words(i) )
            return True
     
        najdene_slova = isv.iskati_slovo(slova, jezycny_kod, najdene_slova_contain) 
        if najdene_slova: 
            await sendmessage(ctx, public, embed_words_list(najdene_slova, "Imamo jedino:" ))
        elif len(slova) == 1:
            pass
        else:
            najdene_slova = najdene_slova_contain.index
            await sendmessage(ctx, public, embed_words_list(najdene_slova, "Imamo jedino:" ))
            #return True
    
    if jezycny_kod == 'id':
        slova = slova.upper()
            
    najdene_slova_suggestions = isv.iskati(slova, jezycny_kod, suggestions)
    if najdene_slova_suggestions:
        for i in najdene_slova_suggestions:
            await ctx.send(embed=embed_suggestions(i))  
        return True            
    najdene_slova_suggestions = isv.iskati_slovo(slova, jezycny_kod, suggestions)
    if najdene_slova_suggestions:
        for i in najdene_slova_suggestions:
            await ctx.send(embed=embed_suggestions(i))   
        return True
    
    if najdene_slova_contain.empty and not najdene_slova_suggestions:

        if jezycny_kod == "isv" or jezycny_kod == "id":
            await sendmessage(ctx, public, "Nažalost, ničto ne jest najdeno.")
            return False   

        wiki = wiki_titles(jezycny_kod, slova)
        if wiki != False:
            await sendmessage(ctx, public, wiki )
            return True
        
        jezyky_slovnika_slav = "ru uk pl cs bg sr".split(" ")
        jezyky_slovnika_slav.remove(jezycny_kod)
        jezyk2 = jezyky_slovnika_slav[ randrange( 0,len(jezyky_slovnika_slav) ) ]
        
        glosbe = slova.replace(" ", "%20")
        
        await sendmessage(ctx, public, f"Ničto ne jest najdeno. Ale tobě mogut pomogti Glosbe: https://glosbe.com/{jezycny_kod}/{jezyk2}/{ glosbe } i Nicetranslator: {nicetranslator(slova)} `")    




@bot.command(name = 'wiki')
async def wiki1(ctx):                 
    text = ctx.message.content
    public = False
    if " --public" in text:
        text = str.replace(text,' --public', '')
        public = True

    jezyk = text.split(" ")[1]
    jezyk = transliterations.kirilicna_zamena(jezyk)

    start = len("wiki" + " " + jezyk) + 1
    fraza = text[start:len(text)]

    if jezyk not in wikis:
        await ctx.send("Ne znajemy jezyk")
        return False
    
    result = wiki_titles(jezyk, fraza)
    if result == False:
        await sendmessage(ctx, public, "Nažalost, ničto ne jest najdeno")
        return False
    await sendmessage(ctx, public, result)


@bot.command(name = 'wiki_summary')
async def wiki2(ctx):   
    text = ctx.message.content
    public = False
    if " --public" in text:
        text = str.replace(text,' --public', '')
        public = True                  

    jezyk = text.split(" ")[1]
    jezyk = isv.kirilicna_zamena(jezyk)

    start = len("wiki_summary" + " " + jezyk) + 1
    fraza = text[start:len(text)]

    if jezyk not in wikis:
        await sendmessage(ctx, public, "Ne znajemy jezyk")
        return False

    result = wiki_text(jezyk, fraza)
    if result == False:
        await sendmessage(ctx, public, "Nažalost, ničto ne jest najdeno")
        return

    await sendmessage(ctx, public, 'Čekaj, to trěbuje časa')     
    if int(len(result)) > 1990:
        for i in result.split("\n"):
            if len(i) > 3:
                await sendmessage(ctx, public, i)
        return True
    await sendmessage(ctx, public, result)


@bot.event
async def on_ready():
    print("Bot jest gotovy")
    
@bot.command(aliases = ['Hello', 'Pozdrav', 'Zdrav', 'Zdrav,', 'hello', 'pozdrav', 'zdrav', 'zdrav,'])
async def pozdravjenje(ctx):                    # Создаём функцию и передаём аргумент ctx.
    author = ctx.message.author                 # Объявляем переменную author и записываем туда информацию об авторе.
    await ctx.send(f'Zdrav, {author.mention}!')     

@bot.command(aliases = ['kill'])
async def killbot(ctx):
    await ctx.send("Bot jest zastanovjeny")
    await bot.close() 

@bot.command(aliases = ['obnoviti'])
async def obnovjenje(ctx):
    await ctx.send("Dostava slovnika...")
    load_data(update=True)
    await ctx.send("Obnovjenje jest uspěšno skončeno")
    
bot.run(settings['token'])
