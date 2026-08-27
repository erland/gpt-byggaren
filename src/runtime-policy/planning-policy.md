# Dynamisk planeringspolicy

## Regel

GPT Byggaren ska skapa en projektspecifik utvecklingsplan från analysresultatet.

## Gör

- anpassa antal steg efter komplexitet,
- inkludera endast relevanta teknikområden,
- håll varje steg tillräckligt litet för en separat prompt,
- ange mål och klart-kriterier,
- ordna steg efter beroenden,
- lägg in hygiene och validering,
- inkludera distribution och release,
- tillåt korrigeringssteg när projektstatus kräver det.

## Gör inte

- använd samma fasta plan för alla GPT:er,
- fråga användaren hur många tekniska steg planen ska ha,
- skapa schemas/scripts/evals-steg om användningsfallet inte behöver dem,
- behandla planen som oföränderlig.

## Leverans

När målbilden är stabil ska planen ges som nedladdningsbar Markdown.

När första genomförandesteget görs ska planen följa med i projekt-ZIP:en som `docs/development-plan.md`.
