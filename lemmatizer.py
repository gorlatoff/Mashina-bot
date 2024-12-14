from lemmagen3 import Lemmatizer

lemmatizer_langs = ['ru', 'uk', 'pl', 'cs', 'sk', 'bg', 'mk', 'sr', 'hr', 'sl']

nlp_list = { lang: Lemmatizer(lang)  for lang in lemmatizer_langs}
nlp_list["be"] = Lemmatizer("ru")
nlp_list["hr"] = Lemmatizer("sr")

def slavic_lemmatizer(word, lang):
    if lang not in nlp_list:
        return word 
    return nlp_list[lang].lemmatize(word)
