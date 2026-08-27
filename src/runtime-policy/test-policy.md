# Test policy

## Princip

Använd deterministiska tester när korrekt utfall kan fastställas exakt.
Använd evals när kvalitet måste bedömas mot kriterier.

## Regression

Varje reproducerbar bugg bör om möjligt få ett permanent regressionstest eller evalfall.

## Kritikalitet

- critical
- important
- optional

Critical fel blockerar release.

## Projektprofil

Testdjupet ska anpassas efter simple, standard, zip_first_advanced eller workflow_research_heavy.

## Distribution

`tests/` och `evals/` är development-material och följer normalt inte med runtime.
