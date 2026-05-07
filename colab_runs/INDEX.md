# colab_runs — Índice Global

**Actualizado:** 2026-05-07 08:29
**Pipeline:** RFdiffusion → ProteinMPNN → AF2 multimer scoring
**Higiene:** 2026-05-07 — mock runs archivados, duplicados eliminados

---

## Nipah G Binder (2VSM chain A)
**Iteración total:** 11  |  **Mejor score real:** 0.2802 (2026-04-23_test_2vsm)
**Stuck count:** 0

| Run | pLDDT (mean/best) | ipTM | pAE | Diseños | Complex? | Score |
|-----|-------------------|------|-----|---------|----------|-------|
| 2026-04-22_diffusion_test | 0.91 / 0.935 | — | 3.8 | 8 | — | 0.0910 |
| 2026-04-22_diffusion_test_qccnm | 0.883 / 0.899 | — | 4.1 | 8 | — | 0.0883 |
| 2026-04-22_diffusion_test_yijv1 | None / None | — | — | 8 | — | 0.0000 |
| 2026-04-22_test_bmu6c | 0.905 / 0.936 | — | 3.9 | 8 | — | 0.0905 |
| 2026-04-23_test_2vsm | 0.815 / 0.93 | 0.157 | 27.8 | 64 | — | 0.2802 |
| 2026-04-24_test.result | 0.7569 / 0.9153 | 0.1604 | 27.7993 | 64 | ✅ | 0.2710 |
| 2026-04-24_test_bmu6c.result | 0.8952 / 0.9357 | — | 5.649 | 8 | — | 0.0895 |
| 2026-04-27_nipah_iter4.result | 0.8639 / 0.9776 | — | 6.0151 | 64 | — | 0.0864 |
| 2026-04-27_nipah_iter7.result | 0.8221 / 0.9663 | — | 7.0053 | 32 | — | 0.0822 |
| 2026-04-27_nipah_iter8.result(1) | 0.912 / 0.9746 | — | 5.1236 | 64 | — | 0.0912 |
| 2026-04-27_nipah_iter9.result | 0.8559 / 0.9773 | — | 5.4845 | 128 | — | 0.0856 |
| 2026-04-27_nipah_iter8_complex_test_32468.res | None / None | 0.18 | — | 1 | ✅ | 0.1260 |

## Ferritin Biosensor (1BFR — CYS mutation validation)
**Iteración total:** 4  |  **Mejor score real:** 0.2349 (2026-04-27_ferritin_iter2.result)
**Stuck count:** 0

| Run | pLDDT (mean/best) | ipTM | pAE | Diseños | Complex? | Score |
|-----|-------------------|------|-----|---------|----------|-------|
| 2026-04-27_ferritin_iter1.result | 0.7871 / 0.9153 | 0.0619 | 22.9732 | 32 | ✅ | 0.2242 |
| 2026-04-27_ferritin_iter2.result | 0.8648 / 0.9498 | 0.0513 | 22.2016 | 64 | ✅ | 0.2349 |
| 2026-04-27_ferritin_iter3.result | 0.8371 / 0.9409 | 0.0629 | 23.2634 | 32 | ✅ | 0.2339 |

---

## Criterios de éxito (Sappington 2026)

| Métrica | Umbral mínimo | Estado actual |
|---------|---------------|---------------|
| pLDDT > 0.85 | Nipah: ✅ | Ferritin: ✅ |
| ipTM > 0.50  | Nipah: 🔴 (max ~0.16) | Ferritin: 🔴 (max ~0.06) |

## Notas post-higiene

- **Mock runs archivados** en `archive/mock_runs/` — no representan corridas reales
- **Duplicados eliminados:** nipah_iter4/ y outputs/ sueltos
- **15 corridas reales** conservadas en colab_runs/
- **Próximo paso:** ipTM es el cuello de botella. RFdiffusion con 50 pasos T + AF2 en T4 de Colab no está generando binders con ipTM >0.16 en Nipah ni >0.06 en Ferritin