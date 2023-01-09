import discord
from discord.ext import commands
from bot_config import *

bot = commands.Bot(command_prefix = settings['prefix']) 

def embed_pouka1():
    text = """
:small_orange_diamond: [Slovnik](https://interslavic-dictionary.com/)
:small_orange_diamond: [Slovnik na Android](https://play.google.com/store/apps/details?id=org.interslavicdictionary.twa)

:small_orange_diamond: [Anglijsky kurs gramatiky](http://steen.free.fr/interslavic/grammar.html#advanced_grammar)
:small_orange_diamond: [Transliterator](http://steen.free.fr/interslavic/transliterator.html)
"""
    embed = discord.Embed()
    embed.add_field(name="Važne linky", value=f"{text} ", inline=False)
    return embed 


def embed_pouka2():
    text = """
[za glagoly](http://steen.free.fr/interslavic/conjugator.html) 
[za imenniky ](http://steen.free.fr/interslavic/declinator.html)
[za pridavniky:](http://steen.free.fr/interslavic/adjectivator.html) 
"""
    text2 = """
Na tutom serveru jestvuje tendencija pisati etimologičnym alfabetom. To ne jest nikako obvezno i ty prosto možeš čitati "čudne bukvy" kako jih najvyše blizky vizualny ekvivalent (ę kako e, ć kako č, đ kako dž, ų kako u, å kako a, i.t.d). 

Slovnik uměje prěměnjati pravopis na etimologičny, a takože dělati regionalnu flavorizaciju slov (gledi obrazok)

Ako li ty hčeš poznati to vyše gluboko:    
[Razširjeny etimologičny alfabet na sajtu Jana van Steenbergena:](http://steen.free.fr/interslavic/pronunciation.html#extensions)
[Dobry dokument ob etimologičnom izgovoru](https://cdn.discordapp.com/attachments/759440410014646293/817425631578816562/Naucny_pravopis.docx)
"""

    text3 = """
V něktoryh slučajah jest potrěbno pogleděti na druge jezyky, da by uznati optimalnu metodu skazati něčto. Tut jest [spis resursov](https://teletype.in/@mashine_of_goodness/scyLN60SDhk) (slovniky za vsaky jezyk i tako dalje). 
"""
    embed = discord.Embed()
    embed.add_field(name="Deklinatory i konjungatory", value=f"{text} ", inline=False)
    embed.add_field(name="O etimologičnyh literah", value=f"{text2} ", inline=False)
    embed.add_field(name="Slovniky slovjanskyh jezykov", value=f"{text3} ", inline=False)
    embed.set_image(url="https://media.discordapp.net/attachments/791699552649609219/907562028158312468/TRhFUp9.png")
    return embed



def embed_pouky3():

    teksty = """
[Sbornik tekstov v Medžuviki](https://isv.miraheze.org/wiki/Sbornik:Glavna_stranica)
[Antologija tekstov na medžuslovjanskom](https://books.google.nl/books?id=i3lhDwAAQBAJ&printsec=frontcover#v=onepage&q&f=false) 
[Maly Princ na latinici](http://steen.free.fr/interslavic/maly_princ_lat.pdf) 
[Малы Принц на кирилици](http://steen.free.fr/interslavic/maly_princ_kir.pdf)
"""

    media = """
[Videa](https://youtube.com/playlist?list=PLT_X5HnKrXoiL3a5oK9Tv977JI8ijvFNM)
[Muzika](https://youtube.com/playlist?list=PL--S_Qi-XfGTs4Hpnukm4VyiymJJ5VZqF)
"""
    embed = discord.Embed( title=f"Resursy za pasivno učenje")

    embed.add_field(name="Media", value=f"{media} ", inline=False)
    embed.add_field(name="Teksty", value=f"{teksty} ", inline=False)
    return embed




def embed_pouky4():

    teksty = """
Pročitaj nemnogo [o gramatikě](http://steen.free.fr/interslavic/grammar.html) (ili [tu](https://interslavic-dictionary.com/grammar)), [pisanju](http://steen.free.fr/interslavic/orthography.html) i [čitanju](http://steen.free.fr/interslavic/pronunciation.html). Prěkladaj slova v [slovniku](https://interslavic-dictionary.com/). Govori s ljudami v [Discord-serveru](https://discord.gg/8hBqtf4uej) i ględi kako govoręt oni.

[Video s resursami za učenje medžuslovjanskogo](https://youtu.be/zOgTPTV6Sso)
"""

    embed = discord.Embed()

    embed.add_field(name="KAKO SĘ UČITI", value=f"{teksty} ", inline=False)
    return embed




