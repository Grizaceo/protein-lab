# Estado de competencias — Proteinbase / Adaptyv

**Actualizado:** 2026-07-04  
**Fuente:** https://proteinbase.com/competitions

## Modo actual: PRACTICAR Y ESPERAR

No hay competencia abierta hoy. Todas las listadas están **Ended**.

| Competencia | Target | Estado | Validación wet-lab | Benchmark |
|-------------|--------|--------|-------------------|-----------|
| GEM x Adaptyv RBX1 | RBX1 (E3 ligase) | Cerrada (mar 2026) | 300 diseños, BLI | 2.8% hit rate; 1 Strong binder (26 nM) |
| Nipah Binder | Nipah G | Cerrada | 1200 diseños | ~9.3% hit rate; mejor KD 370 pM |
| Adaptyv EGFR 1/2 | EGFR | Cerradas | 200–400 diseños | Target más fácil (pocket profundo) |

Adaptyv anuncia competencias futuras en [proteinbase.com/competitions](https://proteinbase.com/competitions) y su blog. Monitorear semanalmente con:

```bash
python binder_design/scripts/monitor_competitions.py
```

## Estrategia mientras no hay competencia abierta

1. Validar pipeline BindCraft sobre **Nipah G (2VSM)** — benchmark público con datos experimentales.
2. Auto-evaluar contra resultados publicados en Proteinbase (colección Nipah).
3. Cuando abra la próxima competencia: generar pool con BindCraft, rankear, enviar ≤100 secuencias.

## Reglas típicas de envío (RBX1 / Nipah como referencia)

- Diseños **de novo** (no motif scaffolding ni lead optimization, salvo sdAb).
- Edit distance ≥25% vs UniRef50 (CDR ≥25% vs SAbDab para anticuerpos).
- ≤250 aa por binder; ≤100 secuencias rankeadas por equipo.
- Method description ≤2 páginas (ver `METHOD_DESCRIPTION_TEMPLATE.md`).
