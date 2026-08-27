# Next-step recommendation policy

- Använd faktisk projektstatus, inte `current_step + 1`.
- Prioritera blockerare, failed validation, hygiene, korrigering och beroenden före planordning.
- Tillåt inserted, skipped, split och merged steps med dokumenterad motivering.
- `pause` används endast för verkliga verksamhetsbeslut som inte kan härledas.
