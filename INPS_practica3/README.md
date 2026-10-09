# Pràctica 3 INPS — Interacció amb Visió

- `practica3.m`: script principal. Demana una imatge (per defecte `imatges/figures1.jpg`), detecta cada figura i l'etiqueta com a `<forma><color><mida>`:
  - Forma: `C` cercle, `T` triangle, `S` quadrat
  - Color: `R` vermell, `G` verd, `B` blau
  - Mida (opcional): `1` petita, `2` mitjana, `3` gran
- `ejemploVision.m`: exemple d'Atenea del qual parteix la pràctica.
- `imatges/`: imatges de prova.

## Mètode
1. Màscara binària per a cada color: un canal > 128 i els altres dos < 100.
2. Neteja amb `bwareaopen`, `imfill` i una obertura (`imerode` + `imdilate`).
3. `bwconncomp` + `regionprops` → àrea, bounding box i centroide.
4. Forma segons l'*extent* (àrea / àrea de la bounding box): quadrat ≈ 1, cercle ≈ π/4 ≈ 0,785, triangle ≈ 0,5.
5. Mida: dins de cada forma s'ordenen les tres figures per àrea (1, 2, 3).
