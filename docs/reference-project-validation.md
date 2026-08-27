# Referensprojektsvalidering – GPT Byggaren

Steg 26 kalibrerar GPT Byggarens profilval mot tre kända projektmönster.

| Referens | Förväntad profil | Varför |
|---|---|---|
| Läroboksskaparen | `standard` | Tydligt arbetsflöde och Knowledge, men inte script-/ZIP-tung runtime |
| Tullverket Remiss | `workflow_research_heavy` | Flerstegsprocess, källor/evidens och spårbarhet |
| ArchiMate Modeller | `zip_first_advanced` | Scripts, schemas, strukturerad modell och projekt-ZIP-hantering |

Dessa fall fungerar som regressionstest för profilval. Steg 26 verifierar den deterministiska klassificeringen; samma fall kan senare användas för kvalitativa LLM-evals.
