import yaml
import re
import asyncio
import disnake
from disnake.ext import commands
import lang_detect
import wiki
import transliteration as transl
import isv_tools as isv
import bots
from bot_config import *

bot = commands.Bot(command_prefix='.', help_command=None, intents=disnake.Intents.all())

def check_public(text: str) -> tuple[bool, str]:
    public = False
    if " --public" in text:
        text = text.replace(' --public', '')
        public = True
    return public, text


async def sendmessage(ctx, public, the_message):

    free_channels = {
        "slovnik-bot": 913744290826555442,

        "jedino medžuslovjansky 1": 879438775011385387,
        "jedino medžuslovjansky 2": 881609946553262180,
        "any-language": 918601986428010547,
        "rabotanje zajedno": 1153414647324606484,

        "eksperimentalny ms": 1185114493097885748,
        "grěšky v slovniku": 1138823260444840037,
        "tehnično věče": 1099638006903738379,
        "ideje novyh projektov": 902594298149756999,
        "razvoj ms slovnika": 896807569601986610,

        "o lingvistikě": 879453674605256724,
        "pytanja": 1048229781407281182,
    }

    channel_id = int(ctx.message.channel.id)
    server_id = int(ctx.message.guild.id)
    ms_besěda_id = 879438774323535914


    the_message = re.sub(r'(?<!\])\(([^)]*)\)', lambda m: f'\\({m.group(1)}\\)', the_message)
    the_message = re.sub(r'\[(.*?)\]\((.*?)\)', lambda m: f'[{m.group(1)}](<{m.group(2)}>)', the_message)


    if any([channel_id in free_channels.values(), server_id != ms_besěda_id, public]):
        await ctx.send( the_message)
        return True

    await ctx.send(f"Rezultaty sut v kanalu <#{free_channels['slovnik-bot']}>. Za prizyvanje bota v drugyh kanalah napiši `{ctx.message.content} --public`")

    slovnik_bot = bot.get_channel(free_channels['slovnik-bot'])
    await slovnik_bot.send(the_message)
    return True


@bot.command(aliases=['obnovi', 'обнови'])
async def update(ctx):
    try:
        public, text = check_public(ctx.message.content)
        await sendmessage(ctx, public, "Ide obnovjenje")
        isv.update_sheets(text.lower())
        await sendmessage(ctx, public, "Obnovjenje jest skončeno")
    except:
        await sendmessage(ctx, True, "Nažalj, moj programist ne primětil někaku pogrěšku. Mečtam o času, kogda roboti počnut pisati svoj kod sami.")

@bot.command(aliases=['id', 'isv', 'мс', 'ms', 'ru', 'be', 'uk', 'ua', 'pl', 'cs', 'cz', 'sk', 'bg', 'mk',
                     'sr', 'hr', 'sl', 'ру', 'бе', 'ук', 'бг', 'мк', 'ср', 'en', 'de', 'nl', 'eo'])
async def dictionary_handler(ctx):
    """Search for words in different languages"""
    try:
        if ' ' not in ctx.message.content:
            await ctx.send( "Priměr korektnogo prikaza: `/pl kurva`", is_disable=True)
        public, text = check_public(ctx.message.content)
        lang, slova = bots.command_splitter(ctx.message.content, 1)

        results = isv.mashina_search(slova, lang)
        for text in results:
            text = text.replace("<", "").replace(">", "")
            await sendmessage(ctx, public, text)
    except:
        await ctx.send("Nažalj, moj programist ne primětil někaku pogrěšku. Mečtam o času, kogda roboti počnut pisati svoj kod sami.")

