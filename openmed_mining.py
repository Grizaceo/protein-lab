#!/usr/bin/env python3
"""
openmed_mining.py — Mining de literatura biomédica con OpenMed (NER local).

Extrae PROTEÍNAS, COMPUESTOS QUÍMICOS, FÁRMACOS y ENFERMEDADES de abstracts
o texto de papers, usando modelos NER de OpenMed (maziyarpanahi/openmed).
Todo corre local (CPU o CUDA en RTX 4060), sin enviar datos a la nube.

Modelos por defecto (nombres HF verificados 2026-08-05):
  - ProteinDetect:   OpenMed/OpenMed-NER-ProteinDetect-PubMed-109M
  - ChemicalDetect:  OpenMed/OpenMed-NER-ChemicalDetect-PubMed-335M
  - PharmaDetect:    OpenMed/OpenMed-NER-PharmaDetect-SuperMedical-125M
  - DiseaseDetect:   OpenMed/OpenMed-NER-DiseaseDetect-TinyMed-135M

Uso:
  # Texto directo
  python openmed_mining.py --text "Patients treated with pregabalin for fibromyalgia..."
  # Archivo markdown/txt (ej: resumen de paper de la vault)
  python openmed_mining.py --file literatura/abstract_fm.md
  # Batch sobre varios archivos
  python openmed_mining.py --dir literatura/ --glob "*.md" --json salida.json
  # Modelo específico
  python openmed_mining.py --text "TACR1 and OPRM1..." --model protein

Requiere: pip install "openmed[hf]"
"""
import argparse
import json
import os
import sys
import time

MODELS = {
    "protein": "OpenMed/OpenMed-NER-ProteinDetect-PubMed-109M",
    "chemical": "OpenMed/OpenMed-NER-ChemicalDetect-PubMed-335M",
    "pharma": "OpenMed/OpenMed-NER-PharmaDetect-SuperMedical-125M",
    "disease": "OpenMed/OpenMed-NER-DiseaseDetect-TinyMed-135M",
}
# Etiquetas canónicas de OpenMed que nos importan
RELEVANT_LABELS = {
    "protein", "PROTEIN", "PROTEIN_CHANGE", "GENE", "GENE_SYMBOL",
    "chem", "CHEM", "CHEMICAL", "drug", "DRUG", "MEDICATION",
    "disease", "DISEASE", "CONDITION",
}


def analyze(text: str, model_name: str, min_conf: float = 0.5):
    from openmed import analyze_text
    t0 = time.time()
    result = analyze_text(text, model_name=model_name)
    elapsed = time.time() - t0
    entities = []
    for e in getattr(result, "entities", []):
        conf = float(getattr(e, "confidence", 0.0) or 0.0)
        if conf < min_conf:
            continue
        entities.append({
            "label": str(getattr(e, "label", "?")),
            "text": str(getattr(e, "text", "")),
            "confidence": round(conf, 3),
        })
    return {"model": model_name, "seconds": round(elapsed, 1), "entities": entities}


def run_pipeline(text: str, models: list[str], min_conf: float):
    out = {}
    for key in models:
        model = MODELS.get(key)
        if not model:
            print(f"  [skip] modelo desconocido: {key}", file=sys.stderr)
            continue
        print(f"  → {key} ({model}) ...", file=sys.stderr)
        try:
            out[key] = analyze(text, model, min_conf)
            for e in out[key]["entities"]:
                print(f"      {e['label']:<10} {e['text']:<40} conf={e['confidence']:.2f}")
        except Exception as ex:
            out[key] = {"model": model, "error": str(ex)}
            print(f"      ERROR: {ex}", file=sys.stderr)
    return out


def read_file_text(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def main():
    ap = argparse.ArgumentParser(description="Mining NER biomédico con OpenMed")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--text", help="Texto directo a analizar")
    src.add_argument("--file", help="Archivo .md/.txt a analizar")
    src.add_argument("--dir", help="Directorio para batch (con --glob)")
    ap.add_argument("--glob", default="*.md", help="Glob para batch (default *.md)")
    ap.add_argument("--models", default="protein,chemical,disease,pharma",
                    help="Modelos separados por coma (default todos)")
    ap.add_argument("--min-conf", type=float, default=0.5)
    ap.add_argument("--json", default=None, help="Ruta del JSON de salida")
    args = ap.parse_args()

    models = [m.strip() for m in args.models.split(",") if m.strip()]

    if args.text:
        docs = {"stdin": args.text}
    elif args.file:
        docs = {args.file: read_file_text(args.file)}
    else:
        import glob
        docs = {}
        for p in sorted(glob.glob(os.path.join(args.dir, args.glob))):
            docs[p] = read_file_text(p)
        if not docs:
            print(f"No hay archivos {args.glob} en {args.dir}", file=sys.stderr)
            sys.exit(1)

    results = {}
    for name, text in docs.items():
        print(f"\n=== {name} ({len(text)} chars) ===", file=sys.stderr)
        results[name] = run_pipeline(text[:20000], models, args.min_conf)

    # Resumen consolidado
    print("\n=== RESUMEN ENTIDADES (conf >= {:.2f}) ===".format(args.min_conf))
    for name, pipe in results.items():
        total = sum(len(r.get("entities", [])) for r in pipe.values())
        print(f"{name}: {total} entidades")

    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\nJSON guardado: {args.json}")


if __name__ == "__main__":
    main()
