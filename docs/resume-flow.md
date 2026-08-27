# Resume flow – GPT Byggaren

Projekt-ZIP ska kunna återuppta utvecklingen utan tidigare chathistorik.

## Läsordning
1. `gpt-project.yaml`
2. `project-status.yaml`
3. `docs/development-plan.md`
4. `STATUS.md`
5. `PROJECT.md`
6. relevanta canonical sources

`project-status.yaml` är primär statuskälla.

## Resume-status
- `ready`
- `ready_with_warnings`
- `needs_correction`
- `blocked`
- `legacy_or_unknown`

## Verifiering
Kör i första hand lint och next-step recommendation. Vid behov körs tester, build och distributionsvalidering.

## Legacy
Projekt utan `gpt-project.yaml` inventeras som legacy/unknown och migreras innan normal resume.

## Regel
Be inte användaren återberätta projekthistorik som redan finns i projekt-ZIP:en.
