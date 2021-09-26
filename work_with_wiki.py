
from wikipediaapi import Wikipedia
SLOVJANSKE_VIKI = "ru pl uk sr cs sh bg sk hr be sl mk be-x-old hsb rue dsb cu".split(" ")
slovjanske_viki = "ru pl uk sr cs bg sk hr be sl mk".split(" ")

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
    wiki_wiki = Wikipedia(lang)
    page_test = wiki_wiki.page(text)
    if page_test.summary == '':
        return False
    result ="Rezultaty iz Wikipedije:\n"

    for k in SLOVJANSKE_VIKI:
        try:
            result = result + f"`{k}` {page_test.langlinks[k].title}" + "\n"
        except KeyError:
            if k == lang:
                result = result + f"`{k}` {page_test.title}" + "\n"
    return result




def wiki_text(lang, text):
    wiki_wiki = Wikipedia(lang)
    page_test = wiki_wiki.page(text)
    if page_test.summary == '':
        return False
    result ="Rezultaty iz Wikipedije:\n"

    for k in slovjanske_viki:
        if k == lang:
            result = result + f"`{k}` {page_test.title}: "
            result = result + str( sentence_splitter(page_test.summary) ) + "\n"
            pass
        try:
            result = result + f"`{k}` {page_test.langlinks[k].title}: "
            result = result + str( sentence_splitter(page_test.langlinks[k].summary) ) + "\n"
        except KeyError:
            pass
    return result
