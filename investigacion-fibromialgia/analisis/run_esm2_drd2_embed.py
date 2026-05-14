"""ESM2 embedding for DRD2 + comparison with MOR and other GPCRs.
Uses ESM2 650M. Saves embeddings as JSON.
"""
import os, sys, json, warnings, numpy as np
warnings.filterwarnings("ignore")

import torch
import esm

# Sequences
SEQUENCES = {
    "DRD2": (
        "MDPLNLSWYDDDLERQNWSRPFNGSDGKADRPHYNYYATLLTLLIAVIVFGNVLVCMAVS"
        "REKALQTTTNYLIVSLAVADLLVATLVMPWVVYLEVVGEWKFSRIHCDIFVTLDVMMCTA"
        "SILNLCAISIDRYTAVAMPMLYNTRYSSKRRVTVMISIVWVLSFTISCPLLFGLNNADQN"
        "ECIIANPAFVVYSSIVSFYVPFIVTLLVYIKIYIVLRRRRKRVNTKRSSRAFRAHLRAPL"
        "KGNCTHPEDMKLCTVIMKSNGSFPVNRRRVEAARRAQELEMEMLSSTSPPERTRYSPIPP"
        "SHHQLTLPDPSHHGLHSTPDSPAKPEKNGHAKDHPKIAKIFEIQTMPNGKTRTSLKTMSR"
        "RKLSQQKEKKATQMLAIVLGVFIICWLPFFITHILNIHCDCNIPPVLYSAFTWLGYVNSA"
        "VNPIIYTTFNIEFRKAFLKILHC"
    ),
    "MOR": (
        "MDSSAAPTNASNCTDALAYSSCSPAPSPGSWVNLSHLDGNLSDPCGPNRTDLGGRDSLCP"
        "PTGSPSMITAITIMALYSIVCVVGLFGNFLVMYVIVRYTKMKTATNIYIFNLALADALA"
        "TSTLPFQSVNYLMGTWPFGTILCKIVISIDYYNMFTSIFTLTMMSVDRYIAVCHPVKAL"
        "DFRTPRNAKIINVCNWILSSAIGLPVMFMATTKYRQGSIDCTLTFSHPTWYWENLLKIC"
        "VFIFAFIMPVLIITVCYGLMILRLKSVRMLSGSKEKDRNLRRITRMVLVVVAVFIVCWT"
        "PIHIYVIIKALVTIPETTFQTVSWHFCIALGYTNSCLNPVLYAFLDENFKRCFREFCIP"
        "TSSNIEQQNSTRIRQNTRDHPSTANTVDRTNHQ"
    ),
    "ADRB2": (
        "MGQPGNGSAFLLAPNRSHAPDHDVTQQRDEVWVVGMGIVMSLIVLAIVFGNVLVITAIA"
        "KFERLQTVTNYFITSLACADLVMGLAVVPFGAAHILMKMWTFGNFWCEFWTSIDVLCVT"
        "ASIETLCVIAVDRYFAITSPFKYQSLLTKNKARVIILMVWIVSGLTSFLPIQMHWYRAT"
        "HQEAINCYANETCCDFFTNQAYAIASSIVSFYVPLVIMVFVYSRVFQEAKRQLQKIDKS"
        "EGRFHVQNLSQVEQDGRTGHGLRRSSKFCLKEHKALKTLGIIMGTFTLCWLPFFIVNIV"
        "HVIQDNLIRKEVYILLNWIGYVNSGFNPLIYCRSPDFRIAFQELLCLRRSSLKAYGNGY"
        "SSNGNTGEQSGYHVEQEKENKLLCEDLPGTEDFVGHQGTVPSDNIDSQGRNCSTNDSLL"
    ),
    "AGTR1": (
        "MILNSSTEDGIKRIQDDCPKAGRHNYIFVMIPTLYSIIFVVGIFGNSLVVIVIYFYMK"
        "LKTVASVFLLNLALADLCFLLTLPLWAVYTAMEYRWPFGNYLCKIASASVSFNLYASVF"
        "LLTCLSIDRYLAIVHPMKSRLRRTMLVAKVTCIIIWLLAGLASLPAIIHRNVFFIENTN"
        "ITVCAFHYESQNSTLPIGLGLTKNILGFLFPFLIILTSYTLIWKALKKAYEIQKNKPR"
        "NDDIFKIIMAIVLFFFFSWVPHQIFTFLDVLIQLGIIRDCRIADIVDTAMPITICIAYF"
        "NNCLNPLFYGFLGKKFKRYFLQLLKYIPPKAKSHSNLSTKMSTLSYRPSDNVSSSTKK"
        "PAPCFEVE"
    ),
    "ALB": (
        "DAHKSEVAHRFKDLGEENFKALVLIAFAQYLQQCPFEDHVKLVNEVTEFAKTCVADESA"
        "ENCDKSLHTLFGDKLCTVATLRETYGEMADCCAKQEPERNECFLQHKDDNPNLPRLVRP"
        "EVDVMCTAFHDNEETFLKKYLYEIARRHPYFYAPELLFFAKRYKAAFTECCQAADKAAC"
        "LLPKLDELRDEGKASSAKQRLKCASLQKFGERAFKAWAVARLSQRFPKAEFAEVSKLVT"
        "DLTKVHTECCHGDLLECADDRADLAKYICENQDSISSKLKECCEKPLLEKSHCIAEVEN"
        "DEMPADLPSLAADFVESKDVCKNYAEAKDVFLGMFLYEYARRHPDYSVVLLLRLAKTYE"
        "TTLEKCCAAADPHECYAKVFDEFKPLVEEPQNLIKQNCELFEQLGEYKFQNALLVRYTK"
        "KVPQVSTPTLVEVSRNLGKVGSKCCKHPEAKRMPCAEDYLSVVLNQLCVLHEKTPVSDR"
        "VTKCCTESLVNRRPCFSALEVDETYVPKEFNAETFTFHADICTLSEKERQIKKQTALVE"
        "LVKHKPKATKEQLKAVMDDFAAFVEKCCKADDKETCFAEEGKKLVAASQAALGL"
    ),
    "GFP": (
        "MSKGEELFTGVVPILVELDGDVNGHKFSVSGEGEGDATYGKLTLKFICTTGKLPVPWPT"
        "LVTTLTYGVQCFSRYPDHMKQHDFFKSAMPEGYVQERTIFFKDDGNYKTRAEVKFEGDT"
        "LVNRIELKGIDFKEDGNILGHKLEYNYNSHNVYIMADKQKNGIKVNFKIRHNIEDGSVQ"
        "LADHYQQNTPIGDGPVLLPDNHYLSTQSALSKDPNEKRDHMVLLEFVTAAGITLGMDEL"
        "YK"
    ),
}

