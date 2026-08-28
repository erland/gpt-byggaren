# GPT lint policy

- Kör statisk lint före tester och build.
- `error` blockerar CI.
- `warning` kräver bedömning men blockerar normalt inte.
- Auto-radera inte osäkra filer utifrån namn.

## Runtime complexity

När projektet deklarerar `instructions.core_contract` ska linter verifiera att kritiska invariants finns i canonical instruktionen och att kärnflödet inte kräver fler obligatoriska filhopp än den deklarerade budgeten. Knowledge får aldrig vara ett obligatoriskt beroende för kärnbeteende.
