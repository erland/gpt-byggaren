# Maintenance fix M1 – CI-testisolering och runtime-cache

## Bakgrund
GitHub Actions run `33034383995` föll i teststeget.

## Grundorsaker
1. `scripts/lib/__pycache__` skapades av Python under testkörningen och följde med in i Chat ZIP.
2. Linter-testet var beroende av testordning och såg build/dist från tidigare tester.
3. Next-step- och resume-testerna var hårdkodade till steg 21 trots att projektet gått vidare till steg 30/maintenance.

## Åtgärder
- Runtime copy filtrerar alltid caches samt `.pyc`/`.pyo`.
- Linter-testet städar genererat tillstånd rekursivt före test.
- Statusrelaterade tester härleder förväntat värde från `project-status.yaml`.
- Regressionstest säkerställer att importskapad `__pycache__` aldrig paketeras i Chat ZIP.
