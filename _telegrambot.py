import re
import asyncio
import yaml
from telebot.async_telebot import AsyncTeleBot
import lang_detect
import wiki
import transliteration as transl
import isv_tools as isv
import bots
from bot_config import *


bot = AsyncTeleBot(settings['token_telegram'])


@bot.message_handler(commands=['obnovi', 'обнови'])
async def handle_update(message):
    try:
        await reply(message, "Ide obnovjenje")
        text = message.text.lower()
        isv.update_sheets(text)
        await reply(message, "Obnovjenje jest skončeno")
    except:
        await reply(message, "Nažalj, moj programist ne primětil někaku pogrěšku. Mečtam o času, kogda roboti počnut pisati svoj kod sami.")


async def reply(message, text, is_disable=False):
    print(text)
    text = text.replace("`.", "`/")
    text = text.replace("(", r"\(")
    text = text.replace(")", r"\)")

    #De-escape markdown links
    pattern = r'(?<=\])\\(\()(.+?)\\(\))'
    text = re.sub(pattern, lambda match: f'{match.group(1)}{match.group(2)}{match.group(3)}', text)

    text = text.replace(r'\*\*', '__TEMP__')
    text = text.replace(r'\*', r'\\_')
    text = text.replace(r'__TEMP__', '*')

    text = re.sub(r'^(#+)\s*(.+)', r'*\2*', text, flags=re.MULTILINE) # headers to bold

    text = text.replace("_", r"\_")
    text = text.replace("/", r"\/")
    text = text.replace(".", r"\.")
    text = text.replace("#", r"\#")
    text = text.replace("!", r"\!")
    text = text.replace("-", r"\-")
    text = text.replace("=", r"\=")

    text = text.replace("@Mašina", r"@mashina\_slovnik\_bot")
    await bot.reply_to(message, text, parse_mode="MarkdownV2", disable_web_page_preview=is_disable)
    return True


@bot.message_handler(commands=['id', 'isv', 'мс', 'ms', 'ru', 'be', 'uk', 'ua', 'pl', 'cs', 'cz', 'sk', 'bg', 
                               'mk', 'sr', 'hr', 'sl', 'ру', 'бе', 'ук', 'бг', 'мк', 'ср', 'en', 'de', 'nl', 'eo'])
async def handle_najdtislovo(message):
    try:
        if ' ' not in message.text:
            await reply(message, "Priměr korektnogo prikaza: `/pl kurva`", is_disable=True)
        lang, slova = bots.command_splitter(message.text, 1)
        results = await isv.mashina_search(slova, lang)
        for text in results:
            text = text.replace("<", "").replace(">", "")
            await reply(message, text, is_disable=True)
    except:
        await reply(message, "Nažalj, moj programist ne primětil někaku pogrěšku. Mečtam o času, kogda roboti počnut pisati svoj kod sami.")


@bot.message_handler(commands=['wiki', 'wiki1', 'wiki2', 'wiki_summary'])
async def handle_wikipedia(message):
    try:
        if ' ' not in message.text:
            await reply(message, "Priměr korektnogo prikaza: `/wiki be Вайна з эму`", is_disable=True)

        lang, slova = bots.command_splitter(message.text, 2)

        if lang not in wiki.SUPPORTED_WIKIS:
            await bot.reply_to(message, "Ne znajemy jezyk")
            return

        if "wiki2" in message.text or "wiki_summary" in message.text:
            result = await wiki.wiki_summary(lang, slova)
        else:
            result = await wiki.wiki_titles(lang, slova)

        if result:
            if len(result) > 3000:
                for chunk in [result[i:i+3000] for i in range(0, len(result), 3000)]:
                    await bot.reply_to(message, chunk)
                return
            await reply(message, result)
            return
        noresult = f"V Wikipediji nema teksta o prědmetu `{slova}`, ili on ne imaje prěvody na druge jezyky. Gledati v naših slovnikah: `.{lang} {slova}`"
        await reply(message, noresult)
    except:
        await reply(message, "Nažalj, moj programist ne primětil někaku pogrěšku. Mečtam o času, kogda roboti počnut pisati svoj kod sami.")

with open('pouky.yaml', encoding="UTF-8") as fh:
    pouky_data = yaml.load(fh, Loader=yaml.FullLoader)

async def pouka_render(pouky_data, name, command):
    name = str(name)
    result = pouky_data[name]["text"]
    if "image" in pouky_data[name]:
        image_link = "[​](<link>)\n".replace("link", pouky_data[name]["image"])
        result = image_link + result
    if lang_detect.checkalphabet(command) == 'latin':
        result = transl.transliteration2(result, 'kir_to_lat')
    return result

@bot.message_handler(commands=['fraznik', 'фразник'])
async def handle_fraznik(message):
    try:
        lang, slova = bots.command_splitter(message.text, 2)

        results = isv.phrasebook(slova, lang)

        for text in results:
            text = text.replace("<", "").replace(">", "")
            await reply(message, text, is_disable=True)
    except:
        await reply(message, "Nažalj, moj programist ne primětil někaku pogrěšku. Mečtam o času, kogda roboti počnut pisati svoj kod sami.")



@bot.message_handler(commands=['start','help', 'pomoč', 'помоч'])
async def handle_help(message):
    text = pouka_render(pouky_data, "help", "latin")
    await reply(message, text)

@bot.message_handler(commands=['pouka1', 'поука1', 'линкы', 'линкы1', 'транслитератор', 'граматика', 'linky', 'linky1', 'transliterator', 'gramatika'])
async def handle_pouka1(message):
    await reply(message, pouka_render(pouky_data, "pouka1", message.text))

@bot.message_handler(commands=['pouka2', 'поука2', 'линкы2', 'linky2'])
async def handle_pouka2(message):
    await reply(message, pouka_render(pouky_data, "pouka2", message.text))

@bot.message_handler(commands=['pouka3', 'поука3', 'пасивно_ученје', 'pasivno_učenje'])
async def handle_pouka3(message):
    await reply(message, pouka_render(pouky_data, "pouka3", message.text))

@bot.message_handler(commands=['pouka4', 'поука4', 'како_учити', 'kako_učiti'])
async def handle_pouka4(message):
    await reply(message, pouka_render(pouky_data, "pouka4", message.text))

@bot.message_handler(commands=['pouka5', 'поука5', 'словник1', 'словник', 'slovnik1', 'slovnik'])
async def handle_pouka5(message):
    await reply(message, pouka_render(pouky_data, "pouka5", message.text))

@bot.message_handler(commands=['pouka6', 'поука6', 'словник2', 'slovnik2'])
async def handle_pouka6(message):
    await reply(message, pouka_render(pouky_data, "pouka6", message.text))

@bot.message_handler(commands=['pouka7', 'поука7', 'о_фразнику', 'o_frazniku'])
async def handle_pouka7(message):
    await reply(message, pouka_render(pouky_data, "pouka7", message.text))

@bot.message_handler(commands=['pouka8', 'поука8', 'о_боту', 'o_botu'])
async def handle_pouka8(message):
    await reply(message, pouka_render(pouky_data, "pouka8", message.text))

@bot.message_handler(commands=['pouka9', 'поука9', 'keyboards', 'клавиатуры', 'klaviatury'])
async def handle_pouka9(message):
    await reply(message, pouka_render(pouky_data, "pouka9", message.text))


async def main():
    await bot.polling(none_stop=True)
#    await bot.infinity_polling()

if __name__ == "__main__":
    print("Bot jest gotovy")
    asyncio.run(main())
