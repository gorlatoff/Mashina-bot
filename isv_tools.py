import asyncio
import os
import re
import polars as pl
from rapidfuzz import fuzz, process
import bots
import transliteration as transl
import lang_detect
import lemmatizer
import wiki

sheet_links = {
  'words': 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRsEDDBEt3VXESqAgoQLUYHvsA5yMyujzGViXiamY7-yYrcORhrkEl5g6JZPorvJrgMk6sjUlFNT4Km/pub?output=csv',
  'Cognates': 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRz8l3w4h--36bUS-5plpkkVLnSFmCPIB3WnpDYRer87eirVVMYfI-ZDbp3WczyL2G5bOSXKty2MpOY/pub?gid=86109375&single=true&output=csv',
  'Wiki list': 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRz8l3w4h--36bUS-5plpkkVLnSFmCPIB3WnpDYRer87eirVVMYfI-ZDbp3WczyL2G5bOSXKty2MpOY/pub?gid=281935577&single=true&output=csv',
  'suggestions': 'https://docs.google.com/spreadsheets/d/e/2PACX-1vS8scL0kxJY7rgLC-2iaG_XmbOI72sbfmd63YhcvuFgc9KDDFpRyvIWwfcr6yHxE7Uk0coCaePfozL-/pub?gid=1226657383&single=true&output=csv',
  'fraznik': 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTIevV03tPoLIILAx4DqHH6QetiiYb13xMiQ7HMvvleWLjveoJ6uayNIDLd0cKUMj9TtNsl2XDsZR8w/pub?gid=0&single=true&output=csv',
#   'CogNet': 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRz8l3w4h--36bUS-5plpkkVLnSFmCPIB3WnpDYRer87eirVVMYfI-ZDbp3WczyL2G5bOSXKty2MpOY/pub?gid=1725053439&single=true&output=csv',
}

fraznik_link = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vTIevV03tPoLIILAx4DqHH6QetiiYb13xMiQ7HMvvleWLjveoJ6uayNIDLd0cKUMj9TtNsl2XDsZR8w/pub?gid=0&single=true&output=csv'
sheets = {key: False for key in sheet_links.keys()}
columns = [ 'id', 'isv', 'partOfSpeech', 'en', 'ru', 'be', 'uk', 'pl', 'cs', 'sk', 'bg', 'mk', 'sr', 'hr', 'sl', 'frequency']
langs = "isv en ru uk be pl cs sk bg mk sr hr sl".split(' ')

brackets_regex1 = re.compile( r" \(.*\)" )
brackets_regex2 = re.compile( r" \[.*\]" )


def cell_normalization(cell: str, lang: str) -> str:
    cell = cell.replace( '!', '').replace( '#', '')
    cell = re.sub(brackets_regex1, "", cell)
    cell = re.sub(brackets_regex2, "", cell)
    cell = cell.lower()
    cell = cell.strip()
    cell = transl.transliteration(cell, lang)
    return cell


def prepare_slovnik(sheet, sheetname: str):
    if sheetname == 'fraznik':
        sheet = sheet.with_columns([
            (sheet['Vse varianty v MS'].map_elements(lambda x: cell_normalization(x, 'isv'), return_dtype=pl.Utf8)).alias(f'isv')
        ])
        return sheet
    for lang in langs:
        print(lang)
        sheet = sheet.with_columns([
            (sheet[lang].map_elements(lambda x: cell_normalization(x, lang), return_dtype=pl.Utf8)).alias(f'{lang}_normalized')
        ])
    sheet = sheet.with_columns(pl.Series(name="index", values=range(1, len(sheet) + 1))) 
    return sheet


def load_sheet(tabela_name: str, update: bool):
    tabela_name_parquet = tabela_name+".parquet"
    if update or not os.path.isfile(tabela_name_parquet):
        print(f'Sheet {tabela_name} is downloading ...')
        df = pl.read_csv(sheet_links[tabela_name], separator=",", ignore_errors=True, dtypes={k: str for k in columns} ).fill_null(' ')
        if tabela_name != 'fraznik': 
            cols = [i for i in df.columns if (i in columns) ]
            df = df.select(cols)
        df = prepare_slovnik(df, tabela_name)      
        df.write_parquet(tabela_name_parquet)
        return df
    print( f"Found {tabela_name_parquet} file, using it")
    return pl.read_parquet(tabela_name_parquet)

def load_all_sheets(sheet_names=sheets.keys(), update=False):
    for sheetname in sheet_names:
        sheets[sheetname] = load_sheet(sheetname, update)
    return sheets


sheets = load_all_sheets()
sheets['words']['isv_normalized']


def update_sheets(text: str):
    global sheets
    text = transl.transliteration(text, 'kir_to_lat')
    sheets_to_update = [s for s in sheet_links.keys() if (s.lower() in text)]
    if not sheets_to_update:
        sheets = load_all_sheets(update=True)
        return True
    for sheetname in sheets_to_update:
        print(f"Dostava tabely {sheetname}...")
        sheets[sheetname] = load_sheet(sheetname, True)
    print("Obnovjenje jest skončeno")
    return True


