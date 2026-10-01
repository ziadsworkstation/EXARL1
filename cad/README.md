# EXAR · L1 — Slatted Chair "TI 1A" (Marcel Breuer, 1922-24)

Part CAD de la pràctica L1 (Composició i proporció).

| Fitxer | Contingut |
|---|---|
| `EXAR_L1_cadira_breuer.dxf` | Làmina A3 a escala 1:10 (espai model): alçat, perfil esquerre i planta acotats (sistema europeu) + perspectiva isomètrica. Capes: FUSTA, TELA, COTES, EIXOS, MARC, CAIXETI, TEXT. Obre amb AutoCAD / LibreCAD / DraftSight. |
| `EXAR_L1_cadira_breuer_CAD.pdf` | Exportació PDF de la làmina. |
| `EXAR_L1_cadira_breuer_3D.stl` | Model 3D de la cadira (mm). |
| `cadira_breuer.py` | Generador paramètric (`pip install ezdxf matplotlib` → `python3 cadira_breuer.py --pdf`). |

## Mòdul i proporcions (proposta)

Mòdul base **M = 40 mm** (secció quadrada dels llistons, 40 × 40).

| Element | Mida | En mòduls |
|---|---|---|
| Amplada total | 560 | 14 M |
| Profunditat total | 560 | 14 M |
| Alçada total | 960 | 24 M |
| Travesser lateral (cara inferior) | 240 | 6 M |
| Seient davant / darrere | 440 / 360 | 11 M / 9 M |
| Pota posterior = base del braç | 640 | 16 M |
| Posició pota posterior (des de davant) | 400 | 10 M |
| Voladís davanter del braç | 80 | 2 M |
| Cinga respatller inferior / superior | 480–600 / 840–940 | 12–15 M / 21–23,5 M |

La planta és un quadrat (14 M × 14 M) i l'alçada total és 24 M (relació 7:12).
Per canviar qualsevol mida, edita les constants al principi de `cadira_breuer.py` i regenera.
