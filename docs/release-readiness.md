# Release-readiness assessment – GPT Byggaren

Release readiness är en sammanvägd release gate, inte ett enskilt test.

## Resultat
- `ready`
- `ready_with_warnings`
- `blocked`

## Underlag
Assessment väger in project status, lint, tester/schemas, build, distributionsvalidering, final hygiene, runtime parity, Custom GPT platform validation och kritiska evals.

## Blockerande exempel
- project blocker
- lint error
- critical test/schema-fel
- build fail
- distribution validation fail
- final hygiene blocked
- Custom GPT platform validation blocked
- runtime parity `not_viable` för en distribution som ska publiceras

## Distributioner
Project ZIP, Chat ZIP och Custom GPT bedöms separat och sammanvägt.

## Automation
Samma assessment ska kunna användas vid direktbyggnad och GitHub Release.

## Rapport
Maskinläsbar JSON används av automation. En Markdown-rapport kan användas som releaseartefakt.
