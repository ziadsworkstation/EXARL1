# EXAR · L1 — Slatted Chair "TI 1A" (Marcel Breuer, 1922-24)

Part CAD de la pràctica L1 (Composició i proporció).

| Fitxer | Contingut |
|---|---|
| `EXAR_L1_cadira_breuer.dxf` | Làmina A3 a escala 1:10 (espai model): alçat, perfil esquerre i planta acotats (sistema europeu) + perspectiva isomètrica. Capes: FUSTA, TELA, COTES, EIXOS, MARC, CAIXETI, TEXT. Obre amb AutoCAD / LibreCAD / DraftSight. |
| `EXAR_L1_cadira_breuer_CAD.pdf` | Exportació PDF de la làmina. |
| `EXAR_L1_cadira_breuer_3D.stl` | Model 3D de la cadira (mm). |
| `cadira_breuer.py` | Generador paramètric (`pip install ezdxf matplotlib` → `python3 cadira_breuer.py --pdf`). |

## Fonts

Mides reals: 96 × 57 × 57,5 cm (H × A × P). Segona versió (1924): tota l'estructura
es fa amb **un únic llistó estandarditzat** (~25 × 54 mm) i només en canvia la llargada.
Les teles (seient i dues cinghes del respatller) es dibuixen com a **làmines sòlides** de 6 mm.

## Mòdul i proporcions (proposta)

Mòdul base **M = 48 mm** = amplada del llistó; llistó tipus **24 × 48 (½M × M)**.

| Element | Mida (mm) | Mòduls |
|---|---|---|
| Amplada × profunditat × alçada | 576 × 576 × 960 | 12M × 12M × 20M (planta quadrada, alçat 3:5) |
| Pota davantera | 432 | 9M |
| Travesser lateral (cantell) | 336–384 | 7M–8M |
| Seient davant / darrere (làmina inclinada) | 408 / 360 | 8,5M / 7,5M |
| Pota posterior = sota del braç | 600 | 12,5M |
| Braç (24 × 48, pla) | 600–624, voladís 96 | 2M de voladís |
| Làmina respatller inferior / superior | 480–576 / 768–864 | 10M–12M / 16M–18M |
| Suport de la làmina superior | fins a 912 | 19M |

Estructura en dos plans laterals: **exterior** (potes davanteres + travessers laterals)
i **interior** (potes posteriors, pals del respatller, braços i suports), units per
3 travessers transversals → 18 llistons en total.
