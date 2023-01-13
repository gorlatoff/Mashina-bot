import pandas as pd
import os
import re

brackets_regex1 = re.compile( " \(.*\)" )
brackets_regex2 = re.compile( " \[.*\]" )

slovnik_link = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRsEDDBEt3VXESqAgoQLUYHvsA5yMyujzGViXiamY7-yYrcORhrkEl5g6JZPorvJrgMk6sjUlFNT4Km/pub?output=xlsx'


def load_slovnik(tabela=slovnik_link, obnoviti=False):
    if obnoviti == False and os.path.isfile("slovnik_words.pkl") and os.path.isfile("slovnik_suggestions.pkl"):
        print("Found 'slovnik_words.pkl' file, using it")
        print("Found 'slovnik_suggestions.pkl' file, using it")
        dfs = {"words": pd.read_pickle("slovnik_words.pkl"),
               "suggestions": pd.read_pickle("slovnik_suggestions.pkl")}
        return dfs

    print('Dostava slovnika...')
    dfs = pd.read_excel(io=tabela, engine='openpyxl', sheet_name=['words', 'suggestions'])
        
    dfs['suggestions'].columns = dfs['suggestions'].iloc[0]
    dfs['suggestions'].reindex(dfs['suggestions'].index.drop(0))
    dfs['suggestions'].rename(columns={'ids': 'id'}, inplace=True)
        
    for i in ['words', 'suggestions']:
        for col in dfs[i].columns:
            dfs[i][col] = dfs[i][col].fillna(' ').astype(str)
        
    dfs['words'].to_pickle("slovnik_words.pkl")
    dfs['suggestions'].to_pickle("slovnik_suggestions.pkl")

    return dfs


def load_sheet(tabela_name, sheet_names: list, tabela, obnoviti):
    ispath = [os.path.isfile(f"{tabela_name}_{name}.pkl") for name in sheet_names]
    if obnoviti == False and (False not in ispath):
        dfs = {}
        for name in sheet_names:
            sheetname = f'{tabela_name}_{name}.pkl'
            dfs.update({name: pd.read_pickle(f'{sheetname}')})
        return dfs
    print(f'Dostava tabely {tabela_name}...')
    dfs = pd.read_excel(io=tabela, engine='openpyxl', sheet_name=sheet_names)
    print('Gotovo.')    
    for name in sheet_names:
        for col in dfs[name].columns:
            dfs[name][col] = dfs[name][col].fillna(' ').astype(str)
        dfs[name].to_pickle(f"{tabela_name}_{name}.pkl")
    return dfs

def load_discord_fraznik():
    discord_list = pd.read_excel(io='https://docs.google.com/spreadsheets/d/e/2PACX-1vTIevV03tPoLIILAx4DqHH6QetiiYb13xMiQ7HMvvleWLjveoJ6uayNIDLd0cKUMj9TtNsl2XDsZR8w/pub?output=xlsx',
                    engine='openpyxl',
                    sheet_name=['tabela', 'nove slova'])
    for i in ['tabela', 'nove slova']:
        for name in discord_list[i].columns:
            discord_list[i][name] = discord_list[i][name].fillna(" ").astype(str)    
    return discord_list

def iskati_discord(jezyk, slovo, sheet):
    najdene_slova = []
    for i in range(0, len(sheet.index)):      
        cell = str( sheet[jezyk][i] )
        cell = cell.lower()
        cell = re.sub(r'\[.*?\]', '', cell)
        if jezyk == 'Vse varianty v MS':
            cell = transliteracija(cell, 'isv')
        if slovo in str.split( cell, ', ' ):
            najdene_slova.append(i)
    return najdene_slova

LANGS = "isv en ru uk be pl cs sk bg mk sr hr sl de nl eo".split(' ')

trans_tables = { 'isv': 'ć-č ś-s ź-z ŕ-r ĺ-l ľ-l ń-n ť-t ť-t ď-d ď-d đ-dž ȯ-o ė-e č-č š-š ž-ž ě-ě е̌-ě ě-e å-a ę-e ų-u',
                 'ru': 'ё-е а́-а е́-е и́-и о́-о у́-у ы́-ы э́-э ю́-ю я́-я',
                 'uk': 'ґ-г а́-а е́-е и́-и о́-о у́-у ы́-ы є́-є ю́-ю я́-я і́-і ї́-ї',  
                 'be': 'ґ-г а́-а е́-е и́-и о́-о у́-у ы́-ы э́-э ю́-ю я́-я і́-і',  
                 'bg': 'ѝ-и',
                 'mk': 'ѝ-и ѐ-е',
                 'kir_to_lat': 'ньј-ńj ь- а-a ӑ-å б-b в-v ў-v г-g ґ-g д-d дж-dž ђ-dž е-e є-ě ѣ-ě ж-ž з-z и-i ј-j ї-ji й-j к-k л-l љ-lj м-m н-n њ-nj о-o п-p р-r с-s т-t у-u ф-f х-h ц-c ч-č ш-š щ-šč ъ-ȯ ы-y ю-ju я-ja ё-e ѫ-ų ѧ-ę ћ-ć ѥ-je ꙑ-y',     
                 'kirilicna_zamena': 'ру-ru бе-be ук-uk бг-bg мк-mk ср-sr ua-uk cz-cs ms-isv мс-isv',
}