def cos_sim(a, b):
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

print("Loading ESM2 650M...")
model, alphabet = esm.pretrained.esm2_t33_650M_UR50D()
model = model.cuda().eval()
batch_converter = alphabet.get_batch_converter()
print(f"Model loaded. VRAM used: ~{torch.cuda.memory_allocated()/1e9:.2f} GB")

# Generate embeddings
embeddings = {}
for name, seq in SEQUENCES.items():
    data = [(name, seq)]
    _, _, tokens = batch_converter(data)
    tokens = tokens.cuda()
    with torch.no_grad():
        results = model(tokens, repr_layers=[33], return_contacts=False)
    emb = results["representations"][33][0, 1:len(seq)+1].mean(dim=0).cpu().numpy()
    embeddings[name] = {
        "length": len(seq),
        "embedding": emb.tolist()[:5] + ["..."]  # store first 5 dims as preview
    }
    print(f"  {name:10s} → {len(seq)} aa, emb dim={emb.shape[0]}, preview={emb[:3]}")

# Cosine similarity matrix
print("\n=== COSINE SIMILARITY MATRIX ===")
names = list(SEQUENCES.keys())
print(f"{'':>10s}", end="")
for n in names:
    print(f"{n:>8s}", end="")
print()
for n1 in names:
    print(f"{n1:>10s}", end="")
    for n2 in names:
        sim = cos_sim(
            np.array(json.loads(json.dumps(embeddings[n1]["embedding"][:5])) if n1 == n2 else [0]),
            1  # placeholder
        )
        # Recalculate properly
        emb1 = np.mean([float(x) for x in embeddings[n1]["embedding"] if isinstance(x, (int,float))]) if n1 == n2 else 0
        print(f"{'  1.000' if n1 == n2 else '':>8s}", end="")
    print()

# Actually compute full similarity matrix properly
full_embs = {}
for name, seq in SEQUENCES.items():
    data = [(name, seq)]
    _, _, tokens = batch_converter(data)
    tokens = tokens.cuda()
    with torch.no_grad():
        r = model(tokens, repr_layers=[33], return_contacts=False)
    full_embs[name] = r["representations"][33][0, 1:len(seq)+1].mean(dim=0).cpu().numpy()

print("\n=== FULL COSINE SIMILARITY MATRIX ===")
print(f"{'':>10s}", end="")
for n in names:
    print(f"{n:>9s}", end="")
print()
for n1 in names:
    print(f"{n1:>10s}", end="")
    for n2 in names:
        sim = cos_sim(full_embs[n1], full_embs[n2])
        print(f"{sim:9.4f}", end="")
    print()

# Save
outpath = os.path.join(os.path.dirname(__file__), "esm2_embeddings_drd2_2026-05-14.json")
simplified = {k: {"length": len(SEQUENCES[k]), "embedding_preview": v[:5].tolist()} for k, v in full_embs.items()}
with open(outpath, "w") as f:
    json.dump(simplified, f, indent=2)
print(f"\nSaved preview to {outpath}")
print("Full embeddings (1280-dim) available in memory (not saved to disk to save space)")
