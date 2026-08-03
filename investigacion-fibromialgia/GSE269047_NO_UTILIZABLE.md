# GSE269047 — NO UTILIZABLE para validar proxies FM (verificado 2026-08-03)

**Dataset:** GSE269047 "HERV activation segregates ME/CFS from fibromyalgia while defining a novel nosologic entity"
**Archivo:** gse269047_exprs.txt.gz (432MB, descargado; check: proc_054dfc021e64)

## VEREDICTO: item 4 (especificidad FM vs ME/CFS) CERRADO — dataset incompatible

El check de integridad confirma que GSE269047 NO contiene nuestros genes candidatos:

| Gen proxy | Presencia en GSE269047 |
|-----------|------------------------|
| TAC1 | 0 |
| IL6 | 0 |
| OPRM1 | 0 |
| PENK | 0 |
| LGALS3BP | 0 |

## POR QUÉ (formato de IDs)

Las filas usan IDs tipo `0000001-04-HK02-gag_at` / `0000001-04-HK02-gag_st`
(1,394,525 filas). Los sufijos `_gag_at` / `_gag_st` corresponden a transcritos de
**HERV (human endogenous retroviruses)** — el estudio mide activación retroviral
endógena, NO expresión génica estándar (los símbolos Hugo no existen en su anotación).

El dataset es valioso PARA SU PREGUNTA (¿HERV separa ME/CFS de FM?) pero inútil
para la nuestra (¿TAC1/IL6/OPRM1/PENK discriminan FM de ME/CFS?).

## DECISIÓN

- No invertir más tiempo en GSE269047 para validación de proxies.
- La pregunta de especificidad FM vs ME/CFS queda SIN respuesta por ahora —
  requeriría un dataset con expresión génica estándar en ambas condiciones.
- Nota: el error de conda (plugin) en el log no afectó el check — el archivo
  se descargó y verificó correctamente.
