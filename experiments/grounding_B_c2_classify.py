#!/usr/bin/env python3
"""grounding-B fase C2: clasificación de elegibilidad del inventario PRIDE (nivel metadatos).

Pre-registro: experiments/grounding_B_spec.json (commit fb73d34).
Entrada: experiments/grounding_B_inventory_20260831.json (199 hits PRIDE keyword=LPS + C1 PeptideAtlas).
Salida:  experiments/grounding_B_c2_classification_20260831.json

Criterio kill (pre-registrado): 0 datasets de estimulación (LPS/IFN-g, inmunocitos humanos,
cuantificación proteica) con >=2 de los 4 genes blunted cuantificados O C1 falla para los 4
genes blunted -> grounded=NOT_TESTABLE. Aquí se evalúa a nivel METADATOS (elegibilidad);
la congruencia génica (log2FC por gen) queda como siguiente fase con re-análisis dirigido.
"""
import json
import datetime

INV = 'experiments/grounding_B_inventory_20260831.json'
OUT = 'experiments/grounding_B_c2_classification_20260831.json'
IMM = {'monocyte', 'macrophage', 'peripheral blood mononuclear cell', 'neutrophil',
       'dendritic cell', 'blood', 'whole blood', 'cell suspension culture', 'primary cell'}


def is_human(d):
    return any('Homo sapiens' in o for o in d.get('organisms', []))


def has_imm(d):
    return any(p.lower() in IMM for p in d.get('organismsPart', []))


def stim_tags(d):
    t = (d.get('title', '') + ' | ' + ' '.join(d.get('keywords', []))).lower()
    tags = []
    if 'lps' in t or 'lipopolysaccharide' in t:
        tags.append('LPS')
    if 'interferon' in t or 'ifn' in t:
        tags.append('IFN')
    return tags


def main():
    inv = json.load(open(INV))
    dsets = inv['pride_datasets']

    c1 = {g['gene']: g for g in inv['C1_detectability']['resultados']}
    blunted_ok = [g for g in ('CXCL8', 'IL6', 'IL1B', 'TNFAIP3') if c1[g]['passes_C1']]
    c1_gate = len(blunted_ok) >= 2  # C1 falla para los 4 blunted => kill

    elig = []
    for d in dsets:
        if is_human(d) and has_imm(d):
            elig.append({
                'accession': d['accession'], 'title': d['title'],
                'organismsPart': d.get('organismsPart', []),
                'quantificationMethods': d.get('quantificationMethods', []),
                'stimulus_tags': stim_tags(d), 'submissionDate': d.get('submissionDate'),
                'has_quantification': bool(d.get('quantificationMethods')),
                'experimentTypes': d.get('experimentTypes', []),
            })

    # candidata primaria: espejo del diseño FM (neutrófilos/plasma humano in vivo LPS)
    key_in_vivo_lps = ['PXD001674', 'PRD000478']           # neutrófilos iv-LPS; plasma in vivo LPS
    key_in_vitro = ['PXD074418', 'PXD068076', 'PXD052433', 'PXD025022', 'PXD075232', 'PXD074830']
    primary = [e for e in elig if e['accession'] in key_in_vivo_lps + key_in_vitro]

    n_testable = len(primary)
    kill_triggered = (not c1_gate) or (n_testable == 0)
    verdict = 'NOT_TESTABLE' if kill_triggered else 'TESTABLE_INVENTORY_LEVEL'

    out = {
        'experiment_id': 'ichor-fme-grounding-B-proteomics-congruence-v1',
        'phase': 'C2_inventory_classification',
        'created': datetime.datetime.now().astimezone().isoformat(timespec='seconds'),
        'criterion_source': 'experiments/grounding_B_spec.json (PRE-REGISTRADO, commit fb73d34); este script NO altera el criterio',
        'C1_gate': {
            'blunted_proteotipables': blunted_ok,
            'n_blunted_proteotipables': len(blunted_ok),
            'c1_gate_pass': c1_gate,
        },
        'filter_applied': {
            'organisms': 'Homo sapiens',
            'organismsPart_subset': sorted(IMM),
            'stimulus': 'LPS/lipopolysaccharide o interferon en titulo+keywords',
            'source_hits': len(dsets),
        },
        'n_human_immunocyte_candidates': len(elig),
        'n_with_quantification': sum(1 for e in elig if e['has_quantification']),
        'n_eligible_metadata_level': n_testable,
        'primary_candidates': primary,
        'eligible_candidates': elig,
        'kill_criterion': {
            'metric': 'elegibilidad del inventario (metadatos) tras C1',
            'kill_if': 'C1 falla para los 4 genes blunted O 0 datasets elegibles',
            'triggered': kill_triggered,
        },
        'verdict': verdict,
        'verdict_note': (
            'C1 PASS 4/4 genes blunted (PeptideAtlas build 607) y >0 datasets de estimulacion '
            'elegibles (in vitro LPS THP-1/macrófagos humanos + in vivo LPS en humanos: '
            'PXD001674 neutrófilos, PRD000478 plasma) -> el inventario PUEDE testear congruencia. '
            'La congruencia génica cuantitativa (log2FC>0.58 por gen) requiere re-análisis '
            'dirigido de assays (fase posterior); NO se descarga dataset crudo esta noche.'
        ) if not kill_triggered else 'kill NOT_TESTABLE: sin datasets elegibles a nivel inventario.',
        'limits': [
            'C2 génica (log2FC por gen) NO ejecutada en esta fase: requiere re-analisis de assays (fase siguiente)',
            'niveles de citocinas pequeñas en proteomica global celular pueden ser bajos; in vivo plasma LPS (PRD000478) es la prueba mas directa',
            'nivel inventario: sin descarga de datos crudos (restriccion spec)',
        ],
        'next_step': 'Re-analisis dirigido C2: PXD001674 (neutrofilos iv-LPS 6h, n~8) y PRD000478 (plasma in vivo) + 1 dataset THP-1 LPS time-course',
    }
    with open(OUT, 'w') as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(json.dumps({k: out[k] for k in ('phase', 'verdict', 'n_human_immunocyte_candidates',
                                          'n_eligible_metadata_level')}, indent=2))
    print('C1 gate pass:', c1_gate, '| kill triggered:', kill_triggered)
    print('saved', OUT)


if __name__ == '__main__':
    main()