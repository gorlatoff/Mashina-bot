import isv_tools as isv
from work_with_wiki import *
from bot_config import *
import bots
import discord
from discord.ext import commands

slovnik_loaded = False
words = False 
suggestions = False
discord_fraznik = False
korpus_loaded = False
words_general = False

def load_data(update):
    global slovnik_loaded, words, suggestions, discord_fraznik, korpus_loaded, words_general 
       
    slovnik_loaded = isv.load_slovnik(obnoviti=update)   
    words = isv.prepare_slovnik(slovnik_loaded['words']) 
    suggestions = isv.prepare_slovnik(slovnik_loaded['suggestions']) 
    discord_fraznik = isv.load_discord_fraznik()
    korpus_link = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRz8l3w4h--36bUS-5plpkkVLnSFmCPIB3WnpDYRer87eirVVMYfI-ZDbp3WczyL2G5bOSXKty2MpOY/pub?output=xlsx'    
    korpus_loaded = isv.load_sheet(tabela_name="korpus", sheet_names=['words (general)'], tabela=korpus_link, obnoviti= update )
    words_general = isv.prepare_slovnik(korpus_loaded['words (general)'])

load_data(False)

def embed_words(i):
    columns = "en ru be uk pl cs sk bg mk sr hr sl".split(" ")
    words = slovnik_loaded['words']
    kartka = ""
 
    for col in columns:
        kartka = kartka + f"**`{col}` **{ bots.formatizer(words[col][i]) }\n" 
    
    embed = discord.Embed( title=f"{i+2} v slovniku ", url = bots.link_na_slovo(i, "words") )
    embed.add_field(name=f"{ bots.formatizer( words['isv'][i] )}\n", value=f"{kartka} ", inline=False)
    embed.set_footer(text = f"ID: {words['id'][i]}")
    return embed


def embed_suggestions(i):
    columns = "en ru be uk pl cs sk bg mk sr hr sl".split(" ")
    suggestions = slovnik_loaded['suggestions']
    kartka = ""

    for col in columns:
        kartka = kartka + f"**`{col}` **{ bots.formatizer(suggestions[col][i]) }\n" 
    
    embed = discord.Embed( title=f"{i+2} v spisu novyh slov ", url = bots.link_na_slovo(i, "suggestions"))

    if suggestions['isv'][i] == " ":
        suggestions['isv'][i] = "_____"

    embed.add_field(name=f"{suggestions['isv'][i]}\n", value=f"{kartka} ", inline=False)
    embed.set_footer(text = f"Avtor: {suggestions['kto dodal'][i]}, ID: {suggestions['id'][i]}")
    return embed



def embed_korpus(i):
    columns = "en ru be uk pl cs sk bg mk sr hr sl".split(" ")
    korpus = korpus_loaded['words (general)']
    kartka = ''

    for col in columns:
        kartka = kartka + f"**`{col}` **{ bots.formatizer(korpus[col][i]) }\n" 
    
    embed = discord.Embed( title=f"{i+2} v korpusu slov", url = f"https://docs.google.com/spreadsheets/d/1rBG7brwbG4pR1j8_eVZapFZUSdaegSVjDH2V6Oqy00A/edit#gid=281935577&range={i+2}:{i+2}")

    if korpus['isv'][i] == " ":
        korpus['isv'][i] = "_____"

    embed.add_field(name=f"{korpus['isv'][i]}\n", value=f"{kartka} ", inline=False)
    embed.set_footer(text = "Ako li hčeš pomogti v rabotě nad tabeloju, piši do @Neudržima Mašina Dobra")
    return embed



def embed_discord_list(i, tabela):
    embed = discord.Embed( title="Rezultat iz Discord fraznika:", url='https://docs.google.com/spreadsheets/d/1lxLtsJIi-MjimKok7iXHEaAhUFsICq9ePZPPWWCmcBE/edit#gid=0')
    columns = tabela.columns[0:8]
    for col in columns:
        cell = tabela[col][i]
        if cell != " ":
            embed.add_field(name=f"{ col }\n", value=f"{tabela[col][i]} ", inline=False)
    return embed


bot = commands.Bot(command_prefix = settings['prefix']) 
from pouky import *

@bot.command(name = "fraznik", aliases = ['фразник'])
async def najdti_vo_frazniku(ctx):
    text = ctx.message.content

    alias = text.split(" ")[0]
    start = len(f"{alias} ")
    slova = text[start:len(text)]
    print(slova)
    slova = isv.transliteracija(slova, "isv")

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
        for i in najdeno_v_discord_listu:
            await ctx.send( embed = embed_discord_list(i, discord_fraznik['tabela']) )  
        return True
    if najdeno_v_discord_listu2:
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
        return True
    else:
        await channel.send( the_message)
        return True

def embed_words_list(najdene_slova):
    embed = discord.Embed()
    result = "\n\n"
    for i in najdene_slova:
        word_id = f"`.id {slovnik_loaded['words']['id'][i]}` "
        new_word = slovnik_loaded['words']['isv'][i] + f" ({word_id})" + "\n"
        if len(result) + len(new_word) < 600:
            result = result + new_word
        else:
            embed.set_footer(text = "I tako dalje....")
            break           
    embed.add_field(name=f"Najdeno {len(najdene_slova)} slov(a)", value=result )    
    return embed


