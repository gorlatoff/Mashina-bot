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
    the_message = re.sub(r'(?<!\])\(([^)]*)\)', lambda m: f'\\({m.group(1)}\\)', the_message)
    the_message = re.sub(r'\[(.*?)\]\((.*?)\)', lambda m: f'[{m.group(1)}](<{m.group(2)}>)', the_message)
    await ctx.send( the_message)
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

        results = await isv.mashina_search(slova, lang)
        for text in results:
            text = text.replace("<", "").replace(">", "")
            await sendmessage(ctx, public, text)
    except:
        await ctx.send("Nažalj, moj programist ne primětil někaku pogrěšku. Mečtam o času, kogda roboti počnut pisati svoj kod sami.")

@bot.command(aliases=['wiki', 'wiki1', 'wiki2', 'wiki_summary'])
async def wikipedia_handler(ctx):
    # try:
    if ' ' not in ctx.message.content:
        await ctx.send( "Priměr korektnogo prikaza: `.wiki be Вайна з эму`")

    public, text = check_public(ctx.message.content)

    lang, slova = bots.command_splitter(ctx.message.content, 2)

    if lang not in wiki.SUPPORTED_WIKIS:
        await sendmessage(ctx, public, "Ne znajemy jezyk")
        return

    if "wiki2" in ctx.message.content or "wiki_summary" in ctx.message.content:
        result = await wiki.wiki_summary(lang, slova)
    else:
        result = await wiki.wiki_titles(lang, slova)

    if result:
        print(result)
        if len(result) > 3000:
            for chunk in [result[i:i+3000] for i in range(0, len(result), 3000)]:
                await sendmessage(ctx, public, chunk)
            return
        await sendmessage(ctx, public, result)
        return
    noresult = f"V Wikipediji nema teksta o prědmetu `{slova}`, ili on ne imaje prěvody na druge jezyky. Gledati v naših slovnikah: `.{lang} {text}`"
    await sendmessage(ctx, public, noresult)
    # except:
    #     await ctx.send( "Nažalj, moj programist ne primětil někaku pogrěšku. Mečtam o času, kogda roboti počnut pisati svoj kod sami.")

with open('pouky.yaml', encoding="UTF-8") as fh:
    pouky_data = yaml.load(fh, Loader=yaml.FullLoader)

def pouka_render(pouky_data, name, command):
    name = str(name)
    result = pouky_data[name]["text"]
    if "image" in pouky_data[name]:
        image_link = f"[_____________]({pouky_data[name]["image"]})\n"
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

bot.run(settings['test_token_discord'])