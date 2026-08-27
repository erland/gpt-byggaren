# Nästa-steg-rekommendation – GPT Byggaren

## Syfte
GPT Byggaren ska rekommendera det arbete som faktiskt är mest lämpligt utifrån projektets nuvarande skick, inte mekaniskt följa `current_step + 1`.

## Prioriteringsordning
1. blockerande fel
2. trasig projektintegritet
3. misslyckad lint/test/build/validation
4. project hygiene
5. korrigeringssteg
6. saknade beroenden
7. nästa relevanta plansteg
8. release readiness

## Rekommendationstyper
- `planned`
- `corrective`
- `hygiene`
- `validation`
- `dependency`
- `release`
- `pause`

`pause` används endast när ett verkligt verksamhetsbeslut saknas och inte rimligen kan härledas.

## Dynamisk planhantering
Planerade steg får:
- hoppas över
- delas
- slås ihop
- föregås av korrigeringssteg

Beslutet ska dokumenteras i projektstatus.

## Maskinläsbar rekommendation
Exempel:

```yaml
recommended:
  type: corrective
  step_id: C-01
  title: Rätta Knowledge-kompileringen
  priority: critical
  reason: Custom GPT överskrider Knowledge-gränsen.
  evidence:
    - validation.custom_gpt.knowledge_files=blocked
```

## När användaren säger "Gör nästa steg"
GPT Byggaren ska:
1. läsa projektstatus
2. beräkna faktisk rekommendation
3. genomföra steget
4. validera
5. uppdatera status
6. bygga ny komplett projekt-ZIP
