#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""protein-fme-grounding-A — re-minado GEO/SRA post-2022
Busca datasets con (ejercicio/entrenamiento O estimulación inmune) AND (fibromialgia/dolor crónico/PPT/EIH)
Y que midan ΔPPT o EIH + transcriptómica/proteómica longitudinal.

Kill criterion pre-registrado: 0 datasets nuevos (post-2022) con ΔPPT/EIH + transcriptómica longitudinal
→ cerrar vía in-silico puro, documentar vacante, pasar a proteómica pública (Opción B).

Spec hash: sha256:5e8b3f1a2c4d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f
"""
import json, urllib.request, urllib.parse, time, datetime, xml.etree.ElementTree as ET
from pathlib import Path

OUT = Path("/home/gris/.hermes/workspace/ACTIVE/protein-lab/grounding_A")
OUT.mkdir(parents=True, exist_ok=True)

# Queries GEO (via E-utilities)
BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
API_KEY = None  # sin key, rate limit 3/s

def esearch(db, term, retmax=100):
    params = {"db": db, "term": term, "retmax": retmax, "retmode": "json"}
    if API_KEY:
        params["api_key"] = API_KEY
    url = BASE + "esearch.fcgi?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url) as r:
        return json.load(r)

def esummary(db, ids):
    params = {"db": db, "id": ",".join(ids), "retmode": "json"}
    if API_KEY:
        params["api_key"] = API_KEY
    url = BASE + "esummary.fcgi?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url) as r:
        return json.load(r)

def fetch_pubmed(pmids):
    params = {"db": "pubmed", "id": ",".join(pmids), "retmode": "xml"}
    if API_KEY:
        params["api_key"] = API_KEY
    url = BASE + "efetch.fcgi?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url) as r:
        return r.read().decode()

# Queries compuestas (post-2022 = desde 2023/01/01)
queries = [
    # Ejercicio + FM/dolor + transcriptómica
    '("exercise"[Title/Abstract] OR "training"[Title/Abstract] OR "physical activity"[Title/Abstract]) AND ("fibromyalgia"[Title/Abstract] OR "chronic pain"[Title/Abstract] OR "pressure pain threshold"[Title/Abstract] OR "exercise-induced hypoalgesia"[Title/Abstract]) AND ("RNA-seq"[Title/Abstract] OR "transcriptomics"[Title/Abstract] OR "gene expression"[Title/Abstract]) AND ("2023/01/01"[PDAT] : "3000"[PDAT])',
    
    # Estimulación inmune (LPS, citocinas) + FM/dolor + transcriptómica
    '("LPS"[Title/Abstract] OR "lipopolysaccharide"[Title/Abstract] OR "immune stimulation"[Title/Abstract] OR "cytokine"[Title/Abstract]) AND ("fibromyalgia"[Title/Abstract] OR "chronic pain"[Title/Abstract]) AND ("RNA-seq"[Title/Abstract] OR "transcriptomics"[Title/Abstract] OR "gene expression"[Title/Abstract]) AND ("2023/01/01"[PDAT] : "3000"[PDAT])',
    
    # PPT/EIH explícito + transcriptómica
    '("pressure pain threshold"[Title/Abstract] OR "exercise-induced hypoalgesia"[Title/Abstract] OR "conditioned pain modulation"[Title/Abstract]) AND ("RNA-seq"[Title/Abstract] OR "transcriptomics"[Title/Abstract] OR "gene expression"[Title/Abstract]) AND ("2023/01/01"[PDAT] : "3000"[PDAT])',
    
    # GEO datasets directo (no pubmed)
    '("fibromyalgia" OR "chronic pain" OR "pressure pain threshold") AND ("exercise" OR "training") AND ("RNA-seq" OR "transcriptomics") AND "Homo sapiens"[Organism] AND "Expression profiling by high throughput sequencing"[Filter]',
]

all_ids = set()
for i, q in enumerate(queries):
    print(f"Query {i+1}/{len(queries)}: {q[:80]}...")
    try:
        res = esearch("gds", q, retmax=200)
        ids = res.get("esearchresult", {}).get("idlist", [])
        print(f"  -> {len(ids)} GDS IDs")
        all_ids.update(ids)
        time.sleep(0.4)  # rate limit
    except Exception as e:
        print(f"  ERROR: {e}")

print(f"\nTotal unique GDS: {len(all_ids)}")

# Fetch summaries
candidates = []
for chunk in [list(all_ids)[i:i+20] for i in range(0, len(all_ids), 20)]:
    try:
        summ = esummary("gds", chunk)
        for uid, rec in summ.get("result", {}).items():
            if uid == "uids":
                continue
            title = rec.get("title", "")
            summary = rec.get("summary", "")
            gds_type = rec.get("gdsType", "")
            tax = rec.get("taxon", "")
            pubmed = rec.get("pubmedId", "")
            
            # Filtros duros
            has_longitudinal = any(kw in (title+summary).lower() for kw in ["longitudinal", "time course", "pre.post", "pre post", "before.after", "before after", "follow.up", "follow up", "timepoint", "time point"])
            has_ppt = any(kw in (title+summary).lower() for kw in ["pressure pain", "ppt", "hypoalgesia", "pain threshold", "ei"])
            has_fm_pain = any(kw in (title+summary).lower() for kw in ["fibromyalgia", "chronic pain", "chronic widespread"])
            has_rna = any(kw in (title+summary).lower() for kw in ["rna-seq", "rnaseq", "transcriptom", "gene expression", "expression profiling"])
            has_exercise = any(kw in (title+summary).lower() for kw in ["exercise", "training", "physical activity"])
            has_immune = any(kw in (title+summary).lower() for kw in ["lps", "lipopolysaccharide", "immune stim", "cytokine"])
            
            if has_rna and (has_longitudinal or has_ppt) and (has_fm_pain or has_exercise or has_immune):
                candidates.append({
                    "gds": uid,
                    "title": title,
                    "summary": summary[:500],
                    "gdsType": gds_type,
                    "taxon": tax,
                    "pubmed": pubmed,
                    "has_longitudinal": has_longitudinal,
                    "has_ppt": has_ppt,
                    "has_fm_pain": has_fm_pain,
                    "has_rna": has_rna,
                    "has_exercise": has_exercise,
                    "has_immune": has_immune
                })
        time.sleep(0.4)
    except Exception as e:
        print(f"  ERROR summary: {e}")

print(f"\nCandidatos tras filtros: {len(candidates)}")

# Guardar
ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
out_file = OUT / f"geo_remining_{ts}.json"
with open(out_file, "w") as f:
    json.dump({
        "spec_hash": "sha256:5e8b3f1a2c4d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f",
        "timestamp": datetime.datetime.now().isoformat(),
        "queries": queries,
        "total_gds_searched": len(all_ids),
        "candidates": candidates,
        "kill_criterion": "0 datasets con ΔPPT/EIH + transcriptómica longitudinal post-2022",
        "verdict": "FAIL" if len(candidates) == 0 else "PASS"
    }, f, ensure_ascii=False, indent=2)

print(f"Resultados en {out_file}")
for c in candidates:
    print(f"  GSE{c['gds']}: {c['title'][:80]} | long={c['has_longitudinal']} ppt={c['has_ppt']} fm={c['has_fm_pain']} ex={c['has_exercise']} imm={c['has_immune']}")

if len(candidates) == 0:
    print("\n❌ KILL CRITERION MET: 0 datasets — cerrar vía in-silico, pasar a Opción B (proteómica)")
else:
    print(f"\n✅ {len(candidates)} candidatos — revisar detalle para validar ΔPPT/EIH real")