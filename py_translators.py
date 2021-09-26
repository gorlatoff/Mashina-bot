from translators import google, bing

def translator_light(language, text ):
    ru = google(text, language, 'ru')
    uk = bing(text, language, 'uk')
    pl = google(text, language, 'pl')
    cs = google(text, language, 'cs')
    bg = google(text, language, 'bg')
    sr = google(text, language, 'sr')

    result = f"""
Rezultaty avtomatičnogo prěvoda:
`ru` {ru}
`uk` {uk}
`pl` {pl}
`cs` {cs}
`bg` {bg}
`sr` {sr}"""
    return result
