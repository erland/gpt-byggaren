# Existing-project migration policy

När användaren uttryckligen vill migrera ett befintligt projekt till en runtime ska detta behandlas som tillstånd att applicera säkra, beteendebevarande migrationer.

## Regler

- Inventera före ändring.
- Bevara canonical instruktion och domänbeteende.
- Applicera safe_auto och auto_with_warning där information inte tappas.
- Applicera aldrig manual_review tyst.
- Aktivera runtime endast när compatibility är ready.
- Vid reduced: genomför inte runtime-aktivering; redovisa exakt blockerande granskningspunkt.
- Vid blocked: ändra inte kritiska osäkra områden.
- Fråga inte om tekniska adapterdetaljer som kan härledas.
- Validera efter lyckad migration.

## OpenCode

För OpenCode används det user-oriented migration workflow som kapslar legacy migration + compatibility + adapter enablement.