@bot.command( aliases = ['id', 'isv', 'мс', 'ms', 'ru', 'be', 'uk', 'ua', 'pl', 'cs', 'cz', 'sk', 'bg', 'mk', 'sr', 'hr', 'sl', 'ру', 'бе', 'ук', 'бг', 'мк', 'ср', 'en', 'de', 'nl', 'eo' ] )
async def najdtislovo(ctx):
    text = ctx.message.content

    public = False
    if " --public" in text:
        text = text.replace(' --public', '')
        public = True

    # if " --test" in text:
    #     text = text.replace(' --test', '')
    # else: 
    #     return False

    jezycny_kod = bots.commands_reader(text)['jezyk']
    slova = bots.commands_reader(text)['slova']    

    if (slova == "") or (slova == " "):
        await ctx.send( f"jezyk: {jezycny_kod}, slovo: ne jest zadano" ) 
        return False

    limit = 4
    najdeno_v_discord_listu = []
    
    if jezycny_kod == 'isv':
        najdeno_v_discord_listu = isv.iskati_discord('Vse varianty v MS', slova, discord_fraznik['tabela'])
    if jezycny_kod == 'en': 
        najdeno_v_discord_listu = isv.iskati_discord('Slovo na anglijskom', slova, discord_fraznik['tabela'])
    
    if najdeno_v_discord_listu:
        for i in najdeno_v_discord_listu:
            await ctx.send( embed=embed_discord_list(i, discord_fraznik['tabela'] ) )    
        limit = 3 

    print(f"lang {jezycny_kod}, text {slova}")
    najdene_slova_contain = isv.filtr_contain( slova, jezycny_kod, words )  

    if not najdene_slova_contain.empty:
        najdene_slova = isv.iskati(slova, jezycny_kod, najdene_slova_contain)
        if najdene_slova:
            if len(najdene_slova) > limit:
                await sendmessage(ctx, public, embed_words_list(najdene_slova ) )
                return True
            for i in najdene_slova:
                await sendmessage(ctx, public, embed_words(i) )
            return True
     
        najdene_slova = isv.iskati_slovo(slova, jezycny_kod, najdene_slova_contain) 
        if najdene_slova:
            if len(najdene_slova) == 1: 
                await sendmessage(ctx, public, embed_words(i) )
            else:
                await sendmessage(ctx, public, embed_words_list(najdene_slova))
        elif len(slova) == 1:
            pass
        else:
            najdene_slova = najdene_slova_contain.index
            if len(najdene_slova) == 1:
                await sendmessage(ctx, public, embed_words(najdene_slova[0]) )
            else:
                await sendmessage(ctx, public, embed_words_list(najdene_slova ))

    if jezycny_kod == 'id':
        slova = slova.upper()      
      
    najdene_slova_suggestions = isv.search_in_sheet(slova, jezycny_kod, suggestions)
    if najdene_slova_suggestions:
        for i in najdene_slova_suggestions:
            await ctx.send(embed=embed_suggestions(i))  
            return True 
    
    najdene_slova_korpus = isv.search_in_sheet( slova, jezycny_kod, words_general )  
    if najdene_slova_korpus: 
        for i in najdene_slova_korpus:
            await ctx.send(embed=embed_korpus(i))
            return True   
    
    if najdene_slova_contain.empty:
        if jezycny_kod not in ['isv', 'id']:
            wiki = wiki_titles(jezycny_kod, slova)
            if wiki != False:
                await sendmessage(ctx, public, wiki )
                return True
            await sendmessage(ctx, public, f"Ničto ne jest najdeno. Ale tobě mogut pomogti Glosbe: {bots.glosbe(slova, jezycny_kod)} i Nicetranslator: {bots.nicetranslator(slova)} `")  
            return False  
        await sendmessage(ctx, public, f"Ničto ne jest najdeno.")    
    

@bot.command(name = 'wiki')
async def wiki1(ctx):                 
    text = ctx.message.content
    public = False
    if " --public" in text:
        text = str.replace(text,' --public', '')
        public = True

    jezyk = text.split(" ")[1]
    jezyk = isv.transliteracija(jezyk, 'kir_to_lat')

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
    jezyk = isv.transliteracija(jezyk, 'kirilicna_zamena')

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

@bot.command(aliases = ['obnoviti', 'обновити', 'obnovi', 'обнови'])
async def obnovjenje(ctx):
    global slovnik_loaded, words, suggestions, discord_fraznik, korpus_loaded, words_general      
    text = ctx.message.content
    text = isv.transliteracija(text, 'kir_to_lat')
    if "slovnik" in text:
        await ctx.send("Dostava slovnika...")  
        slovnik_loaded = isv.load_slovnik(obnoviti=True)   
        words = isv.prepare_slovnik(slovnik_loaded['words']) 
        suggestions = isv.prepare_slovnik(slovnik_loaded['suggestions']) 
        await ctx.send("Obnovjenje slovnika jest uspěšno skončeno")
        return True
    if "fraznik" in text:
        await ctx.send("Dostava fraznika...")  
        discord_fraznik = isv.load_discord_fraznik()
        await ctx.send("Obnovjenje fraznika jest uspěšno skončeno")
        return True
    if "korpus" in text:
        await ctx.send("Dostava korpusa slov...")    
        korpus_link = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRz8l3w4h--36bUS-5plpkkVLnSFmCPIB3WnpDYRer87eirVVMYfI-ZDbp3WczyL2G5bOSXKty2MpOY/pub?output=xlsx'    
        korpus_loaded = isv.load_sheet(tabela_name="korpus", sheet_names=['words (general)'], tabela=korpus_link, obnoviti=True )
        words_general = isv.prepare_slovnik(korpus_loaded['words (general)'])
        await ctx.send("Obnovjenje korpusa jest uspěšno skončeno")
        return True
    await ctx.send("Ide obnovjenje...")
    load_data(True)
    await ctx.send("Obnovjenje jest uspěšno skončeno")


 
bot.run(settings['token'])