def embed_pouky5():

    teksty = """
V nastavjeńjah [slovnika](https://interslavic-dictionary.com/) možno izbrati svoj jezyk.

Takože tam sut mnogo drugyh možnostij, kako opcionalne jezyky :flag_nl: :flag_de: :flag_es:, izměnjenje nazvanij/poredka padežev, iskanje na medžuslovjanskom po izměnjenym formam slov i tako dalje.
"""

    embed = discord.Embed()

    embed.add_field(name="Nastavjenja slovnika", value=f"{teksty} ", inline=False)
    embed.set_image(url="https://i.imgur.com/ANXqoQv.png")
    return embed



def embed_pouky6():

    tekst = """
Da by prěvesti slovo, izberi iz kakogo języka potrěbno prěkladati i vpiši potrěbno slovo.

**Važno priměčanje:** to jest slovnik, a ne avtomatičny prěvoditelj. To znači, že on ne može razuměti frazy ili različne od infinitiva formy slov.

*бежать, běžet, chcieć, трчати, дърво* — Dobre zaprosy :thumbsup: 
*бежала, psi utekli, chciałam, трчање, дръвче* — Nedobre :thumbsdown: 
"""

    tekst2 = """
Otvori "prěklady/translations" pod vśakym variantom. Tam možno uviděti, kako slovo jest v najvelikoj kolikosti slovjanskyh językov.
"""

    tekst3 = """
Ne zabyvaj, že slovnik ima funkciju "sklonjenja/conjugation"! Vsaku možlivu formu slova možno pogleděti tam.
"""
    embed = discord.Embed(title=f"Slovnik", url='https://interslavic-dictionary.com/grammar')

    embed.add_field(name="Kako iskati slova", value=f"{tekst} ", inline=False)
    
    embed.add_field(name="Akoli v slovniku jest několiko variantov něktorogo slova:", value=f"{tekst2} ", inline=True)
    embed.add_field(name="O formah slov:", value=f"{tekst3} ", inline=True)

    embed.set_image(url="https://i.imgur.com/kxpV3B6.jpg")
    return embed



def embed_pouky7():

    tekst = """
Takože možno prěględěti [naš fraznik](https://gorlatoff.github.io/fraznik.html), tam jest detaljna informacija o několikyh desetkah najvyše važnyh slov.
"""
    embed = discord.Embed()
    embed.add_field(name="O frazniku", value=f"{tekst} ", inline=False)
    return embed



def embed_pouky8():

    tekst = """
Zaprosite jego u našego bota **@Mašina**, i često budete najdti odgovor. On postupno iskaje slova [vo frazniku](https://gorlatoff.github.io/fraznik.html), vo slovniku medžuslovjanskogo jezyka, v listu s prědloženjami novyh slov, i takože v titulah člankov iz Wikipedije:

Da by uviděti detaljne instrukcije, napišite `.pomoč`. Bot rabotaje na serveru ili takože v ličnyh poslanjah.
"""
    tekst2 = """
Često jest dobro pogleděti kako govoret v drugyh jezykah, tut jest maly [spis resursov](https://teletype.in/@mashine_of_goodness/scyLN60SDhk)

p.s. Vy jeste prěględali jeste vsi možlive varianty i kako prědtym ničto ne razuměte i ne znajete kako slovo potrěbno koristati? Dobrodošli do kanala #vśaky-slovjansky na našem serveru v Diskordu! Može byti, v rěšenju tutogo pytanja vam bųdųt pomogti drugi koristniki togo servera.
"""

    embed = discord.Embed(title="AKO LI SLOVO NE JEST V SLOVNIKU")
    embed.add_field(name="O botu", value=f"{tekst} ", inline=False)
    embed.add_field(name="O slovnikah", value=f"{tekst2} ", inline=False)
    embed.set_image(url="https://i.imgur.com/xKRnA94.jpg")
    return embed



def embed_pouky9():
    text1 = """
Narodne klaviatury, ktore imajut vse potrěbne simboly: **češska**, **slovačska**, **litovska**. Takože možno koristati **hrvatsku** i **slovensku**, a za kirilicu - **srbsku** (ne ima ы/y i е/є), ili **rusinsku** klaviaturu (Њњ i Љљ možno zaměnjati na Нь i Ль, а Jj na Ii).
"""

    text2 = """
:keyboard: Windows — [različne medžuslovjanske klaviatury.](http://tyflonet.com/siciliano/klaviatury/)
:keyboard: Android — [GBoard s opcijeju medžuslovjanskogo jezyka.](http://usachov.eu/g)
:keyboard: Mac — [latinična i kirilična klaviatury]( https://github.com/orlean-git/isv_mac_keyboards). Takože možno uživati medžunarodne klavjatury (napriměr ABC Extended).
:keyboard: iOS — češska/slovačska/litovska klaviatura za latinicu i srbska klaviatura za kirilicu. Da by dodati drugy jezyk, odkrojte `Settings > General > Keyboard > Keyboards`, i natisknite `Add New Keyboard…` 
:keyboard: Linux — razširjena MS latinica na medžunarodnyh latiničnyh klaviaturah (kako napriměr hrvatska v variantu unicodeus). Polna kiriličska klaviatura jest na standardnoj ukrajinskoj klaviaturě.
   
[vyše informacije](https://www.facebook.com/groups/interslavic/permalink/2814961431848977/)
"""
    embed = discord.Embed()
    embed.add_field(name="MEDŽUSLOVJANSKE KLAVIATURY", value=f"{text1} ", inline=False)
    embed.add_field(name="Prěporučenja za različne sistemy:", value=f"{text2} ", inline=False)
    return embed



