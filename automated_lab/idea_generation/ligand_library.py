#!/usr/bin/env python3
"""Curated small-molecule expansion for automated_lab.

The library uses names only as search seeds, then resolves executable SMILES via
PubChem PUG REST and caches the exact result locally. No PubChem hit = no
experiment. This is intentionally conservative: better fewer real molecules than
LLM-invented chemistry soup.
"""

from __future__ import annotations

import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

LAB_DIR = Path(__file__).resolve().parent.parent.parent
CACHE_FILE = LAB_DIR / "automated_lab" / "data" / "pubchem_smiles_cache.json"

# Fibromyalgia-relevant/control-ish seed set: analgesics, antidepressants,
# anticonvulsants, anti-inflammatory drugs, mast-cell/allergy drugs, TRP/channel
# ligands, GPCR ligands, immunomodulators, and negative-ish broad controls.
DEFAULT_SEED_NAMES = [
    # Core FM / pain / opioidergic controls
    "naltrexone", "naloxone", "nalmefene", "morphine", "buprenorphine", "tramadol",
    "tapentadol", "methadone", "fentanyl", "oxycodone", "hydrocodone", "codeine",
    "dextromethorphan", "ketamine", "memantine", "amantadine", "lidocaine",
    "mexiletine", "carbamazepine", "oxcarbazepine", "lamotrigine", "gabapentin",
    "pregabalin", "topiramate", "valproic acid", "levetiracetam", "lacosamide",
    # SNRIs/SSRIs/TCAs and neuro-modulators
    "duloxetine", "milnacipran", "venlafaxine", "desvenlafaxine", "amitriptyline",
    "nortriptyline", "imipramine", "desipramine", "cyclobenzaprine", "mirtazapine",
    "fluoxetine", "sertraline", "paroxetine", "citalopram", "escitalopram",
    "fluvoxamine", "bupropion", "trazodone", "buspirone", "tizanidine", "baclofen",
    "clonidine", "guanfacine", "propranolol", "prazosin", "modafinil", "armodafinil",
    # NSAIDs / anti-inflammatory controls
    "ibuprofen", "naproxen", "diclofenac", "ketoprofen", "indomethacin", "celecoxib",
    "meloxicam", "piroxicam", "etoricoxib", "aspirin", "acetaminophen", "metamizole",
    "prednisone", "prednisolone", "dexamethasone", "hydrocortisone", "colchicine",
    "sulfasalazine", "methotrexate", "leflunomide", "hydroxychloroquine",
    # Mast cell / allergy / histamine axis
    "ketotifen", "cromolyn", "nedocromil", "rupatadine", "loratadine", "desloratadine",
    "cetirizine", "levocetirizine", "fexofenadine", "diphenhydramine", "doxepin",
    "famotidine", "cimetidine", "ranitidine", "montelukast", "zafirlukast",
    "omalizumab", "quercetin", "luteolin", "resveratrol", "curcumin", "apigenin",
    "naringenin", "baicalein", "epigallocatechin gallate",
    # Ion channels, TRP, sodium channel, neuropathic pain adjacent
    "capsaicin", "capsazepine", "menthol", "camphor", "cinnamaldehyde", "allyl isothiocyanate",
    "suzetrigine", "riluzole", "ranolazine", "flecainide", "propafenone", "quinidine",
    "verapamil", "diltiazem", "nifedipine", "amlodipine", "nimodipine", "ziconotide",
    # TLR4 / neuroinflammation / glia adjacent
    "resatorvid", "minocycline", "doxycycline", "pioglitazone", "rosiglitazone",
    "metformin", "dimethyl fumarate", "monomethyl fumarate", "fingolimod", "laquinimod",
    "ibudilast", "pentoxifylline", "apremilast", "roflumilast", "n-acetylcysteine",
    "melatonin", "palmitoylethanolamide", "low-dose naltrexone",
    # Cannabinoid / endocannabinoid / PPAR controls
    "cannabidiol", "tetrahydrocannabinol", "dronabinol", "nabilone", "rimonabant",
    "oleoylethanolamide", "anandamide", "fenofibrate", "bezafibrate", "gemfibrozil",
    # Cytokine/small-molecule immunomodulatory controls
    "tofacitinib", "baricitinib", "ruxolitinib", "upadacitinib", "filgotinib",
    "thalidomide", "lenalidomide", "pomalidomide", "azathioprine", "mycophenolic acid",
    "cyclosporine", "tacrolimus", "sirolimus", "everolimus", "rapamycin",
    # Extra pharmacological diversity / negative controls
    "caffeine", "theophylline", "nicotine", "varenicline", "donepezil", "rivastigmine",
    "galantamine", "omeprazole", "pantoprazole", "atorvastatin", "simvastatin",
    "rosuvastatin", "losartan", "telmisartan", "lisinopril", "enalapril", "sildenafil",
    "tadalafil", "allopurinol", "febuxostat", "probenecid", "clonazepam", "diazepam",
    "alprazolam", "zolpidem", "eszopiclone", "ramelteon",
]


def _safe_key(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", name.strip().lower()).strip("_")


def _load_cache() -> dict[str, dict]:
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text())
        except Exception:
            return {}
    return {}


def _save_cache(cache: dict[str, dict]) -> None:
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(json.dumps(cache, indent=2, ensure_ascii=False))


def fetch_pubchem_smiles(name: str, timeout: int = 20) -> dict | None:
    encoded = urllib.parse.quote(name)
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{encoded}/property/CanonicalSMILES,IsomericSMILES/JSON"
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        props = data.get("PropertyTable", {}).get("Properties", [])
        if not props:
            return None
        row = props[0]
        smiles = row.get("IsomericSMILES") or row.get("CanonicalSMILES") or row.get("SMILES") or row.get("ConnectivitySMILES")
        if not smiles:
            return None
        return {"name": name, "cid": row.get("CID"), "smiles": smiles, "source": "PubChem PUG REST"}
    except Exception:
        return None


def resolve_ligands(seed_names: list[str] | None = None, *, limit: int | None = None,
                    sleep_s: float = 0.12) -> dict[str, str]:
    """Resolve seed names to canonical executable SMILES.

    Returns `{safe_name: smiles}`. Failed PubChem lookups are cached as misses so
    reruns do not hammer NCBI.
    """
    names = seed_names or DEFAULT_SEED_NAMES
    if limit:
        names = names[:limit]
    cache = _load_cache()
    changed = False
    out: dict[str, str] = {}
    for name in names:
        key = _safe_key(name)
        cached = cache.get(key)
        if cached and cached.get("smiles"):
            out[key] = cached["smiles"]
            continue
        if cached and cached.get("miss"):
            continue
        hit = fetch_pubchem_smiles(name)
        changed = True
        if hit:
            cache[key] = hit
            out[key] = hit["smiles"]
        else:
            cache[key] = {"name": name, "miss": True, "source": "PubChem PUG REST"}
        time.sleep(sleep_s)
    if changed:
        _save_cache(cache)
    return out


if __name__ == "__main__":
    ligands = resolve_ligands(limit=None)
    print(json.dumps({"resolved": len(ligands), "cache": str(CACHE_FILE)}, indent=2))