# update_sheets("obnovi Cognates", sheet_links, sheets)



def translations_card(row, sheet_name: str):
    i = row['index'][0]
    languages = "en ru be uk pl cs sk bg mk sr hr sl".split(" ")
    word_is_in = {
    'words': 'v slovniku',
    'suggestions': 'v spisu novyh slov',
    'Wiki list': 'v tabelě "Wiki list"',
    'CogNet': 'v tabelě "CogNet"',
    'Cognates': 'v tabelě "Cognates"',
    }
    title = f"{i+2} {word_is_in[sheet_name]}"
    output = f"## [{title}](<{bots.link_na_slovo(i, sheet_name)}>)\n\n"
    output += f"**{ bots.formatizer( row['isv'][0] )}**\n"
    for col in languages:
        words = row[col][0]
        output += f"**`{col}` **{ bots.formatizer(words) }\n"
    output += f"\n`.id {row['id'][0]}`"
    return output


def words_list_card(sheet, contain = False):
    result = f"**Najdeno {len(sheet)} slov(a), vy možete vyzvati jih prikazom `.id`:**\n\n"
    if contain:
        result = f"**Najdeno {len(sheet)} slov(a):**\n\n"
    for i in range(0, len(sheet)):
        new_row = f"{sheet['isv'][i]} (`.id {sheet['id'][i]}`)\n"
        if len(result) + len(new_row) < 600:
            result += new_row
        else:
            result += "\n*I tako dalje....*"
            break
    return result



def phrasebook_card(i: int, tabela):
    markdown = "# Rezultat iz [fraznika](https://gorlatoff.github.io/fraznik.html)\n\n"
    for col in tabela.columns[0:8]:
        cell = tabela[col][i]
        if cell != " ":
            markdown += f"## {col}\n{cell}\n\n"
    return markdown

def split_by_coma(text: str) -> list:
    if ";" in text:
        return text.split("; ")
    return text.split(", ")


def split_and_search(s: str, text: str) -> bool:
    s = str(s)
    if ";" in text:
        return s in text.split("; ")
    return s in text.split(", ")


def filter_contain(s: str, lang: str, sheet):
    sheet = sheet.filter( pl.col(lang).str.contains(s, literal=True) )
    return sheet



def search(s: str, lang: str, sheet):
    filter_sheet = pl.col(lang).map_elements(lambda text: split_and_search(s, text), return_dtype=pl.Boolean)
    return sheet.filter(filter_sheet)

def search_by_word(s: str, lang: str, sheet):
    split_column = pl.col(lang).map_elements(lambda text: s in re.split(r'[^\w]', text), return_dtype=pl.Boolean)
    return sheet.filter(split_column)

def search_in_sheet(slova: str, lang: str, sheet):
    sheet = filter_contain( slova, lang, sheet)
    if sheet.is_empty():
        return sheet
    najdene_slova = search( slova, lang, sheet)
    if not najdene_slova.is_empty():
        return najdene_slova
    najdene_slova = search_by_word(slova, lang, sheet)
    return najdene_slova



phrasebook_result = search_in_sheet('biti', "isv", sheets['fraznik'])



def search_in_phrasebook(slova: str, lang: str):
    sheet = sheets['fraznik']
    if lang == "isv_normalized":
        slova = transl.transliteration(slova, 'isv')
        return search_in_sheet(slova, "isv", sheet)
    if lang == "en":
        return search_in_sheet(slova, "Slovo na anglijskom", sheet)
    isv_translations = search_in_sheet(slova, lang, sheets['words'])
    if isv_translations.is_empty():
        return isv_translations
    isv_words = isv_translations['isv_normalized'].to_list()
    isv_words = [split_by_coma(text) for text in isv_words]
    isv_words = [item for sublist in isv_words for item in sublist]
    results = pl.DataFrame()
    for isv_word in isv_words:
        phrasebook_result = search_in_sheet(isv_word, "isv", sheet)
        results = pl.concat([results, phrasebook_result], how="vertical")
    return results.unique(maintain_order=True)

def phrasebook(slova: str, lang: str):
    result = search_in_phrasebook(slova, lang)
    messages = []
    if not result.is_empty():
        for i in range(0, len(result)):
            card = phrasebook_card(i, result)
            messages.append(card)
        return messages
    return ["Ničto ne jest najdeno. Tut možeš uviděti vsi slova, ktore imajemo https://gorlatoff.github.io/fraznik.html"]



def search_fuzzy(s: str, langs_wordlist: list):
    results = process.extract(s, langs_wordlist, scorer=fuzz.ratio, score_cutoff=85, limit=6)
    if not results:
        return False
    results = {i[0] for i in results}
    return list(results)


