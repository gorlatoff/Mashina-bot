import telebot

bot = telebot.TeleBot("5701607715:AAGVDGLpCa7l4NnOEpOxRalCAAJh51WU1z8", parse_mode="Markdown") # You can set parse_mode by default. HTML or MARKDOWN

import isv_tools as isv
from work_with_wiki import *
from bot_config import *
import bots

slovnik_loaded = False
words = False 
suggestions = False
# discord_fraznik = False
korpus_loaded = False
words_general = False

def load_data(update):
    global slovnik_loaded, words, suggestions, discord_fraznik, korpus_loaded, words_general 
       
    slovnik_loaded = isv.load_slovnik(obnoviti=update)   
    words = isv.prepare_slovnik(slovnik_loaded['words']) 
    suggestions = isv.prepare_slovnik(slovnik_loaded['suggestions']) 
    # discord_fraznik = isv.load_discord_fraznik()
    korpus_link = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRz8l3w4h--36bUS-5plpkkVLnSFmCPIB3WnpDYRer87eirVVMYfI-ZDbp3WczyL2G5bOSXKty2MpOY/pub?output=xlsx'    
    korpus_loaded = isv.load_sheet(tabela_name="korpus", sheet_names=['words (general)'], tabela=korpus_link, obnoviti= update )
    words_general = isv.prepare_slovnik(korpus_loaded['words (general)'])

load_data(False)


def handler(event, _):
    message = telebot.types.Update.de_json(event['body'])
    bot.process_new_updates([message])
    return {
        'statusCode': 200,
        'body': '!',
    }


def words_list(najdene_slova):
    result = f"Najdeno {len(najdene_slova)} slov(a): \n\n"
    for i in najdene_slova:
        word_id = f"/id {slovnik_loaded['words']['id'][i]} "
        new_word = slovnik_loaded['words']['isv'][i] + f" (`{word_id}`)" + "\n"
        if len(result) + len(new_word) < 400:
            result = result + new_word
        else:
            result = result + "I tako dalje...."
            return result
    return result        


def markdown_kartka(i, sheet):
    columns = "en ru be uk pl cs sk bg mk sr hr sl".split(" ")
    kartka = sheet['isv'][i] + "\n\n"
    for col in columns:
        kartka = kartka + f"`{col}`{ bots.formatizer(sheet[col][i], 'telegram')}\n" 
    return kartka


@bot.message_handler(commands = bots.langs_aliases)
def najdti(message):
    text = message.text

    jezycny_kod = bots.commands_reader(text)['jezyk']
    slova = bots.commands_reader(text)['slova']    

    if (slova == "") or (slova == " "):
        bot.send_message(message.chat.id, f"jezyk: {jezycny_kod}, slovo: ne jest zadano" ) 
        return False

    limit = 2

    najdene_slova_contain = isv.filtr_contain( slova, jezycny_kod, words )  

    if not najdene_slova_contain.empty:
        najdene_slova = isv.iskati(slova, jezycny_kod, najdene_slova_contain)
        if najdene_slova:
            if len(najdene_slova) > limit:
                bot.send_message(message.chat.id, words_list(najdene_slova) )
                return True
            for i in najdene_slova:
                bot.send_message(message.chat.id, markdown_kartka(i, slovnik_loaded['words']))
            return True

        najdene_slova = isv.iskati_slovo(slova, jezycny_kod, najdene_slova_contain) 
        if najdene_slova: 
            if len(najdene_slova) == 1: 
                bot.send_message(message.chat.id, markdown_kartka(najdene_slova[0], slovnik_loaded['words'])  )
            else:
                bot.send_message(message.chat.id, words_list(najdene_slova) )
        elif len(slova) == 1:
            pass
        else:
            najdene_slova = najdene_slova_contain.index
            if len(najdene_slova) == 1:
                bot.send_message(message.chat.id, markdown_kartka(najdene_slova[0], slovnik_loaded['words'])  )
            else:
                bot.send_message(message.chat.id, words_list(najdene_slova) )
            

    if jezycny_kod == 'id':
        slova = slova.upper()      
      
    najdene_slova_suggestions = isv.search_in_sheet(slova, jezycny_kod, suggestions)
    if najdene_slova_suggestions:
        for i in najdene_slova_suggestions:
            bot.send_message(message.chat.id, markdown_kartka(i, slovnik_loaded['suggestions']))
            return True 
    
    najdene_slova_korpus = isv.search_in_sheet( slova, jezycny_kod, words_general )  
    if najdene_slova_korpus: 
        for i in najdene_slova_korpus:
            bot.send_message(message.chat.id, markdown_kartka(i, korpus_loaded['words (general)']))
            return True   
    
    if najdene_slova_contain.empty:
        if jezycny_kod not in ['isv', 'id']:
            wiki = wiki_titles(jezycny_kod, slova)
            if wiki != False:
                bot.send_message(message.chat.id, wiki)
                return True
            bot.send_message(message.chat.id, f"Ničto ne jest najdeno. Ale tobě mogut pomogti Glosbe: {bots.glosbe(slova, jezycny_kod)} i Nicetranslator: {bots.nicetranslator(slova)} ")    
            return False  
        else:
            bot.send_message(message.chat.id, f"Ničto ne jest najdeno.")    



@bot.message_handler(commands = ["obnoviti", "обновити", "obnovi", "обнови"])
def obnoviti(message):
    global slovnik_loaded, words, suggestions, discord_fraznik, korpus_loaded, words_general 
    text = message.text

    if "slovnik" in text:
        bot.send_message(message.chat.id, "Dostava slovnika...")  
        slovnik_loaded = isv.load_slovnik(obnoviti=True)   
        words = isv.prepare_slovnik(slovnik_loaded['words']) 
        suggestions = isv.prepare_slovnik(slovnik_loaded['suggestions']) 
        bot.send_message(message.chat.id, "Obnovjenje slovnika jest uspěšno skončeno")
        return True
    if "fraznik" in text:
        bot.send_message(message.chat.id, "Dostava fraznika...")  
        discord_fraznik = isv.load_discord_fraznik()
        bot.send_message(message.chat.id, "Obnovjenje fraznika jest uspěšno skončeno")
        return True
    if "korpus" in text:
        bot.send_message(message.chat.id, "Dostava korpusa slov...")    
        korpus_link = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRz8l3w4h--36bUS-5plpkkVLnSFmCPIB3WnpDYRer87eirVVMYfI-ZDbp3WczyL2G5bOSXKty2MpOY/pub?output=xlsx'    
        korpus_loaded = isv.load_sheet(tabela_name="korpus", sheet_names=['words (general)'], tabela=korpus_link, obnoviti=True )
        words_general = isv.prepare_slovnik(korpus_loaded['words (general)'])
        bot.send_message(message.chat.id, "Obnovjenje korpusa jest uspěšno skončeno")
        return True
    bot.send_message(message.chat.id, "Ide obnovjenje...")
    load_data(True)
    bot.send_message(message.chat.id, "Obnovjenje jest uspěšno skončeno")



bot.infinity_polling()
