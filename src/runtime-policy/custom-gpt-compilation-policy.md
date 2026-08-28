# Custom GPT compilation policy

## Roll

Custom GPT är ett separat kompileringsmål.

## Prioritet

Bevara kärnbeteende före full filparitet.

## Instruktion

Använd `identical`, `compressed` eller `compiled` strategi beroende på behov. Kompilering ska vara konservativ och verifiera `core_contract` efter transformation.

## Knowledge

Använd `identical`, `consolidate`, `prioritize` eller `hybrid`. Vid prioritering ska deklarerade semantic priority-globs användas före filordning.

## Gränser

Läs plattformsgränser från `gpt-project.yaml`.

## Capabilities

Härled rekommenderade Builder-inställningar från analysmodellen.

## Reducerad funktion

Dokumentera skillnader i `COMPATIBILITY.md`.

## Blockera

Bygg inte en Custom GPT-distribution som överskrider gränser eller ger en missvisande bild av kärnfunktionen.