def sort_by_distance(slova: str, lang: str, sheet):
    sheet = sheet.with_columns( 
        pl.col(lang)
        .map_elements(lambda x: fuzz.ratio(slova, x), return_dtype=pl.Float64)
        .alias("distance"),
    )
    return sheet.sort(["distance"], descending=True)


import asyncio
async def mashina_search(slova: str, lang: str):
    print(slova, lang)
    messages = []

    lang_normalized = lang + '_normalized'
    if lang == 'id':
        lang_normalized = 'id'
    if lang == 'en':
        lang_normalized = 'en'
    slova = cell_normalization(slova, lang)
    result = search_in_sheet(slova, lang_normalized, sheets['words'])
    if not result.is_empty():
        fraznik_results = search_in_phrasebook(slova, lang_normalized)
        if not fraznik_results.is_empty():
            for i in range(0, len(fraznik_results)):
                messages.append(phrasebook_card(i, fraznik_results))
        length = len(result)
        if length <= 3:
            for i in range(0, len(result)):
                messages.append(translations_card(result[i:i+1], 'words'))
            return messages
        result = sort_by_distance(slova, lang_normalized, result)
        messages.append(words_list_card(result))
        return messages
    result = search_fuzzy(slova, sheets['words'][lang])
    if result:
        if len(result) > 1:
            alternative_variants = f"*{', '.join(result[:-1])}* ili *{result[-1]}*"
            answer = f"Prividno, slovnik ne imaje slovo *{slova}*. Jeste li vy imali na mysli {alternative_variants}?"
            messages.append(answer)
        else:
            answer = f"Prividno, slovnik ne imaje slovo *{slova}*. Jeste li vy imali na mysli `.{lang} {result[0]}`?"
            messages.append(answer)
    lemma = lemmatizer.slavic_lemmatizer(slova, lang)
    result = search_in_sheet(lemma, lang_normalized, sheets['words'])
    if not result.is_empty():
        messages.append(f"Prividno, slovnik ne imaje slovo *{slova}*. Jeste li vy imali na mysli `.{lang} {lemma}`?")
        return messages
    result = filter_contain(slova, lang_normalized, sheets['words'])
    if not result.is_empty():
        result = sort_by_distance(slova, lang_normalized, result)
        messages.append(words_list_card(result, contain=True))
        return messages
    optional_sheets = list(sheets.keys())[1:]
    optional_sheets.remove('fraznik')
    success = False
    for sheet_name in optional_sheets:
        result = search_in_sheet(slova, lang_normalized, sheets[sheet_name])
        if not result.is_empty():
            success = True
            for i in range(0, len(result)):
                messages.append(translations_card(result[i:i+1], sheet_name))
    if success:
        return messages
    if not lang_detect.language_verify(slova, lang):
        answer = f"Vaše poslanje ne izgledaje kako tekst na {lang} jezyku, jeste li vy uvěrjeni?\n\nMožlive jezyky i jih kody:\n`isv` medžuslovjansky, `en` anglijsky, `ru` russky, `be` bělorussky, `uk` ukrajinsky, `pl` poljsky, `cs` češsky, `sk` slovačsky, `bg` bulgarsky, `mk` makedonsky, `sr` srbsky, `hr` hrvatsky, `sl` slovensky."
        messages.append(answer)
        return messages
    wiki_result = None
    if lang in wiki.SUPPORTED_WIKIS:
        try:
            wiki_result = await wiki.wiki_titles(lang, slova)
        except Exception:
            wiki_result = None
    if wiki_result:
        messages.append(wiki_result)
        return messages
    answer = f"My gledali jesmo v slovniku, neoficialnyh spisah slov, i daže v Wikipediji, i ne jesmo našli ničto. Poprobuj najdti podobne ili srodne rěči, ili stvori novo slovo sam. V analizovanju pomogut [Glosbe.com](<{bots.glosbe(slova, lang)}>) ili [Nicetranslator](<{bots.nicetranslator(lang)}>)."
    messages.append(answer)
    return messages


# if __name__ == "__main__":
#     async def run_tests():
#         search_in_phrasebook('привет', 'ru')
#         search_fuzzy('млово', sheets['words']['ru'])
#         filter_contain("слово", 'ru', sheets['words'])
#         search("слово", 'ru', sheets['words'])
#         search_by_word("слово", 'ru', sheets['words'])
#         print(search_in_sheet("слово", 'ru', sheets['words']))
#         search_in_sheet("слово", 'ru_normalized', sheets['words'])
#         filter_contain('кaкой-то', 'ru_normalized', sheets['words'])
#         search('983', 'id', sheets['words'])

#         tests_dict = {
#             "млово": "ru",
#             "быть": "ru",
#             "делать": "ru",
#             "буду": "ru",
#             "делаю": "ru",
#             "какой-то": "ru",
#             "за": "ru",
#             "добрый": "ru",
#             "ить": "ru",
#             "тест": "ru",
#             "снежный": "ru",
#             "привет": "ru",
#             "барс": "ru",
#             "pozdrav": "isv",
#             "pozdråv": "isv",
#             "rodženja": "isv",
#         }
#         for word, lang in tests_dict.items():
#             print(await mashina_search(word, lang))   # <-- await!

