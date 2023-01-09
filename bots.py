import isv_tools as isv

langs_aliases = ['id', 'isv', 'мс', 'ms', 'ru', 'be', 'uk', 'ua', 'pl', 'cs', 'cz', 'sk', 'bg', 'mk', 'sr', 'hr', 'sl', 'ру', 'бе', 'ук', 'бг', 'мк', 'ср', 'en', 'de', 'nl', 'eo' ]

def commands_reader(text):
    text = str.replace(text,'  ', ' ')
    jezycny_kod = text.split(" ")[0]
    jezycny_kod = jezycny_kod[1:]
    jezycny_kod = isv.transliteracija(jezycny_kod, 'kirilicna_zamena')

    start = len(text.split(" ")[0] + " ")
    slova = text[start:len(text)]
    slova = str.replace(slova,'!', '')
    slova = slova.lower()    
    if jezycny_kod == "isv":
        slova = isv.transliteracija(slova, 'kir_to_lat')
    slova = isv.transliteracija(slova, jezycny_kod)
    print(f"jezyk = '{jezycny_kod}', slova = '{slova}'")
    return {"slova": slova, "jezyk": jezycny_kod}

 
def formatizer(slovo, botplatform = "discord"):
    if slovo[-1] == ' ':
        slovo = slovo[0:-1]
        
    if '!' not in slovo[0:1]:
        return f" {slovo}"
    if '! ' == slovo[0:2]:
        slovo = str.replace(slovo, '! ', '!')

    slovo = slovo[1:len(slovo)]

    if botplatform == "discord":
        return f" ~{slovo}"
    if botplatform == "telegram":    
        return f" _~{slovo}_"
    else:
        print("error")
        
def link_na_slovo(i, sheetname: str):
    match sheetname:
        case "words": return f"https://docs.google.com/spreadsheets/d/1N79e_yVHDo-d026HljueuKJlAAdeELAiPzdFzdBuKbY/edit#gid=1987833874&range={i+2}:{i+2}"
        case "korpus": return f"https://docs.google.com/spreadsheets/d/1rBG7brwbG4pR1j8_eVZapFZUSdaegSVjDH2V6Oqy00A/edit#gid=281935577&range={i+2}:{i+2}"
        case "suggestions": return f"https://docs.google.com/spreadsheets/d/1N79e_yVHDo-d026HljueuKJlAAdeELAiPzdFzdBuKbY/edit#gid=1226657383&range={i+2}:{i+2}"
    return False

import urllib.parse
def nicetranslator(word):
    url = urllib.parse.quote_plus(word)
    return f"https://nicetranslator.com/translation/ru,be,uk,pl,cs,sk,bg,mk,sr,hr,sl/{url}"



from random import randrange
def glosbe(slova, jezycny_kod):
    jezyky_slovnika_slav = "ru uk pl cs bg sr".split(" ")
    if jezycny_kod in jezyky_slovnika_slav:
        jezyky_slovnika_slav.remove(jezycny_kod)
    jezyk2 = jezyky_slovnika_slav[ randrange( 0,len(jezyky_slovnika_slav) ) ]
    
    glosbe = slova.replace(" ", "%20")
    return f'https://glosbe.com/{jezycny_kod}/{jezyk2}/{ glosbe }'

