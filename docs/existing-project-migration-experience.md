# Existing-project migration UX – GPT Byggaren

## Mål

Användaren ska kunna uttrycka ett migrationsmål i vanligt språk, till exempel:

- "Migrera denna GPT så att den även fungerar i OpenCode."
- "Lägg till OpenCode-stöd i detta projekt."
- "Gör projektet kompatibelt med OpenCode utan att ändra kärnbeteendet."

Användaren ska inte behöva känna till `--apply`, `--enable-opencode`, adapterfiler eller kontraktsversioner.

## Flöde

När ett befintligt projekt och ett tydligt runtime-mål finns ska GPT Byggaren:

1. inventera projektet,
2. klassificera legacy/current state,
3. identifiera canonical sources,
4. skapa migrationsrapport,
5. bedöma mål-runtimens compatibility,
6. applicera säkra canonical migrationer när användaren uttryckligen bett om migration,
7. aktivera mål-runtimen endast när compatibility är `ready`,
8. lämna manual-review-områden orörda,
9. validera det uppdaterade projektet,
10. sammanfatta vad som ändrades och vad som eventuellt återstår.

## Resultatnivåer

### completed

Säkra migrationer och runtime-aktivering är utförda.

### needs_review

Projektet kan sannolikt stödja runtime-målet men ett konkret område behöver klassificeras, exempelvis scripts som kan vara runtime-tools.

### blocked

En kritisk förutsättning saknas, exempelvis canonical instruktion eller projektkontrakt.

### ready_to_migrate

Analysläge visar att migration kan genomföras säkert men inga förändringar har ännu applicerats.

## Fråga inte om implementationen

Fråga inte användaren:

- om `runtime.opencode` ska läggas till,
- om adapter-schema ska kopieras,
- om migrationsscriptet ska köras med vissa flaggor,
- om contracts ska normaliseras när detta är safe_auto.

Fråga endast när ett verkligt verksamhets- eller semantiskt val återstår.

## Tool-review

Om oklassificerade scripts hittas ska GPT Byggaren inte fråga "ska alla scripts bli tools?".

I stället ska den:

1. inventera scripts,
2. identifiera sannolika runtime-operationer,
3. föreslå semantic id/purpose/requirement/mutation/fallback,
4. be om beslut endast där scriptets funktion inte kan avgöras från projektet.

## Domänbeteende

Migrationen får inte skriva om canonical domänbeteende för att passa runtime-målet.

Rätt princip:

```text
bevara canonical beteende
→ migrera struktur/kontrakt
→ projicera runtime-adapter
→ dokumentera verkliga begränsningar
```

## Intern mekanism

Det användarorienterade workflow-scriptet är:

```text
scripts/migrate_project_for_runtime.py
```

Det kapslar den lägre migrationsmotorn och returnerar:

- target runtime,
- status,
- compatibility,
- changed areas,
- warnings,
- required actions,
- next action,
- teknisk migrationsrapport.

## Nuvarande runtime-stöd

Steg 20 exponerar OpenCode som första fullt integrerade migrationsmål.

Arkitekturen ska kunna utökas med fler runtime-targets utan att ändra användarens sätt att uttrycka önskemålet.

## Definition of Done

- naturligt språk räcker för migrationsintention,
- tekniska CLI-flaggor behöver inte exponeras,
- safe migration appliceras utan onödiga frågor,
- reduced/blocked ger konkret nästa åtgärd,
- canonical beteende bevaras,
- resultatet är maskinläsbart och testat.
