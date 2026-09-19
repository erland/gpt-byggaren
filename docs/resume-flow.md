# Resume flow – GPT Byggaren

Projektpaketet ska kunna återuppta utvecklingen utan tidigare chathistorik.

Detta är ett konkret exempel på det generella workspace/state-kontraktet: projektpaketet är workspace och `project-status.yaml` är dess auktoritativa state. En annan skapad assistent kan använda en annan statefil eller klara sig utan persistent state.

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
Be inte användaren återberätta projekthistorik som redan finns i workspace/state. Chatthistorik får vara ett komplement men inte enda sanningskälla när kontraktet kräver persistent state.
