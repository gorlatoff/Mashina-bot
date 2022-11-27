import pandas as pd
import os, re

brackets_regex1 = re.compile(" \(.*\)")
brackets_regex2 = re.compile(" \[.*\]")

slovnik_link = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRsEDDBEt3VXESqAgoQLUYHvsA5yMyujzGViXiamY7-yYrcORhrkEl5g6JZPorvJrgMk6sjUlFNT4Km/pub?output=xlsx'

def load_slovnik(tabela=slovnik_link, obnoviti=False):
    if obnoviti == False and os.path.isfile("slovnik_words.pkl") and os.path.isfile("slovnik_suggestions.pkl"):
        print("Found 'slovnik_slovnik.pkl' file, using it")
        print("Found 'slovnik_suggestions.pkl' file, using it")
        dfs = { "words": pd.read_pickle("slovnik_words.pkl"), 
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
            cell = transliteration['isv'](cell)
        if slovo in str.split( cell, ', ' ):
            najdene_slova.append(i)
    return najdene_slova

LANGS = "isv en ru uk be pl cs sk bg mk sr hr sl de nl eo".split(' ')

trans_tables = { 'isv': 'ć-č ś-s ź-z ŕ-r ĺ-l ľ-l ń-n ť-t ť-t ď-d ď-d đ-dž ȯ-o ė-e č-č š-š ž-ž ě-ě е̌-ě ě-e å-a ę-e ų-u',
                 'ru': 'ё-е а́-а е́-е и́-и о́-о у́-у ы́-ы э́-э ю́-ю я́-я',
                 'uk': 'ґ-г а́-а е́-е и́-и о́-о у́-у ы́-ы є́-є ю́-ю я́-я і́-і ї́-ї',  
                 'be': 'ґ-г а́-а е́-е и́-и о́-о у́-у ы́-ы э́-э ю́-ю я́-я і́-і',  
                 'bg': 'ѝ-и',
                 'mk': 'ѝ-и ѐ-е'
          #'sr': сербохорватский и словенский: четыре знака ударения (/, \, ^, \\), 
}

def transliteration_replacer(text, lang):
    for i in trans_tables[lang].split(' '):
        letters = i.split('-')
        text = text.replace(letters[0], letters[1])
    return text


from collections import defaultdict
transliteration = defaultdict( lambda: lambda x: x)
   
transliteration['isv'] = lambda x: transliteration_replacer(x, 'isv')
transliteration['ru'] = lambda x: transliteration_replacer(x, 'ru')
transliteration['be'] = lambda x: transliteration_replacer(x, 'be')
transliteration['uk'] = lambda x: transliteration_replacer(x, 'uk')
transliteration['bg'] = lambda x: transliteration_replacer(x, 'bg')
transliteration['mk'] = lambda x: transliteration_replacer(x, 'mk')


# Oddaljaje space'y ako li one sut v početku teksta
def despace(s):
    if s and s[0] == ' ':
        return s.replace(' ', '')
    return s

def cell_normalization(cell, jezyk):
    cell = str(cell)
    cell = str.replace( cell, '!', '')
    cell = str.replace( cell, '#', '')
    cell = cell.lower()
    cell = transliteration[jezyk](cell)
    return cell

def symbols_normalization(cell):
    cell = str(cell)
    cell = str.replace( cell, '+', '' )     
    cell = str.replace( cell, '^', '' ) 
    cell = str.replace( cell, '$', '' )  
    cell = str.replace( cell, '?', '' )  
    cell = str.replace( cell, '@', '' )    
    cell = str.replace( cell, '-', '' )
    cell = str.replace( cell, '!', '' )    
    cell = str.replace( cell, '#', '' )
    cell = str.replace( cell, '/', '' )
    cell = str.replace( cell, '\\', '' )                
    return cell

# from transliterations import etymologicna_zamena

def prepare_slovnik(slovnik, split=False, transliterate = True):
    sheet = slovnik.copy()
    langs = list((set(slovnik.columns) & set(LANGS) ))
    for lang in langs:
        assert sheet[sheet[lang].astype(str).apply(lambda x: "((" in sorted(x))].empty
    for lang in langs:
        slovnik[lang] = slovnik[lang].apply(lambda x: str(x) ) # в переводчике была проблема, пока эту строчку не добавил
        sheet[lang] = sheet[lang].str.replace(brackets_regex1, "")
        sheet[lang] = sheet[lang].str.replace(brackets_regex2, "")
        sheet[lang] = sheet[lang].apply(lambda x: cell_normalization(x, lang))
        sheet[lang] = sheet[lang].apply(lambda x: despace(x))   
        if transliterate == True:
            sheet[lang] = sheet[lang].apply(transliteration[lang])               
        if split == True:
            sheet[lang + "_set"] = sheet[lang].str.split(", ").apply(lambda x: x)
    sheet['isv'] = sheet['isv'].str.replace("!", "").str.replace("#", "").str.lower()
    return sheet


def filtr_contain(stroka, jezyk, sheet):
    return sheet[ sheet[jezyk].str.contains(stroka) == True].copy()


def iskati(slovo, jezyk, sheet):
    najdene_slova = []
    if '(' in slovo:
        for i, stroka in sheet.iterrows():    
            if slovo in str.split( stroka[jezyk], ', ' ):
                najdene_slova.append(i)
    else:
        for i, stroka in sheet.iterrows():    
            if slovo in str.split( stroka[jezyk], ', ' ):
                najdene_slova.append(i)
    return najdene_slova


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
    return words_gluer(wordslist)

def is_in_dict(stroka, jezyk, sheet):
    sheet1 = filtr_contain(stroka, jezyk, sheet)
    sheet2 = iskati(stroka, jezyk, sheet1)
    if sheet2.empty:
        return False
    return True

def words_gluer(arr):
    glued = ''
    if not arr:
        return False
    for word in arr[:-1]:
        glued = glued + word + ", "
    return glued + arr[-1]



# slovnik_loaded = load_slovnik()   
# words = prepare_slovnik(slovnik_loaded['words']) 
# suggestions = prepare_slovnik(slovnik_loaded['suggestions']) 

# najdene_slova_suggestions = iskati("S00002", 'id', suggestions)