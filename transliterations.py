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

def ryba(text):
    return text

transliteration = {'isv': etymologicna_zamena,
                   'ru': transliteration_ru, 
                   'pl': transliteration_pl,
                   'uk': transliteration_uk,   
                   'be': ryba,
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
