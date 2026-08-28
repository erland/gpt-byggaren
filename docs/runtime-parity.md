# Funktionell paritet mellan runtimes – GPT Byggaren

## Syfte

GPT Byggaren ska kunna beskriva hur väl en Custom GPT-distribution motsvarar den fulla Chat ZIP-runtime.

Paritet ska inte bedömas utifrån antal filer utan utifrån **faktisk funktionalitet**.

Grundprincip:

> Det canonical capability-kontraktet beskriver full målbild. Chat ZIP och Custom GPT jämförs var för sig mot denna capability för capability.

## Paritetsnivåer

Varje capability klassificeras som:

- `equivalent` – funktionen är i praktiken likvärdig,
- `reduced` – funktionen finns men är begränsad,
- `missing` – funktionen saknas,
- `not_applicable` – capabilityn är inte relevant i den aktuella runtime.

## Symboler

För mänskligt läsbara rapporter:

```text
✓  equivalent
~  reduced
-  missing
N/A not_applicable
```

## Capability-katalog

Projektet ska kunna deklarera vilka funktionella capabilities som ska jämföras.

Exempel:

```yaml
capabilities:
  - id: core_workflow
    title: Grundarbetsflöde
    criticality: critical

  - id: web_research
    title: Webbresearch
    criticality: important

  - id: structured_model_handling
    title: Strukturerad modellhantering
    criticality: important

  - id: local_scripts
    title: Lokala projektscripts
    criticality: optional
```

## Kritikalitet

Varje capability ska kunna klassificeras som:

- `critical`
- `important`
- `optional`

### Critical

Om en critical capability saknas i Custom GPT ska GPT Byggaren normalt avråda från Custom GPT som meningsfull distribution.

### Important

Reducerad eller saknad funktion ska dokumenteras och påverka paritetsbedömningen.

### Optional

Kan saknas utan att kärnfunktionen nödvändigtvis påverkas.

## Runtime-matris

Exempel:

```text
Capability                     Chat ZIP   Custom GPT
----------------------------------------------------
Grundarbetsflöde                  ✓           ✓
Webbresearch                      ✓           ✓
Strukturerad modellhantering      ✓           ~
Lokala projektscripts             ✓           -
Avancerad export                  ✓           ~
```

## Maskinläsbar modell

Exempel:

```yaml
capabilities:
  - id: core_workflow
    criticality: critical
    chat_zip: equivalent
    custom_gpt: equivalent

  - id: structured_model_handling
    criticality: important
    chat_zip: equivalent
    custom_gpt: reduced
    reason: >
      Custom GPT använder konsoliderad Knowledge och saknar delar av
      den strukturerade runtime som finns i ZIP.
```

## Paritetspoäng

GPT Byggaren får beräkna en sammanfattande poäng, men poängen får aldrig ersätta capability-matrisen.

Föreslagen viktning:

```text
equivalent = 1.0
reduced    = 0.5
missing    = 0.0
```

Kritikalitet kan viktas:

```text
critical  = 3
important = 2
optional  = 1
```

Exempel:

```text
Weighted parity: 82 %
```

Detta är en översikt, inte en garanti för likvärdig funktion.

## Bedömningsnivåer

Föreslagen sammanfattning:

### `full`

Alla critical och important capabilities är equivalent.

### `high`

Alla critical capabilities är equivalent och endast mindre reduktioner finns.

### `moderate`

Kärnfunktionen fungerar men flera important capabilities är reducerade.

### `low`

Väsentliga funktioner saknas eller är kraftigt reducerade.

### `not_viable`

Minst en central critical capability saknas på ett sätt som gör distributionen missvisande.

## Rekommenderad runtime

Paritetsrapporten ska ange rekommenderad runtime endast när en verklig skillnad i capability eller plattformsbegränsning motiverar det; annars ska distributionerna behandlas som jämbördiga.

Exempel:

```text
Recommended runtime: no default primary; both distributions supported
Custom GPT compatibility: Moderate
```

## Orsaker till reducerad paritet

Vanliga orsaker:

- instruktionsbudget,
- Knowledge-filgräns,
- saknade lokala scripts,
- saknade schemas eller runtimeverktyg,
- reducerad filhantering,
- mer begränsad projektåterupptagning,
- förenklade exportflöden.

## Spårbarhet

Varje reducerad eller saknad capability ska ha en motivering.

Exempel:

```yaml
reason: >
  Custom GPT saknar lokalt query-script och kan därför endast utföra
  förenklad modellnavigering.
```

## Releasebeslut

Paritetsnivån ska påverka releasebeslutet.

### Full/high

Custom GPT kan normalt publiceras.

### Moderate

Kan publiceras om reducerad funktionalitet är tydligt dokumenterad.

### Low

GPT Byggaren ska aktivt varna för den distribution som har låg paritet och rekommendera en annan distribution endast när capability- eller plattformsdata faktiskt motiverar det.

### Not viable

En distribution som saknar kritisk capability ska normalt inte beskrivas som fullt användbar. Den andra distributionen kan fortfarande publiceras om den uppfyller kontraktet.

## `COMPATIBILITY.md`

Paritetsresultatet ska användas för att generera `COMPATIBILITY.md`.

Dokumentet ska minst innehålla:

- rekommenderad runtime endast när verkliga skillnader motiverar det,
- capability-matris,
- reducerade funktioner,
- saknade funktioner,
- sammanfattad paritetsnivå,
- eventuell poäng,
- releasebedömning.

## Direktleverans

När GPT Byggaren bygger båda distributionerna direkt åt användaren ska den även kunna leverera paritetsrapporten som separat artefakt.

Exempel:

```text
my-gpt-parity-report-v1.0.0.md
```

## Definition of Done

Paritetsmodellen är definierad när:

- capabilities jämförs funktionellt,
- kritikalitet finns,
- equivalent/reduced/missing kan uttryckas,
- sammanfattad nivå kan beräknas,
- eventuell runtime-rekommendation grundas på faktisk capability/paritet,
- releasebeslut påverkas,
- rapporten kan användas både mänskligt och maskinläsbart.
