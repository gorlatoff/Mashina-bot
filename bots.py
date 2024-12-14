import transliteration as transl


def command_splitter(text, max_split_n):
    text = text[1:].split(maxsplit=max_split_n)
    lang = text[-2]
    slova = text[-1]
    lang = transl.transliteration(lang, 'kirilicna_zamena')
    return lang, slova


# command_splitter("/wiki ru test", 2)
# command_splitter("/fraznik en test", 2)
# command_splitter("/en test", 1)
# command_splitter("/en test tests", 1)
# command_splitter("wiki be Вайна з эму", 2)

def formatizer(slovo, botplatform = "discord"):
    if slovo[-1] == ' ':
        slovo = slovo[0:-1]
        
    if '!' not in slovo[0:1]:
        return f" {slovo}"
    if '! ' == slovo[0:2]:
        slovo = str.replace(slovo, '! ', '!')

    slovo = slovo[1:len(slovo)]

    if botplatform == "discord":
        return f" 🤖{slovo}"
    if botplatform == "telegram":    
        return f" 🤖{slovo}"
    else:
        print("error")
    
def link_na_slovo(i, sheetname: str):
    match sheetname:
        case "words": return f"https://docs.google.com/spreadsheets/d/1N79e_yVHDo-d026HljueuKJlAAdeELAiPzdFzdBuKbY/edit#gid=1987833874&range={i+1}:{i+1}"
        case "suggestions": return f"https://docs.google.com/spreadsheets/d/1N79e_yVHDo-d026HljueuKJlAAdeELAiPzdFzdBuKbY/edit#gid=1226657383&range={i+1}:{i+1}"
        case "fraznik": return f"https://docs.google.com/spreadsheets/d/1lxLtsJIi-MjimKok7iXHEaAhUFsICq9ePZPPWWCmcBE/edit#gid=0&range={i+1}:{i+1}"
        case "Wiki list": return f"https://docs.google.com/spreadsheets/d/1rBG7brwbG4pR1j8_eVZapFZUSdaegSVjDH2V6Oqy00A/edit#gid=281935577&range={i+1}:{i+1}"
        case "CogNet": return f"https://docs.google.com/spreadsheets/d/1rBG7brwbG4pR1j8_eVZapFZUSdaegSVjDH2V6Oqy00A/edit#gid=1725053439&range={i+1}:{i+1}"
        case "Cognates": return f"https://docs.google.com/spreadsheets/d/1rBG7brwbG4pR1j8_eVZapFZUSdaegSVjDH2V6Oqy00A/edit#gid=86109375&range={i+1}:{i+1}"
    return False

import urllib.parse
def nicetranslator(text):
    url = urllib.parse.quote_plus(text)
    return f"https://nicetranslator.com/translation/ru,be,uk,pl,cs,sk,bg,mk,sr,hr,sl/{url}"


from random import choice
def glosbe(text, lang):
    langs_slavic = {'ru', 'uk', 'pl', 'cs', 'bg', 'sr'}
    langs_slavic.discard(lang)
    lang2 = choice(list(langs_slavic))
    text = text.replace(" ", "%20")
    return f'https://glosbe.com/{lang}/{lang2}/{text}'
