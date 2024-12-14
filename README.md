## Komandy bota:

**Iskati po jezyku:**
`.en dog` 
`.ms krugly stol` 
`.sr razumeti`, i tako dalje

Možlive jezyky i jih kody:
`isv` medžuslovjansky, `en` anglijsky, `ru` russky, `be` bělorussky, `uk` ukrajinsky, `pl` poljsky, `cs` češsky, `sk` slovačsky, `bg` bulgarsky, `mk` makedonsky, `sr` srbsky, `hr` hrvatsky, `sl` slovenečsky.

**Da by pokazati slovo po jego ID:**
`.id 474`

**Iskati vo viki:**
`.wiki en katana`
`.wiki_summary ru sobaka`

**Prikazy za pokazyvanje pouk:**
`.linky1`, `.linky2`, `.pasivno_učenje`, `.kako_učiti`, `.slovnik1`, `.slovnik2`, `.o_frazniku`, `.o_botu`, `.keyboards`

**Da by obnoviti dane:**
`.obnovi words` — obnoviti jedino oficialny slovnik
`.obnovi suggestions` — obnoviti tabelu prědloženij do slovnika
`.obnovi fraznik` — obnoviti naš fraznik
`.obnovi wiki list` — obnoviti korpus slov (prva tabela)
`.obnovi cognates` — obnoviti korpus slov
`.obnovi` — obnoviti vsečto

## Za rabotu koda:

Potrěbne biblioteky:

```bash
pip install PyYAML polars disnake RapidFuzz lemmagen3 pyTelegramBotAPI regex aiohttp
```

Takože za svojego bota potrěbno stvoriti Discord aplikaciju:

https://discord.com/developers/applications/

https://habr.com/ru/post/511454/
