# MAMMAL DTI — Predicción de Binding Affinity (pKd)
**Modelo:** `ibm/biomed.omics.bl.sm.ma-ted-458m.dti_bindingdb_pkd`
**Fecha:** 2026-05-14

## Predicciones directas (fármaco → su target)

| Fármaco | Target | Tier | pKd | Kd (M) | Interpretación |
|---------|--------|------|-----|--------|---------------|
| naltrexona_LDN | MOR | Tier2 | 6.91 | 1.22e-07 | Afinidad moderada (µM) |
| dimetil_fumarato | NRF2 | Tier1 | 5.88 | 1.31e-06 | Afinidad baja (mM) |
| suzetrigine_VX548 | Nav1.8 | Tier1 | ❌ ERROR | — |  |
| TAK242_resatorvid | TLR4 | Tier2 | 5.95 | 1.11e-06 | Afinidad baja (mM) |

**Mejor afinidad predicha:** naltrexona_LDN → MOR (pKd=6.91)

## Cross-predicciones top-10

| Fármaco | Target | pKd | Interpretación |
|---------|--------|-----|---------------|
| TAK242_resatorvid | MOR | 7.02 | Afinidad moderada (µM) |
| suzetrigine_VX548 | MOR | 6.91 | Afinidad moderada (µM) |
| dimetil_fumarato | MOR | 6.84 | Afinidad moderada (µM) |
| TAK242_resatorvid | MS4A2/FcεRIβ | 6.30 | Afinidad moderada (µM) |
| naltrexona_LDN | MS4A2/FcεRIβ | 6.26 | Afinidad moderada (µM) |
| suzetrigine_VX548 | MS4A2/FcεRIβ | 6.24 | Afinidad moderada (µM) |
| dimetil_fumarato | MS4A2/FcεRIβ | 6.14 | Afinidad moderada (µM) |
| TAK242_resatorvid | HDC | 5.99 | Afinidad baja (mM) |
| naltrexona_LDN | HDC | 5.98 | Afinidad baja (mM) |
| TAK242_resatorvid | NRF2 | 5.97 | Afinidad baja (mM) |

---
*Pipeline: MAMMAL DTI v2 | DAVI + Cristóbal | 2026-05-14*