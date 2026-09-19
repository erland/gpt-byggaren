# Runtime compatibility policy

## Referens

Jämför varje registrerad runtime mot canonical assistant-kontraktet. Ingen runtime är automatiskt referensruntime.

## Kategorier

Bedöm requirement-paritet för:

- behavior
- capability
- artifact
- workspace_state
- tool

## States

- equivalent
- reduced
- missing
- not_applicable

Reducerad eller saknad funktion ska ha en konkret motivering när det är relevant.

## Kritikalitet

- critical
- important
- optional

Saknad critical requirement kan göra just den runtime-distributionen `not_viable`.

## Runtime-registrering

Registrera inte en runtime som stödd endast för att schema eller adapterplan finns. Runtime ska först ha en faktisk adapter/buildväg och relevant validering.

## Release

Releasebedömning sker per runtime:

- publish
- publish_with_warning
- do_not_publish

En runtime får rekommenderas framför en annan endast från faktisk compatibilitydata.

## Legacy

Legacyrapporter för Chat ZIP/Custom GPT får normaliseras, men nya rapporter ska använda den generiska modellen.