@bot.command(aliases=['wiki', 'wiki1', 'wiki2', 'wiki_summary'])
async def wikipedia_handler(ctx):
    try:
        if ' ' not in ctx.message.content:
            await ctx.send( "Priměr korektnogo prikaza: `.wiki be Вайна з эму`")

        public, text = check_public(ctx.message.content)

        lang, slova = bots.command_splitter(ctx.message.content, 2)

        if lang not in wiki.SUPPORTED_WIKIS:
            await sendmessage(ctx, public, "Ne znajemy jezyk")
            return

        if "wiki2" in ctx.message.content or "wiki_summary" in ctx.message.content:
            result = asyncio.run(wiki.wiki_summary(lang, slova))
        else:
            result = asyncio.run(wiki.wiki_titles(lang, slova))

        if result:
            if len(result) > 3000:
                for chunk in [result[i:i+3000] for i in range(0, len(result), 3000)]:
                    await sendmessage(ctx, public, chunk)
                return
            await sendmessage(ctx, public, result)
            return
        noresult = f"V Wikipediji nema teksta o prědmetu `{slova}`, ili on ne imaje prěvody na druge jezyky. Gledati v naših slovnikah: `.{lang} {text}`"
        await sendmessage(ctx, public, noresult)
    except:
        await ctx.send( "Nažalj, moj programist ne primětil někaku pogrěšku. Mečtam o času, kogda roboti počnut pisati svoj kod sami.")

with open('pouky.yaml', encoding="UTF-8") as fh:
    pouky_data = yaml.load(fh, Loader=yaml.FullLoader)

def pouka_render(pouky_data, name, command):
    name = str(name)
    result = pouky_data[name]["text"]
    if "image" in pouky_data[name]:
        image_link = "[​](<link>)\n".replace("link", pouky_data[name]["image"])
        result = image_link + result
    if lang_detect.checkalphabet(command) == 'latin':
        result = transl.transliteration2(result, 'kir_to_lat')
    return result


@bot.command(aliases=['fraznik', 'фразник'])
async def phrasebook_handler(ctx, lang: str, slova: str):
    """Search in the phrasebook"""
    try:
        public, text = check_public(ctx.message.content)
        if ' ' not in ctx.message.content:
            await sendmessage(ctx, public, "Priměr korektnogo prikaza: `/fraznik ru думать`")

        results = isv.phrasebook(slova, lang)
        for text in results:
            text = text.replace("<", "").replace(">", "")
            await sendmessage(ctx, public, text)
    except:
        await ctx.send( "Nažalj, moj programist ne primětil někaku pogrěšku. Mečtam o času, kogda roboti počnut pisati svoj kod sami.")


@bot.command(aliases = ['поука1', 'линкы', 'линкы1', 'транслитератор', 'граматика', 'linky', 'linky1', 'transliterator', 'gramatika'])
async def pouka1(ctx):
    await ctx.send(pouka_render(pouky_data, "pouka1", "latin"))

@bot.command(aliases = ['поука2', 'линкы2', 'linky2'])
async def pouka2(ctx):
    await ctx.send(pouka_render(pouky_data, "pouka2", "latin"))

@bot.command(aliases = ['поука3', 'пасивно_ученје', 'pasivno_učenje'])
async def pouka3(ctx):
    await ctx.send(pouka_render(pouky_data, "pouka3", "latin"))

@bot.command(aliases = ['поука4', 'како_учити', 'kako_učiti'])
async def pouka4(ctx):
    await ctx.send(pouka_render(pouky_data, "pouka4", "latin"))

@bot.command(aliases = ['поука5', 'словник1', 'словник', 'slovnik1', 'slovnik'])
async def pouka5(ctx):
    await ctx.send(pouka_render(pouky_data, "pouka5", "latin"))

@bot.command(aliases = ['поука6', 'словник2', 'slovnik2'])
async def pouka6(ctx):
    await ctx.send(pouka_render(pouky_data, "pouka6", "latin"))

@bot.command(aliases = ['поука7', 'о_фразнику', 'o_frazniku'])
async def pouka7(ctx):
    await ctx.send(pouka_render(pouky_data, "pouka7", "latin"))

@bot.command(aliases = ['поука8', 'о_боту', 'o_botu'])
async def pouka8(ctx):
    await ctx.send(pouka_render(pouky_data, "pouka8", "latin"))

@bot.command(aliases = ['поука9', 'keyboards', 'клавиатуры', 'klaviatury'])
async def pouka9(ctx):
    await ctx.send(pouka_render(pouky_data, "pouka9", "latin"))

@bot.command(aliases = ['правила', 'pravila'])
async def discord_rules(ctx):
    await ctx.send(pouka_render(pouky_data, 'pravila_discord'))

@bot.command(aliases = ['pomoč', 'помоч'])
async def help(ctx):
    await ctx.send(pouka_render(pouky_data, "help", "latin"))


@bot.event
async def on_ready():
    print("Bot jest gotovy")

bot.run(settings['token_discord'])