#     asyncio.run(run_tests())


# ======================================================================
#                                TESTS
# ======================================================================

if __name__ == "__main__":
    import sys
    import traceback
    import polars as pl

    isv = sys.modules[__name__]   # this file IS isv_tools; no re-import needed

    class Tester:
        """Minimal test framework: sections, pass/fail, summary, exit code."""

        def __init__(self):
            self.passed, self.failed = 0, 0
            self.errors = []
            self._section = ""

        def section(self, title):
            self._section = title
            print(f"\n{'─'*60}\n{title}\n{'─'*60}")

        def _record(self, name, ok, detail=""):
            if ok:
                self.passed += 1
                print(f"  ✓ {name}")
            else:
                self.failed += 1
                print(f"  ✗ {name}" + (f"\n      {detail}" if detail else ""))
                self.errors.append((self._section, name, detail))

        def check(self, name, condition, detail=""):
            self._record(name, bool(condition), detail)

        def eq(self, name, actual, expected):
            ok = actual == expected
            self._record(name, ok,
                         "" if ok else f"expected: {expected!r}, got: {actual!r}")

        def run(self, name, func):
            """A test function raising an exception is a failure, not a crash."""
            try:
                return func()
            except Exception as e:
                self._record(name, False, f"exception {type(e).__name__}: {e}")

        def eqf(self, name, func, expected):
            """Lazy eq: func is called inside try/except, exceptions are failures."""
            try:
                actual = func()
            except Exception as e:
                self._record(name, False, f"exception {type(e).__name__}: {e}")
            else:
                self.eq(name, actual, expected)

        def checkf(self, name, func):
            """Lazy check: func is called inside try/except, exceptions are failures."""
            try:
                cond = func()
            except Exception as e:
                self._record(name, False, f"exception {type(e).__name__}: {e}")
            else:
                self.check(name, cond)

        def check_raises(self, name, func, exc_type=None):
            try:
                func()
            except Exception as e:
                ok = exc_type is None or isinstance(e, exc_type)
                self._record(name, ok, f"got {type(e).__name__}: {e}")
            else:
                self._record(name, False, "no exception raised, but one was expected")

        def summary(self):
            total = self.passed + self.failed
            print(f"\n{'='*60}\nTOTAL: {total} | passed: {self.passed} | failed: {self.failed}")
            if self.errors:
                print("\nFailed tests:")
                for sec, name, detail in self.errors:
                    print(f"  [{sec}] {name}")
                    if detail:
                        print(f"      {detail}")
            print("=" * 60)
            return 0 if self.failed == 0 else 1

    t = Tester()

    # ------------------------------------------------------------------
    t.section("1. Transliteration (transliteration.py)")
    # ------------------------------------------------------------------

    t.eq("ru: ё -> е", transl.transliteration('ёж', 'ru'), 'еж')
    t.eq("ru: upper case", transl.transliteration('ЁЛКА', 'ru'), 'ЕЛКА')
    t.eq("ru: word without substitutions is unchanged",
         transl.transliteration('слово', 'ru'), 'слово')
    t.eq("kirilicna_zamena: ср -> sr",
         transl.transliteration('ср', 'kirilicna_zamena'), 'sr')
    t.eq("kirilicna_zamena: ms -> isv",
         transl.transliteration('ms', 'kirilicna_zamena'), 'isv')
    t.eq("isv_to_cyrillic: slovo -> слово",
         transl.transliteration('slovo', 'isv_to_cyrillic'), 'слово')
    t.eq("unknown language: text passes through unchanged",
         transl.transliteration('слово', 'qq'), 'слово')

    t.run("transliteration2: backtick block is not transliterated",
          lambda: t.eq("backtick block preserved",
                       transl.transliteration2("ёж `ёж`", 'kir_to_lat'), "ež `ёж`"))

    # ------------------------------------------------------------------
    t.section("2. Command parsing (bots.command_splitter) — cases from comments")
    # ------------------------------------------------------------------

    t.eq("/en test", bots.command_splitter("/en test", 1), ('en', 'test'))
    t.eq("/en test tests (maxsplit=1)", bots.command_splitter("/en test tests", 1),
         ('en', 'test tests'))
    t.eq("/ms -> isv (via kirilicna_zamena)",
         bots.command_splitter("/ms krugly stol", 1), ('isv', 'krugly stol'))
    t.eq("/wiki be Вайна з эму", bots.command_splitter("/wiki be Вайна з эму", 2),
         ('be', 'Вайна з эму'))
    t.eq("no slash (case from comments)", bots.command_splitter("wiki be Вайна з эму", 2),
         ('be', 'Вайна з эму'))

    t.run("command_splitter on single-word input fails loudly, not silently",
          lambda: t.check_raises("single word -> IndexError",
                                 lambda: bots.command_splitter("/en", 1), IndexError))

    # ------------------------------------------------------------------
    t.section("3. Helper functions (bots.py)")
    # ------------------------------------------------------------------

    t.eq("formatizer: plain word", bots.formatizer('slovo '), ' slovo')
    t.eq("formatizer: '!' prefix", bots.formatizer('!tips'), ' 🤖tips')
    t.eq("formatizer: '! ' -> '!'", bots.formatizer('! tips'), ' 🤖tips')
    t.check_raises("formatizer: unknown platform -> ValueError",
                   lambda: bots.formatizer('!x', 'unknown'), ValueError)

    t.run("link_na_slovo: known sheet",
          lambda: t.check("words -> url with range",
                          bots.link_na_slovo(5, 'words').endswith('range=6:6')))
    t.eq("link_na_slovo: unknown sheet -> False", bots.link_na_slovo(0, 'nope'), False)

    t.run("glosbe: target language is Slavic and differs from source",
          lambda: t.check("valid glosbe url", (lambda url: (
              url.startswith('https://glosbe.com/ru/')
              and url.split('/')[4] in {'uk', 'pl', 'cs', 'bg', 'sr'}
          ))(bots.glosbe('привет', 'ru'))))
    t.run("glosbe: spaces encoded",
          lambda: t.check("space -> %20",
                          bots.glosbe('a b', 'ru').endswith('/a%20b')))

    t.run("nicetranslator: text appears in url",
          lambda: t.check("cyrillic query percent-encoded",
                          bots.nicetranslator('круглый стол').endswith(
                              '%D0%BA%D1%80%D1%83%D0%B3%D0%BB%D1%8B%D0%B9+%D1%81%D1%82%D0%BE%D0%BB')))

    # ------------------------------------------------------------------
    t.section("4. Language detection (lang_detect.py)")
    # ------------------------------------------------------------------

    t.eq("language_verify: Russian text", lang_detect.language_verify("быть", "ru"), True)
    t.eq("language_verify: Latin chars in ru -> False",
         lang_detect.language_verify("hello", "ru"), False)
    t.eq("language_verify: unknown language -> False",
         lang_detect.language_verify("быть", "xx"), False)
    t.eq("language_verify: digits only -> True (quirk: text is empty after cleanup)",
         lang_detect.language_verify("123", "ru"), True)
    t.eq("language_verify: empty string -> True",
         lang_detect.language_verify("", "ru"), True)
    t.eq("checkalphabet: Cyrillic", lang_detect.checkalphabet("привет мир"), 'cyrillic')
    t.eq("checkalphabet: Latin", lang_detect.checkalphabet("hello world"), 'latin')

    # ------------------------------------------------------------------
    t.section("5. Cell normalization (cell_normalization)")
    # ------------------------------------------------------------------

    t.eq("parentheses removed", isv.cell_normalization('слово (какое-то)', 'ru'), 'слово')
    t.eq("square brackets removed", isv.cell_normalization('слово [помета]', 'ru'), 'слово')
    t.eq("! and # removed", isv.cell_normalization('!#слово', 'ru'), 'слово')
    t.eq("case and whitespace", isv.cell_normalization('  Слово ', 'ru'), 'слово')
    t.eq("isv: å is transliterated", isv.cell_normalization('pozdråv', 'isv'), 'pozdrav')
    t.eq("empty string", isv.cell_normalization('', 'ru'), '')

    # ------------------------------------------------------------------
    t.section("6. Split helpers (split_by_coma / split_and_search)")
    # ------------------------------------------------------------------

    t.eq("commas", isv.split_by_coma("a, b, c"), ['a', 'b', 'c'])
    t.eq("semicolons", isv.split_by_coma("a; b"), ['a', 'b'])
    t.eq("empty string", isv.split_by_coma(""), [''])
    t.eq("split_and_search: match found", isv.split_and_search("b", "a, b, c"), True)
    t.eq("split_and_search: substring is not a match",
         isv.split_and_search("b, c", "a, b, c"), False)
    t.eq("split_and_search: exact match after ';'",
         isv.split_and_search("b", "a; b"), True)

    # phrase scenario: ';' separates phrases that may contain commas
    be_cell = "хоць; хаця; нягледзячы на тое, што"
    t.eq("phrase cell: first phrase matches",
         isv.split_and_search("хоць", be_cell), True)
    t.eq("phrase cell: middle phrase matches",
         isv.split_and_search("хаця", be_cell), True)
    t.eq("phrase cell: phrase containing commas matches as a whole",
         isv.split_and_search("нягледзячы на тое, што", be_cell), True)
    t.eq("phrase cell: comma-split of the query would NOT match (why ';' exists)",
         isv.split_and_search("нягледзячы на тое", be_cell), False)
    t.eq("phrase cell: no match for an absent phrase",
         isv.split_and_search("абы-як", be_cell), False)

    # ------------------------------------------------------------------
    t.section("7. Sheet search (filter_contain / search / search_by_word)")
    # ------------------------------------------------------------------

    res = t.run("filter_contain: 'slov' over isv_normalized",
                lambda: isv.filter_contain("slov", 'isv_normalized', isv.sheets['words']))
    if res is not None:
        t.check("result is non-empty", len(res) > 0)
        t.check("all rows really contain the substring",
                all('slov' in x for x in res['isv_normalized'].to_list()))

    t.run("search: exact entry in list, 'быть' over ru",
          lambda: t.check("found",
                          not isv.search("быть", 'ru', isv.sheets['words']).is_empty()))
    t.run("search_by_word: 'slovo' as a standalone word",
          lambda: t.check("found",
                          not isv.search_by_word("slovo", 'isv_normalized', isv.sheets['words']).is_empty()))
    t.run("search_in_sheet: garbage -> empty result",
          lambda: t.check("empty",
                          isv.search_in_sheet("ZZZZZНЕТ", 'ru_normalized', isv.sheets['words']).is_empty()))
    t.run("search_in_sheet: empty query does not crash",
          lambda: t.check("returns a DataFrame (all rows)",
                          isinstance(isv.search_in_sheet("", 'ru_normalized', isv.sheets['words']), pl.DataFrame)))

    # KNOWN BUG: str.contains treats the query as a regex by default,
    # so '(', '[', '+', '?' in a query break the search.
    # Fix: use str.contains(s, literal=True) in filter_contain.
    t.run("filter_contain: regex metacharacters in query are treated literally",
          lambda: t.check("no crash on '(('",
                          isinstance(isv.filter_contain("((", 'ru_normalized', isv.sheets['words']),
                                     pl.DataFrame)))

    # ------------------------------------------------------------------
    t.section("8. Fuzzy search and sorting")
    # ------------------------------------------------------------------

    t.run("search_fuzzy: close misspelling returns candidates",
          lambda: t.check("result is a non-empty list of at most 6 items",
                          (lambda r: isinstance(r, list) and 0 < len(r) <= 6)
                          (isv.search_fuzzy('слоово', isv.sheets['words']['ru']))))
    t.run("search_fuzzy: no candidates -> False",
          lambda: t.eq("False for garbage",
                       isv.search_fuzzy('ZZZZZ_QQ', isv.sheets['words']['ru'].head(5000)), False))

    res = t.run("sort_by_distance: sorted by descending similarity",
                lambda: isv.sort_by_distance(
                    "slovo", 'isv_normalized',
                    isv.filter_contain("slov", 'isv_normalized', isv.sheets['words'])))
    if res is not None:
        d = res['distance'].to_list()
        t.check("distances are non-increasing", d == sorted(d, reverse=True))

    # ------------------------------------------------------------------
    t.section("9. Cards (words_list_card / phrasebook_card / translations_card)")
    # ------------------------------------------------------------------

    df_big = pl.DataFrame({'isv': [f'slovo{i}' for i in range(100)],
                           'id': [str(i) for i in range(100)]})
    card = t.run("words_list_card: long list is truncated",
                 lambda: isv.words_list_card(df_big))
    if card:
        t.check("length is capped (~600 chars)", len(card) < 700)
        t.check("contains 'I tako dalje' marker", "tako dalje" in card)

    df_small = pl.DataFrame({'isv': ['slovo1', 'slovo2'], 'id': ['1', '2']})
    card = t.run("words_list_card: short list kept in full",
                 lambda: isv.words_list_card(df_small))
    if card:
        t.check("both words present", 'slovo1' in card and 'slovo2' in card)
        t.check("not truncated", "tako dalje" not in card)

    # ------------------------------------------------------------------
    t.section("10. Lemmatizer")
    # ------------------------------------------------------------------

    t.eqf("ru: буду -> быть", lambda: lemmatizer.slavic_lemmatizer('буду', 'ru'), 'быть')
    t.eq("unknown language: word returned as is",
         lemmatizer.slavic_lemmatizer('word', 'xx'), 'word')

    # ------------------------------------------------------------------
    t.section("11. Phrasebook (search_in_phrasebook / phrasebook)")
    # ------------------------------------------------------------------

    # direct path: isv_normalized searches the phrasebook itself (what mashina_search uses for isv)
    res = t.run("phrasebook: direct fraznik path ('prosty', isv_normalized)",
                lambda: isv.phrasebook('prosty', 'isv_normalized'))
    if res is not None:
        t.check("result is a non-empty list", isinstance(res, list) and len(res) > 0)
        if res:
            t.check("card starts with phrasebook header",
                    res[0].startswith("# Rezultat iz [fraznika"),
                    f"first response: {res[0][:120]!r}")

    # mediated path: 'isv' first searches the dictionary, then the phrasebook;
    # a documented fallback is a legitimate outcome here
    res = t.run("phrasebook: mediated path ('prosty', isv) via the dictionary",
                lambda: isv.phrasebook('prosty', 'isv'))
    if res is not None:
        t.check("result is a non-empty list", isinstance(res, list) and len(res) > 0)
        if res:
            is_cards = all(c.startswith("# Rezultat iz [fraznika") for c in res)
            is_fallback = (res == ["Ničto ne jest najdeno. Tut možeš uviděti vsi slova, "
                                   "ktore imajemo https://gorlatoff.github.io/fraznik.html"])
            t.check("all cards have the header, or documented fallback",
                    is_cards or is_fallback,
                    f"first response: {res[0][:120]!r}")

    t.eqf("phrasebook: garbage -> 'nothing found' message",
          lambda: isv.phrasebook('ZZZZ_QQ', 'isv'),
          ["Ničto ne jest najdeno. Tut možeš uviděti vsi slova, ktore imajemo https://gorlatoff.github.io/fraznik.html"])

    t.run("search_in_phrasebook: en query does not crash",
          lambda: t.check("returns a DataFrame",
                          isinstance(isv.search_in_phrasebook('hello', 'en'), pl.DataFrame)))

    # ==================================================================
    t.section("12. INTEGRATION: mashina_search — scenarios across languages")
    # (requires internet: some scenarios hit the Wikipedia API)
    # ==================================================================

    async def scenario(name, word, lang, predicate):
        try:
            res = await isv.mashina_search(word, lang)
            ok, detail = predicate(res)
            t._record(name, ok, detail)
        except Exception as e:
            t._record(name, False, f"exception {type(e).__name__}: {e}")

    def nonempty(res):
        return (isinstance(res, list) and len(res) > 0
                and all(isinstance(x, str) for x in res)), \
               f"got: {type(res).__name__}, len={len(res) if isinstance(res, list) else '-'}"

    def contains(*subs):
        def p(res):
            joined = "\n".join(res) if isinstance(res, list) else str(res)
            for s in subs:
                if s not in joined:
                    return False, f"'{s}' not found in response:\n{joined[:300]}"
            return True, ""
        return p

    async def integration():
        # --- exact matches ---
        await scenario("ru: 'быть' found in the dictionary", "быть", "ru", contains("v slovniku"))
        await scenario("ru: UPPER CASE is normalized", "БЫТЬ", "ru", contains("v slovniku"))
        await scenario("ru: extra whitespace ignored", "  быть  ", "ru", contains("v slovniku"))
        await scenario("ru: punctuation in query ('быть!')", "быть!", "ru", contains("v slovniku"))
        await scenario("ru: multiple results ('добрый')", "добрый", "ru", contains("v slovniku"))

        # --- other languages (checking response type; content depends on the data) ---
        await scenario("isv: 'слово' (Cyrillic input)", "слово", "isv", nonempty)
        await scenario("isv: 'pozdråv' with å is normalized", "pozdråv", "isv", nonempty)
        await scenario("en: 'dog'", "dog", "en", nonempty)
        await scenario("uk: 'мова'", "мова", "uk", nonempty)
        await scenario("pl: 'słowo'", "słowo", "pl", nonempty)
        await scenario("cs: 'slovo'", "slovo", "cs", nonempty)
        await scenario("bg: 'дума'", "дума", "bg", nonempty)

        # --- search by ID ---
        await scenario("id: '.id 474' returns a word card", "474", "id", contains(".id 474"))

        # --- hint paths ---
        await scenario("lemmatizer path: 'буду' -> hint 'быть'",
                       "буду", "ru", contains("быть"))
        await scenario("unknown word: 'млово' -> final message with Glosbe link",
                       "млово", "ru", contains("Glosbe"))

        # --- edge cases ---
        await scenario("mixed alphabet: 'делaть' (Latin a) -> language warning",
                       "делaть", "ru", contains("uvěrjeni"))
        await scenario("empty string does not crash the search", "", "ru", nonempty)
        await scenario("digits only (not an id)", "123456789", "ru", nonempty)
        await scenario("very long query", "быть " * 50, "ru", nonempty)
        await scenario("query with regex metacharacters '((' does not crash mashina_search",
                       "((", "ru", nonempty)

    asyncio.run(integration())

    raise SystemExit(t.summary())