@bot.command(name="pouka_linky", aliases = ['linky', 'pouka1', 'linky1', 'transliterator', 'gramatika'])
async def fpouka1(ctx):
    await ctx.send(embed = embed_pouka1() )

@bot.command(name="pouka_linky2", aliases = ['linky2', 'pouka2', 'deklinatory', 'konjungatory', 'etimologičny_alfabet'])
async def fpouka2(ctx):
    await ctx.send(embed = embed_pouka2() )

@bot.command(name="pouka_media", aliases = ['pasivno_učenje', 'pouka3'])
async def fpouka3(ctx):
    await ctx.send(embed = embed_pouky3() )

@bot.command(name="pouka_kako_učiti", aliases = ['kako_učiti', 'pouka4'])
async def fpouka4(ctx):
    await ctx.send(embed = embed_pouky4() )

@bot.command(name="pouka_jezyk_slovnika", aliases = ['slovnik1', 'pouka5', 'slovnik', 'nastavjenja'])
async def fpouka5(ctx):
    await ctx.send(embed = embed_pouky5() )

@bot.command(name="pouka_koristanje_slovnika", aliases = ['slovnik2', 'pouka6'])
async def fpouka6(ctx):
    await ctx.send(embed = embed_pouky6() )

@bot.command(name="pouka_o_frazniku", aliases = ['o_frazniku', 'pouka7'])
async def fpouka7(ctx):
    await ctx.send(embed = embed_pouky7() )

@bot.command(name="pouka_o_botu", aliases = ['o_botu', 'pouka8'])
async def fpouka8(ctx):
    await ctx.send(embed = embed_pouky8() )

@bot.command(name="pouka_klaviatury", aliases = ['keyboards','pouka9', 'klaviatury'])
async def fpouka_klaviatury(ctx):
    await ctx.send(embed = embed_pouky9() )






@bot.command(name = 'pomoč', aliases = ['pomoc', 'komandy', 'Komandy', 'commands', 'Commands'])
async def pomogti(ctx):
    text = """
**Iskati po jezyku:**
`.en dog` 
`.ms krugly stol` 
`.ср разумети`, i tako dalje

Tut jest spis možlivyh jezykov i jih kodov:
`isv` medžuslovjansky, `en` anglijsky, `ru` russky, `be` bělorussky, `uk` ukrajinsky, `pl` poljsky, `cs` češsky, `sk` slovačsky, `bg` bulgarsky, `mk` makedonsky, `sr` srbsky, `hr` hrvatsky, `sl` slovensky.

**Da by pokazati slovo po jego ID:**
`.id 474`

**Iskati vo wiki:**
`.wiki en katana`
`.wiki_summary ru собака`

**Spis komand za pokazyvanje pouk:**
`.linky1`, `.linky2`, `.pasivno_učenje`, `.kako_učiti`, `.slovnik1`, `.slovnik2`, `.o_frazniku`, `.o_botu`, `.keyboards`

**Da by obnoviti dane:**
`.obnoviti fraznik` - obnoviti naš fraznik
`.obnoviti` - obnoviti slovnik
    """
    await ctx.send(text) 



@bot.command(aliases = ['pravila', 'правила'])
async def pravila_server(ctx):
    text = ctx.message.content

    if "pravila" in text:
        result = """
Govorimo jedino medžuslovjanskym jezykom vo vsih kanalah kromě:
 <#879457148122316873>
 <#879448593587646464>
 <#879448623534997524>
 <#879456264004980746>
 <#889133830424887307> (tutoj kanal ima tredy/větvy za vsaky slovjansky jezyk)

O politikě možete govoriti jedino medžuslovjanskym jezykom i jedino v kanalu <#879453948631744513>
    """

    if "правила" in text:
        result = """
Говоримо једино меджусловјанскым језыком во всих каналах кромє:
 <#879457148122316873>
 <#879448593587646464>
 <#879448623534997524>
 <#879456264004980746>
 <#889133830424887307> (тутој канал има треды/вєтвы за всакы словјанскы језык)

О политикє можете говорити једино меджусловјанскым језыком и једино в каналу <#879453948631744513>
    """

    await ctx.send( result )