import asyncio
import aiohttp

SUPPORTED_WIKIS = [ 'ab', 'ace', 'af', 'als', 'am', 'an', 'ar', 'ary', 'arz', 'as', 'ast', 'avk', 'ay', 'az', 'azb', 'ba', 'ban', 'bar', 'bat-smg', 'bcl', 'be', 'be-tarask', 'be-x-old', 'bg', 'bh', 'bjn', 'bn', 'bo', 'bpy', 'br', 'bs', 'bug', 'ca', 'cdo', 'ce', 'ceb', 'ckb', 'co', 'crh', 'cs', 'csb', 'cu', 'cv', 'cy', 'da', 'de', 'diq', 'dsb', 'el', 'eml', 'en', 'eo', 'es', 'et', 'eu', 'fa', 'fi', 'fiu-vro', 'fo', 'fr', 'frp', 'frr', 'fy', 'ga', 'gan', 'gd', 'gl', 'glk', 'gn', 'gor', 'gu', 'gv', 'ha', 'hak', 'he', 'hi', 'hif', 'hr', 'hsb', 'ht', 'hu', 'hy', 'hyw', 'ia', 'id', 'ie', 'ilo', 'io', 'is', 'it', 'ja', 'jv', 'ka', 'kab', 'kk', 'km', 'kn', 'ko', 'ku', 'kv', 'kw', 'ky', 'la', 'lb', 'li', 'lij', 'lmo', 'lt', 'lv', 'mai', 'map-bms', 'mg', 'mhr', 'mi', 'min', 'mk', 'ml', 'mn', 'mni', 'mr', 'mrj', 'ms', 'my', 'myv', 'mzn', 'nah', 'nap', 'nds', 'nds-nl', 'ne', 'new', 'nl', 'nn', 'no', 'nrm', 'nso', 'nv', 'oc', 'or', 'os', 'pa', 'pam', 'pcd', 'pl', 'pms', 'pnb', 'ps', 'pt', 'qu', 'ro', 'roa-tara', 'ru', 'rue', 'sa', 'sah', 'sat', 'sc', 'scn', 'sco', 'sd', 'se', 'sh', 'shn', 'si', 'simple', 'sk', 'sl', 'sn', 'so', 'sq', 'sr', 'su', 'sv', 'sw', 'szl', 'ta', 'te', 'tg', 'th', 'tk', 'tl', 'tr', 'tt', 'udm', 'ug', 'uk', 'ur', 'uz', 'vec', 'vep', 'vi', 'vls', 'vo', 'wa', 'war', 'wuu', 'xmf', 'yi', 'yo', 'zea', 'zh', 'zh-classical', 'zh-min-nan', 'zh-yue', 'zu']
SLAVIC_LANGS_FULL = ["ru", "be", "be-x-old", "uk", "rue", "pl", "hsb", "dsb", "cs", "sk", "bg", "mk", "sr", "hr", "sh", "sl", "cu"]
SLAVIC_LANGS_LIGHT = ["ru", "be", "uk", "pl", "cs", "sk", "bg", "mk", "sr", "hr", "sl"]

# Разделяет по первой точке, которая не находится внутри скобок.
def take_first_sentence(s):
    stack = []
    for i, c in enumerate(s):
        if c == '(':
            stack.append(c)
        elif c == ')':
            stack.pop()
        elif c in ['.', '!', '?'] and not stack:
            return str(s[:i+1])
    return s.split("\n")[0]

async def fetch_wiki_data(session, lang, title, props):
    url = f"https://{lang}.wikipedia.org/w/api.php?action=query&format=json&prop={props}&titles={title}&lllimit=max"
    async with session.get(url) as response:
        data = await response.json()
    page = next(iter(data.get("query", {}).get("pages", {}).values()), None)
    return page 

async def fetch_langlinks(session, lang, text):
    page = await fetch_wiki_data(session, lang, text, "langlinks|extracts&exintro&explaintext")
    langlinks = page.get("langlinks", []) or None
    if not langlinks:
        return False
    return langlinks

async def wiki_titles(lang, text):
    async with aiohttp.ClientSession() as session:
        langlinks = await fetch_langlinks(session, lang, text)
        if langlinks == False:  # Проверка на строку об ошибке
            return False
        result = []
        for lang in SLAVIC_LANGS_FULL:
            for link in langlinks:
                if link["lang"] == lang:
                    result.append(f"`{link['lang']}` {link['*']}")
                    break
        return "\n".join(result)
    
async def wiki_summary(lang, text):
    async with aiohttp.ClientSession() as session:
        langlinks = await fetch_langlinks(session, lang, text)
        if langlinks == False:  # Проверка на строку об ошибке
            return False
        slavic_langs = []
        for lang in SLAVIC_LANGS_LIGHT:
            for link in langlinks:
                if lang == link["lang"]:
                    slavic_langs.append(lang)
                    break
        tasks = {
            link["lang"]: fetch_wiki_data(session, link["lang"], link["*"], "extracts&exintro&explaintext")
            for link in langlinks if link["lang"] in slavic_langs
        }
        summaries = await asyncio.gather(*tasks.values())
        result = []
        for i, lang in enumerate(slavic_langs):
            if isinstance(summaries[i], dict) and 'extract' in summaries[i]:
                first_sentence = take_first_sentence(summaries[i]['extract'].replace('\n', ' '))
                result.append(f"`{lang}`: {first_sentence}")
        return "\n".join(result)

if __name__ == "__main__":
    lang = "en"
    title = "russia"
    print(asyncio.run(wiki_titles(lang, title)))
    print(asyncio.run(wiki_summary(lang, title)))
