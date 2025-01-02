alphabets = {

    'isv': 'a b c č d d́ e ě е̌ ė ę ě f g h i j k l m n o p r s š t t́ u v y z ž å è ò ó ú ý ć č ď đ ĺ ľ ń ŕ ś š ť ų ź ž ȯ а б в г д е ж з и к л м н о п р с т у ф х ц ч ш ы ђ є ј љ њ ћ ь ъ ӑ ѧ ѫ'.split(' '),
    'isv_cyr': 'а б в г д е ж з и к л м н о п р с т у ф х ц ч ш ы ђ є ј љ њ ћ ь ъ ӑ ѧ ѫ'.split(' '),

    'en': 'a b c d e f g h i j k l m n o p q r s t u v w x y z'.split(' '),
    'de': 'a b c d e f g h i j k l m n o p q r s t u v w x y z ä ö ü ß'.split(' '),
    'nl': 'a b c d e f g h i j k l m n o p q r s t u v w x y z ä ë é è ï í ó ö ú ü'.split(' '),
    'eo': 'a b c ĉ d e f g ĝ h ĥ i j ĵ k l m n o p r s ŝ t u ŭ v z'.split(' '),

    'ru': 'а б в г д е ё ж з и й к л м н о п р с т у ф х ц ч ш щ ъ ы ь э ю я'.split(' '),
    'uk': 'а б в г ґ д е є ж з и і ї й к л м н о п р с т у ф х ц ч ш щ ь ю я'.split(' '),
    'be': 'а б в г д е ё ж з і й к л м н о п р с т у ў ф х ц ч ш ы ь э ю я'.split(' '),
    'sr': 'а б в г д ђ е ж з и ј к л љ м н њ о п р с т ћ у ф х ц ч џ ш'.split(' '),
    'sr_lat': 'a b c č ć d đ e f g h i j k l m n o p r s š t u v z ž'.split(' '),
    'bg': 'а б в г д е ж з и й к л м н о п р с т у ф х ц ч ш щ ъ ь ю я'.split(' '),
    'mk': 'а б в г д ѓ е ж з ѕ и ј к л љ м н њ о п р с т ќ у ф х ц ч џ ш'.split(' '),
    'rue': 'а б в г д є е ё ж з и і ї й к л м н о п р с т у ф х ц ч ш щ ь ы э ю я'.split(' '),

    'pl': 'a ą b c ć d e ę f g h i j k l ł m n ń o ó p r s ś t u w y z ź ż'.split(' '),
    'cs': 'a b c č d ď e ě f g h i í j k l m n ň o ó p q r ř s š t ť u ú ů v w x y ý z ž'.split(' '),
    'sk': 'a á ä b c č d ď dz dž e é f g h i í j k l ĺ ľ m n ň o ó ô p q r ŕ s š t ť u ú v w x y ý z ž'.split(' '),
    'hr': 'a b c č ć d đ e f g h i j k l m n o p r s š t u v z ž'.split(' '),
    'sl': 'a b c č ć d đ e f g h i j k l m n o p r s š t u v z ž'.split(' '),
    'csb': 'a ą ã b c ć d e ë é f g h i j k l ł m n ń o ó ô p r s ś t u w y z ź ż'.split(' '),
    'dsb': 'a b c č ć d dž e ě f g h i j k l ł m n ń o ó p r s š t u w y z ž'.split(' '),
    'hsb': 'a b c č ć d dž e ě f g h i j k l ł m n ń o ó p r s š t u w y z ž'.split(' '),
}

import regex


def language_verify(text, lang):
    if lang not in alphabets:
        return False
    text = regex.sub(r'[^\p{L}]+', '', text)
    intersection = set(alphabets[lang]) & set(text)
    if not text:
        return True 
    if len(intersection) < len(set(text)):
        return False
    return True
    # Проверяем, что все символы текста входят в алфавит языка
    # return all(char.lower() in alphabets[lang] for char in text)


language_verify("dear alice", "en")


def checkalphabet(text):
    cyrillic_chars = set('абвгдежзийклмнопрстуфхцчшщъыьэюяёђѓєіїјљњћќўџґѣ')
    latin_chars = set('abcdefghijklmnopqrstuvwxyzěščžåęųėȯŕĺńt́d́śźćđ')
    text_chars = set(text)

    print(cyrillic_chars & text_chars)
    print(latin_chars & text_chars)
    if len(cyrillic_chars & text_chars) > len(latin_chars & text_chars):
        return 'cyrillic'
    return 'latin'