def transliteracija(text, lang):
    if lang not in trans_tables.keys():
        return text
    for i in trans_tables[lang].split(' '):
        letters = i.split('-')
        text = text.replace(letters[0], letters[1])
    return text
    
    
def cell_normalization(cell, jezyk):
    cell = str(cell)
    cell = cell.replace( '!', '')
    cell = cell.replace( '#', '')
    cell = cell.replace( ';', ',')
    cell = cell.lower()
    cell = cell.strip()
    cell = transliteracija(cell, jezyk)
    return cell

def prepare_slovnik(slovnik, split=False, transliterate=True):
    sheet = slovnik.copy()
    langs = list((set(slovnik.columns) & set(LANGS) ))
    for lang in langs:
        assert sheet[sheet[lang].astype(str).apply(lambda x: "((" in sorted(x))].empty
    for lang in langs:
        slovnik[lang] = slovnik[lang].apply(lambda x: str(x) ) # в переводчике была проблема, пока эту строчку не добавил
        sheet[lang] = sheet[lang].str.replace(brackets_regex1, "")
        sheet[lang] = sheet[lang].str.replace(brackets_regex2, "")
        sheet[lang] = sheet[lang].apply(lambda x: cell_normalization(x, lang))
        if transliterate:
            sheet[lang] = sheet[lang].apply(lambda x: transliteracija(x, lang))        
        if split:
            sheet[lang] = sheet[lang].str.split(", ").apply(lambda x: x)
    sheet['isv'] = sheet['isv'].str.replace("!", "").str.replace("#", "").str.lower()
    return sheet


def filtr_contain(stroka, jezyk, sheet):
    stroka = re.escape(stroka)
    return sheet[ sheet[jezyk].str.contains(stroka) == True].copy()

def iskati(stroka, jezyk, sheet):
    result = sheet[ sheet[jezyk].apply( lambda text: stroka in text.split(', '))]
    return result.index.values.tolist()

def iskati_slovo(slovo, jezyk, sheet):
    najdene_slova = []
    for i, stroka in sheet.iterrows():    
        if slovo in str.split( re.sub(r'[^\w\s]','', stroka[jezyk]) ):
            najdene_slova.append(i)
    return najdene_slova

    
def in_dict(stroka, jezyk, sheet):
    sheet = filtr_contain(stroka, jezyk, sheet)
    sheet = iskati(stroka, jezyk, sheet)
    if sheet.empty:
        return False
    wordslist = sheet['isv'].tolist()
    return ", ".join(wordslist)

def is_in_dict(stroka, jezyk, sheet):
    sheet1 = filtr_contain(stroka, jezyk, sheet)
    sheet2 = iskati(stroka, jezyk, sheet1)
    if sheet2.empty:
        return False
    return True


def search_in_sheet(slova, jezycny_kod, sheet):
    sheet = filtr_contain( slova, jezycny_kod, sheet )  
    najdene_slova = iskati(slova, jezycny_kod, sheet)
    if najdene_slova:
        return najdene_slova           
    najdene_slova = iskati_slovo(slova, jezycny_kod, sheet)
    if najdene_slova:
        return najdene_slova
    return False

# def load_data(update):
#     global slovnik_loaded, words, suggestions, discord_fraznik, korpus_loaded, words_general 
       
#     slovnik_loaded = load_slovnik(obnoviti=update)   
#     words = prepare_slovnik(slovnik_loaded['words']) 
#     suggestions = prepare_slovnik(slovnik_loaded['suggestions']) 
#     discord_fraznik = load_discord_fraznik()
#     korpus_link = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRz8l3w4h--36bUS-5plpkkVLnSFmCPIB3WnpDYRer87eirVVMYfI-ZDbp3WczyL2G5bOSXKty2MpOY/pub?output=xlsx'    
#     korpus_loaded = load_sheet(tabela_name="korpus", sheet_names=['words (general)'], tabela=korpus_link, obnoviti= update )
#     words_general = prepare_slovnik(korpus_loaded['words (general)'])
#     return {    
#             "slovnik_loaded": slovnik_loaded,
#             "words": words,
#             "suggestions": suggestions,
#             "discord_fraznik": discord_fraznik,
#             "korpus_loaded": korpus_loaded,
#             "words_general": words_general
#     }


# slovnik_loaded = load_slovnik()   
# words = prepare_slovnik(slovnik_loaded['words'], split=False) 
# suggestions = prepare_slovnik(slovnik_loaded['suggestions']) 

# najdene_slova_suggestions = iskati("S00002", 'id', suggestions)

# contain = filtr_contain("снежный", "ru", words )

# from timeit import timeit

# timeit(lambda: iskati_slovo("снежный", "ru", contain ), number=1000 )