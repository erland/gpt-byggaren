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


## Contract snapshot

Builden ska skriva `builder/runtime-contract.json` som en genererad snapshot av canonical capability-, artifact-, workspace/state- och tool-kontrakten för runtime-id `chatgpt_custom`.

Snapshoten får inte bli en ny canonical källa.

## Tools

Custom GPT Builder-paketet bäddar inte in lokala scripts eller local commands. Tool-kontraktet ska ändå följa med i snapshoten så att reducerad eller saknad funktion kan beskrivas och senare användas i den generella runtime compatibility-bedömningen.
