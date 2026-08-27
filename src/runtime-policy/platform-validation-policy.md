# Platform validation policy

## Regel

Validera den faktiska Custom GPT-distributionen före release.

## Blockera vid

- instruktion över konfigurerad gräns,
- för många Knowledge-filer,
- saknade Builder-filer,
- tom instruktion,
- saknade deklarerade Knowledge-filer,
- missvisande kärnfunktion,
- förbjudna utvecklingsartefakter i distributionen.

## Varning

Reducerad funktionalitet får ge warning om den är tydligt dokumenterad.

## Konfiguration

Plattformsgränser ska läsas från `gpt-project.yaml`.

## Samma logik

Lokal build, CI och GitHub Release ska använda samma valideringsregler.
