# Produktvision – GPT Byggaren

## Syfte

GPT Byggaren ska hjälpa en användare från en tidig idé till en fungerande, testad och paketerad GPT utan att användaren behöver känna till detaljerna i Custom GPT Builder, GitHub Actions, distributionsformat eller tekniska plattformsbegränsningar.

GPT Byggaren ska i första hand förstå **vad användaren vill åstadkomma** och själv rekommendera lämplig implementation.

## Målbild

Användaren ska kunna börja med en enkel beskrivning, till exempel:

> Jag vill ha en GPT som hjälper mig analysera remisser.

GPT Byggaren ska därefter:

1. analysera syfte, användare och huvudsakliga arbetsflöden,
2. rekommendera lämplig GPT-arkitektur,
3. rekommendera capabilities och runtime-strategi,
4. skapa en projektspecifik utvecklingsplan,
5. leverera planen som nedladdningsbar Markdown,
6. skapa en projekt-ZIP när första genomförandesteget görs,
7. bygga vidare på projekt-ZIP:en steg för steg,
8. rekommendera nästa steg utifrån både plan och faktisk projektstatus,
9. rensa bort tillfälliga och ersatta arbetsfiler,
10. bygga färdiga distributionsartefakter direkt åt användaren,
11. skapa ett GitHub-redo projekt med automatiserad releasepaketering.

## Primär princip

För större GPT:er är **Chat/ZIP-runtime den primära distributionen**.

Custom GPT ska ses som ett separat distributionsmål som kan vara reducerat eller transformerat om plattformsgränserna gör full funktionell paritet opraktisk.

## Vad GPT Byggaren ska avgöra själv

GPT Byggaren ska som normalfall själv rekommendera:

- om webbsökning behövs,
- om dataanalys behövs,
- om bildgenerering behövs,
- om filer behöver hanteras,
- om strukturerad Knowledge behövs,
- om schemas behövs,
- om scripts behövs,
- om templates behövs,
- om tester och evals behövs,
- om ZIP-first bör användas,
- om Custom GPT bör stödjas,
- vilken ambitionsnivå projektet bör ha.

Användaren ska inte behöva besvara tekniska frågor som GPT Byggaren rimligen kan härleda från idén.

## Vad GPT Byggaren får fråga om

Frågor ska främst avse verkliga verksamhetsval som inte kan härledas, exempelvis:

- vilken målgrupp som är viktigast när flera tydligt olika målgrupper finns,
- om en viss typ av data eller material måste omfattas,
- om ett specifikt arbetsflöde är obligatoriskt eller valfritt,
- om användaren uttryckligen vill avstå från en rekommenderad funktion.

## Fyra huvudsakliga faser

### 1. Idéfas

Sker direkt i chatten.

Resultat:
- analys av idén,
- rekommenderad målbild,
- rekommenderad runtime,
- rekommenderade capabilities,
- preliminär komplexitetsnivå.

### 2. Planfas

GPT Byggaren skapar en nedladdningsbar Markdown-plan med projektspecifika steg.

Planen ska vara tillräckligt detaljerad för att varje steg ska kunna genomföras i en separat prompt.

### 3. Projektfas

När första genomförandesteget görs skapas en komplett projekt-ZIP.

Varje efterföljande steg:
- läser aktuell projektstatus,
- genomför rekommenderat steg,
- testar,
- validerar,
- städar,
- uppdaterar status,
- bygger om projekt-ZIP:en.

### 4. Releasefas

GPT Byggaren ska kunna leverera:

- komplett projekt-ZIP,
- Chat/ZIP-distribution,
- Custom GPT-distribution när aktiverad,
- valideringsrapport,
- checksummor.

GitHub är valfritt. Samma projekt ska kunna packas upp i ett Git-repo och använda GitHub Actions för motsvarande releasebyggen.

## Framgångskriterium

En nybörjare ska kunna gå från:

> Jag har en idé till en GPT.

till:

> Här är mitt kompletta GPT-projekt, min Chat-ZIP och min Custom GPT-distribution.

utan att behöva förstå den underliggande paketerings- och releasearkitekturen.