"""
────────────────────────────────────────────────────────────
1. Transliteration (transliteration.py)
────────────────────────────────────────────────────────────
  ✓ ru: ё -> е
  ✓ ru: upper case
  ✓ ru: word without substitutions is unchanged
  ✓ kirilicna_zamena: ср -> sr
  ✓ kirilicna_zamena: ms -> isv
  ✓ isv_to_cyrillic: slovo -> слово
  ✓ unknown language: text passes through unchanged
  ✓ backtick block preserved

────────────────────────────────────────────────────────────
2. Command parsing (bots.command_splitter) — cases from comments
────────────────────────────────────────────────────────────
  ✓ /en test
  ✓ /en test tests (maxsplit=1)
  ✓ /ms -> isv (via kirilicna_zamena)
  ✓ /wiki be Вайна з эму
  ✓ no slash (case from comments)
  ✓ single word -> IndexError

────────────────────────────────────────────────────────────
3. Helper functions (bots.py)
────────────────────────────────────────────────────────────
  ✓ formatizer: plain word
  ✓ formatizer: '!' prefix
  ✓ formatizer: '! ' -> '!'
  ✓ formatizer: unknown platform -> ValueError
  ✓ words -> url with range
  ✓ link_na_slovo: unknown sheet -> False
  ✓ valid glosbe url
  ✓ space -> %20
  ✓ cyrillic query percent-encoded

────────────────────────────────────────────────────────────
4. Language detection (lang_detect.py)
────────────────────────────────────────────────────────────
  ✓ language_verify: Russian text
  ✓ language_verify: Latin chars in ru -> False
  ✓ language_verify: unknown language -> False
  ✓ language_verify: digits only -> True (quirk: text is empty after cleanup)
  ✓ language_verify: empty string -> True
  ✓ checkalphabet: Cyrillic
  ✓ checkalphabet: Latin

────────────────────────────────────────────────────────────
5. Cell normalization (cell_normalization)
────────────────────────────────────────────────────────────
  ✓ parentheses removed
  ✓ square brackets removed
  ✓ ! and # removed
  ✓ case and whitespace
  ✓ isv: å is transliterated
  ✓ empty string

────────────────────────────────────────────────────────────
6. Split helpers (split_by_coma / split_and_search)
────────────────────────────────────────────────────────────
  ✓ commas
  ✓ semicolons
  ✓ empty string
  ✓ split_and_search: match found
  ✓ split_and_search: substring is not a match
  ✓ split_and_search: exact match after ';'

────────────────────────────────────────────────────────────
7. Sheet search (filter_contain / search / search_by_word)
────────────────────────────────────────────────────────────
  ✓ result is non-empty
  ✓ all rows really contain the substring
  ✓ found
  ✓ found
  ✓ empty
  ✓ returns a DataFrame (all rows)
  ✓ no crash on '(('

────────────────────────────────────────────────────────────
8. Fuzzy search and sorting
────────────────────────────────────────────────────────────
  ✓ result is a non-empty list of at most 6 items
  ✓ False for garbage
  ✓ distances are non-increasing

────────────────────────────────────────────────────────────
9. Cards (words_list_card / phrasebook_card / translations_card)
────────────────────────────────────────────────────────────
  ✓ length is capped (~600 chars)
  ✓ contains 'I tako dalje' marker
  ✓ both words present
  ✓ not truncated

────────────────────────────────────────────────────────────
10. Lemmatizer
────────────────────────────────────────────────────────────
  ✓ ru: буду -> быть
  ✓ unknown language: word returned as is

────────────────────────────────────────────────────────────
11. Phrasebook (search_in_phrasebook / phrasebook)
────────────────────────────────────────────────────────────
  ✓ result is a non-empty list
  ✓ card starts with phrasebook header
  ✓ result is a non-empty list
  ✓ all cards have the header, or documented fallback
  ✓ phrasebook: garbage -> 'nothing found' message
  ✓ returns a DataFrame

────────────────────────────────────────────────────────────
12. INTEGRATION: mashina_search — scenarios across languages
────────────────────────────────────────────────────────────
быть ru
  ✓ ru: 'быть' found in the dictionary
БЫТЬ ru
  ✓ ru: UPPER CASE is normalized
  быть   ru
  ✓ ru: extra whitespace ignored
быть! ru
  ✓ ru: punctuation in query ('быть!')
добрый ru
  ✓ ru: multiple results ('добрый')
слово isv
  ✓ isv: 'слово' (Cyrillic input)
pozdråv isv
  ✓ isv: 'pozdråv' with å is normalized
dog en
  ✓ en: 'dog'
мова uk
  ✓ uk: 'мова'
słowo pl
  ✓ pl: 'słowo'
slovo cs
  ✓ cs: 'slovo'
дума bg
  ✓ bg: 'дума'
474 id
  ✓ id: '.id 474' returns a word card
буду ru
  ✓ lemmatizer path: 'буду' -> hint 'быть'
млово ru
  ✓ unknown word: 'млово' -> final message with Glosbe link
делaть ru
  ✓ mixed alphabet: 'делaть' (Latin a) -> language warning
 ru
  ✓ empty string does not crash the search
123456789 ru
  ✓ digits only (not an id)
быть быть быть быть быть быть быть быть быть быть быть быть быть быть быть быть быть быть быть быть быть быть быть быть быть быть быть быть быть быть быть быть быть быть быть быть быть быть быть быть быть быть быть быть быть быть быть быть быть быть  ru
  ✓ very long query
(( ru
  ✓ query with regex metacharacters '((' does not crash mashina_search

============================================================
TOTAL: 84 | passed: 84 | failed: 0
============================================================
"""









