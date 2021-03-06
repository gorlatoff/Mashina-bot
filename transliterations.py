


def kirilica_do_latinici(text):
    text = str.replace(text,'ньј', 'ńj')
    text = str.replace(text,'ь', '') 
    text = str.replace(text,'а', 'a') 
    text = str.replace(text,'ӑ', 'å')
    text = str.replace(text,'б', 'b')
    text = str.replace(text,'в', 'v')
    text = str.replace(text,'ў', 'v') 
    text = str.replace(text,'г', 'g')
    text = str.replace(text,'ґ', 'g')
    text = str.replace(text,'д', 'd')
    text = str.replace(text,'дж','dž')
    text = str.replace(text,'ђ','dž')
    text = str.replace(text,'е', 'e')
    text = str.replace(text,'є', 'ě')
    text = str.replace(text,'ѣ', 'ě')
    text = str.replace(text,'ж', 'ž')
    text = str.replace(text,'з', 'z')
    text = str.replace(text,'и', 'i')
    text = str.replace(text,'ј', 'j')
    text = str.replace(text,'ї', 'ji')
    text = str.replace(text,'й', 'j')
    text = str.replace(text,'к', 'k')
    text = str.replace(text,'л', 'l')
    text = str.replace(text,'љ', 'lj')
    text = str.replace(text,'м', 'm')
    text = str.replace(text,'н', 'n')
    text = str.replace(text,'њ', 'nj')
    text = str.replace(text,'о', 'o')
    text = str.replace(text,'п', 'p')
    text = str.replace(text,'р', 'r')
    text = str.replace(text,'с', 's')
    text = str.replace(text,'т', 't')
    text = str.replace(text,'у', 'u')
    text = str.replace(text,'ф', 'f')
    text = str.replace(text,'х', 'h')
    text = str.replace(text,'ц', 'c')
    text = str.replace(text,'ч', 'č')
    text = str.replace(text,'ш', 'š')  
    text = str.replace(text,'щ', 'šč') 
    text = str.replace(text,'ъ', 'ȯ')
    text = str.replace(text,'ы', 'y')  
    text = str.replace(text,'ю', 'ju')  
    text = str.replace(text,'я', 'ja')
    text = str.replace(text,'ё', 'e')
    text = str.replace(text,'ѫ', 'ų')
    text = str.replace(text,'ѧ', 'ę')   
    text = str.replace(text,'ћ', 'ć')   
    text = str.replace(text,'ѥ', 'je')   
    text = str.replace(text,'ꙑ', 'y')         
    return text



def kirilicna_zamena(text):
    text = str.replace(text,'ру', 'ru')
    text = str.replace(text,'бе', 'be')
    text = str.replace(text,'ук', 'uk')
    text = str.replace(text,'бг', 'bg')
    text = str.replace(text,'мк', 'mk')
    text = str.replace(text,'ср', 'sr')
    text = str.replace(text,'ua', 'uk')
    text = str.replace(text,'cz', 'cs')
    text = str.replace(text,'ms', 'isv')
    text = str.replace(text,'мс', 'isv')
    
    return text

def etymologicna_zamena(text):
    text = str(text)
    text = str.replace(text,'ć', 'č')
    text = str.replace(text,'ś', 's')
    text = str.replace(text,'ź', 'z')
    text = str.replace(text,'ŕ', 'r')
    text = str.replace(text,'ĺ', 'l')
    text = str.replace(text,'ľ', 'l')
    text = str.replace(text,'ń', 'n')
    text = str.replace(text,'ť', 't')
    text = str.replace(text,'ť', 't')
    text = str.replace(text,'ď', 'd')
    text = str.replace(text,'ď', 'd')
    text = str.replace(text,'đ','dž')
    text = str.replace(text,'ȯ', 'o')
    text = str.replace(text,'ė', 'e')
    text = str.replace(text,'č', 'č')
    text = str.replace(text,'š', 'š')
    text = str.replace(text,'ž', 'ž')
    text = str.replace(text,'ě', 'ě')
    text = str.replace(text,'е̌', 'ě')
    text = str.replace(text,'ě', 'e')
    text = str.replace(text,'å', 'a')
    text = str.replace(text,'ę', 'e')
    text = str.replace(text,'ų', 'u')
    return text

def transliteration_ru(text):
    text = str(text)
    text = str.replace(text,'ё', 'е')
    return text

def transliteration_pl(text):
    text = str(text)
    text = str.replace(text,'ę', 'e')
    text = str.replace(text,'ľ', 'ł')
    text = str.replace(text,'ł', 'l')
    text = str.replace(text,'ż', 'ž')
    return text

def transliteration_uk(text):
    text = str(text)
    text = str.replace(text,'ґ', 'г')
    return text

def transliteration_be(text):
    text = str(text)
    text = str.replace(text,'ґ', 'г')
    return text

def ryba(text):
    return text

transliteration = {'isv': etymologicna_zamena,
                   'ru': transliteration_ru, 
                   'pl': transliteration_pl,
                   'uk': transliteration_uk,   
                   'be': transliteration_be,
                   'cs': ryba,
                   'sk': ryba,
                   'bg': ryba,
                   'mk': ryba,
                   'sr': ryba,
                   'hr': ryba,
                   'sl': ryba,
                   'en': ryba, 
                   'de': ryba, 
                   'nl': ryba, 
                   'eo': ryba,
                   'id': ryba                     
                    }
