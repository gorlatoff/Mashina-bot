 

from wikipediaapi import Wikipedia

wiki_wiki = Wikipedia('ru')
page_test = wiki_wiki.page('тувалу')
page_test.summary



from wikipediaapi import Wikipedia
# SLOVJANSKE_VIKI = "ru be be-x-old uk rue pl hsb dsb cs sk bg mk sr hr sh sl cu".split(" ")
# slovjanske_viki = "ru be uk pl cs sk bg mk sr hr sl".split(" ")


def sentence_splitter(s):
    bracket = 0
    for i in range(0, len(s)):
        if s[i] == "(":
            bracket = bracket + 1
        if s[i] == ")":
            bracket = bracket - 1
        if (s[i] == ".") and (bracket == 0):
            return str(s[0:(i+1)])
    return s.split("\n")[0]
        
        
def wiki_titles(lang, text):
    SLOVJANSKE_VIKI = "ru be be-x-old uk rue pl hsb dsb cs sk bg mk sr hr sh sl cu".split(" ")
    lang = str.replace(lang,'be-tarask', 'be-x-old')
    wiki_wiki = Wikipedia(lang)
    page_test = wiki_wiki.page(text)
    if page_test.summary == '':
        return False
    result ="Rezultaty iz Wikipedije:\n"
    result = result + f"`{lang}` {page_test.title}" + "\n"
    if page_test.langlinks == {}:
        result = result + str( sentence_splitter(page_test.summary) ) + "\n"
        return result
    if lang in SLOVJANSKE_VIKI:
        SLOVJANSKE_VIKI.remove(lang)  
    for k in SLOVJANSKE_VIKI:
        try:
            result = result + f"`{k}` {page_test.langlinks[k].title}" + "\n"
        except KeyError:
            pass
    return result




def wiki_text(lang, text):
    slovjanske_viki = "ru be uk pl cs sk bg mk sr hr sl".split(" ")
    wiki_wiki = Wikipedia(lang)
    page_test = wiki_wiki.page(text)
    if page_test.summary == '':
        return False
    result ="Rezultaty iz Wikipedije:\n"
    result = result + f"`{lang}` {page_test.title}: "
    result = result + str( sentence_splitter(page_test.summary) ) + "\n"
    if lang in slovjanske_viki:
        slovjanske_viki.remove(lang) 
    for k in slovjanske_viki:
        try:
            result = result + f"`{k}` {page_test.langlinks[k].title}: "
            result = result + str( sentence_splitter(page_test.langlinks[k].summary) ) + "\n"
        except KeyError:
            pass
    return result


wikis = [
 'ab',
 'ace',
 'af',
 'als',
 'am',
 'an',
 'ar',
 'ary',
 'arz',
 'as',
 'ast',
 'avk',
 'ay',
 'az',
 'azb',
 'ba',
 'ban',
 'bar',
 'bat-smg',
 'bcl',
 'be',
 'be-tarask',
 'be-x-old',
 'bg',
 'bh',
 'bjn',
 'bn',
 'bo',
 'bpy',
 'br',
 'bs',
 'bug',
 'ca',
 'cdo',
 'ce',
 'ceb',
 'ckb',
 'co',
 'crh',
 'cs',
 'csb',
 'cu',
 'cu\t',
 'cv',
 'cy',
 'da',
 'de',
 'diq',
 'dsb',
 'el',
 'eml',
 'en',
 'eo',
 'es',
 'et',
 'eu',
 'fa',
 'fi',
 'fiu-vro',
 'fo',
 'fr',
 'frp',
 'frr',
 'fy',
 'ga',
 'gan',
 'gd',
 'gl',
 'glk',
 'gn',
 'gor',
 'gu',
 'gv',
 'ha',
 'hak',
 'he',
 'hi',
 'hif',
 'hr',
 'hsb',
 'ht',
 'hu',
 'hy',
 'hyw',
 'ia',
 'id',
 'ie',
 'ilo',
 'io',
 'is',
 'it',
 'ja',
 'jv',
 'ka',
 'kab',
 'kk',
 'km',
 'kn',
 'ko',
 'ku',
 'kv',
 'kw',
 'ky',
 'la',
 'lb',
 'li',
 'lij',
 'lmo',
 'lt',
 'lv',
 'mai',
 'map-bms',
 'mg',
 'mhr',
 'mi',
 'min',
 'mk',
 'ml',
 'mn',
 'mni',
 'mr',
 'mrj',
 'ms',
 'my',
 'myv',
 'mzn',
 'nah',
 'nap',
 'nds',
 'nds-nl',
 'ne',
 'new',
 'nl',
 'nn',
 'no',
 'nrm',
 'nso',
 'nv',
 'oc',
 'or',
 'os',
 'pa',
 'pam',
 'pcd',
 'pl',
 'pms',
 'pnb',
 'ps',
 'pt',
 'qu',
 'ro',
 'roa-tara',
 'ru',
 'rue',
 'sa',
 'sah',
 'sat',
 'sc',
 'scn',
 'sco',
 'sd',
 'se',
 'sh',
 'shn',
 'si',
 'simple',
 'sk',
 'sl',
 'sn',
 'so',
 'sq',
 'sr',
 'su',
 'sv',
 'sw',
 'szl',
 'ta',
 'te',
 'tg',
 'th',
 'tk',
 'tl',
 'tr',
 'tt',
 'udm',
 'ug',
 'uk',
 'ur',
 'uz',
 'vec',
 'vep',
 'vi',
 'vls',
 'vo',
 'wa',
 'war',
 'wuu',
 'xmf',
 'yi',
 'yo',
 'zea',
 'zh',
 'zh-classical',
 'zh-min-nan',
 'zh-yue',
 'zu']