#!/usr/bin/env python3
"""
fetch_targets.py — Monitorización y descarga de targets CASP17

Consulta la lista oficial de objetivos activos en predictioncenter.org
y descarga secuencias FASTA individuales o en lote.
"""
import os
import sys
import re
import urllib.request
import urllib.error
import argparse
from datetime import datetime

# ---------------------------------------------------------------------------
# Configuración de URLs para CASP17 (2026)
# ---------------------------------------------------------------------------
BASE_URL = "https://predictioncenter.org/casp17"
TARGET_LIST_URL = f"{BASE_URL}/targetlist.cgi"
TARGET_SEQ_URL_TEMPLATE = f"{BASE_URL}/target.cgi?target={{target_id}}&view=sequence"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/126.0.0.0 Safari/537.36"
    )
}

# Prefijos de target y sus categorías
TARGET_TYPES = {
    "T": "Proteina (monomer/homomer)",
    "H": "Heteromero",
    "R": "RNA",
    "M": "Multimer",
    "E": "Ensamblaje",
    "W": "Whole-cell",
}

# ---------------------------------------------------------------------------
# Utilidades HTTP
# ---------------------------------------------------------------------------

def get_url_content(url):
    """Descarga el contenido de una URL con manejo de errores."""
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return response.read().decode("utf-8", errors="ignore")
    except urllib.error.HTTPError as e:
        print(f"Error HTTP {e.code} al conectar a {url}: {e.reason}", file=sys.stderr)
        return None
    except urllib.error.URLError as e:
        print(f"Error de conexión a {url}: {e.reason}", file=sys.stderr)
        return None
    except TimeoutError:
        print(f"Timeout al conectar a {url}", file=sys.stderr)
        return None


def classify_target(target_id):
    """Clasifica un target según su prefijo."""
    prefix = target_id[0] if target_id else "?"
    return TARGET_TYPES.get(prefix, "Desconocido")


# ---------------------------------------------------------------------------
# Funciones principales
# ---------------------------------------------------------------------------

def fetch_targets_with_info():
    """Obtiene la lista de targets con metadatos parseados del HTML."""
    print(f"Consultando objetivos en {TARGET_LIST_URL} ...")

    html = get_url_content(TARGET_LIST_URL)
    if not html:
        return []

    # Extraer IDs de target
    target_matches = re.findall(
        r'target\.cgi\?id=[^>]+>([A-Z0-9]+)</a>', html
    )

    # Dedup preservando orden
    seen = set()
    targets = []
    for t in target_matches:
        if t not in seen:
            seen.add(t)
            targets.append(t)

    return targets


def fetch_active_targets(filter_type=None):
    """Obtiene la lista de targets, opcionalmente filtrada por tipo."""
    targets = fetch_targets_with_info()

    if filter_type:
        prefix = filter_type.upper()[0]
        targets = [t for t in targets if t[0] == prefix]

    return targets


def download_target_sequence(target_id, output_dir):
    """Descarga la secuencia FASTA de un target específico."""
    url = TARGET_SEQ_URL_TEMPLATE.format(target_id=target_id)
    print(f"Descargando secuencia para {target_id} ...")

    content = get_url_content(url)
    if not content:
        print(f"  ERROR: No se pudo descargar la secuencia de {target_id}.", file=sys.stderr)
        return False

    content = content.strip()

    # Limpiar HTML residual si lo hay
    if "<html" in content.lower() or "<body" in content.lower():
        pre_match = re.search(r'<pre[^>]*>(.*?)</pre>', content, re.DOTALL | re.IGNORECASE)
        if pre_match:
            content = pre_match.group(1).strip()
        else:
            content = re.sub('<[^<]+?>', '', content).strip()

    # Asegurar formato FASTA
    if not content.startswith(">"):
        content = f">{target_id}\n{content}"

    # Normalizar line endings a LF
    content = content.replace("\r\n", "\n").replace("\r", "\n")

    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, f"{target_id}.fasta")

    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
        if not content.endswith("\n"):
            f.write("\n")

    # Validación rápida
    lines = content.split("\n")
    seq = "".join(l.strip() for l in lines[1:] if l.strip())
    print(f"  Guardado: {out_path}  ({len(seq)} residuos)")
    return True


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Monitorización y descarga de targets CASP17 (2026)"
    )
    parser.add_argument(
        "--list", action="store_true",
        help="Listar los objetivos disponibles en el portal"
    )
    parser.add_argument(
        "--download", type=str, metavar="ID",
        help="ID del objetivo a descargar (ej. T1313)"
    )
    parser.add_argument(
        "--download-all", action="store_true",
        help="Descargar todas las secuencias FASTA de los targets listados"
    )
    parser.add_argument(
        "--type", type=str, default=None,
        choices=["T", "H", "R", "M", "E", "W"],
        help="Filtrar por tipo de target: T=Proteina, H=Heteromero, R=RNA, M=Multimer, E=Ensamblaje, W=Whole-cell"
    )
    parser.add_argument(
        "--outdir", type=str, default="targets",
        help="Carpeta de salida para las secuencias (default: targets/)"
    )

    args = parser.parse_args()

    # Resolver ruta de salida relativa a la carpeta casp17/
    script_dir = os.path.dirname(os.path.abspath(__file__))
    casp17_dir = os.path.dirname(script_dir)
    outdir_abs = os.path.join(casp17_dir, args.outdir)

    if args.list:
        targets = fetch_active_targets(filter_type=args.type)
        if not targets:
            print("No se encontraron objetivos activos o el servidor no respondió.")
            return

        # Agrupar por tipo
        by_type = {}
        for t in targets:
            tipo = classify_target(t)
            by_type.setdefault(tipo, []).append(t)

        print(f"\n{'='*55}")
        print(f" Objetivos CASP17  —  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"{'='*55}")

        for tipo, ids in by_type.items():
            print(f"\n  {tipo} ({len(ids)}):")
            # Imprimir en filas de 8
            for i in range(0, len(ids), 8):
                row = ids[i:i+8]
                print(f"    {', '.join(row)}")

        print(f"\n{'='*55}")
        print(f" Total: {len(targets)} objetivos")
        if args.type:
            print(f" (filtrado por tipo: {args.type})")
        print(f"{'='*55}\n")

    elif args.download:
        target_id = args.download.upper()
        download_target_sequence(target_id, outdir_abs)

    elif args.download_all:
        targets = fetch_active_targets(filter_type=args.type)
        if not targets:
            print("No hay targets para descargar.")
            return
        print(f"Descargando {len(targets)} secuencias ...\n")
        ok = 0
        fail = 0
        for t in targets:
            if download_target_sequence(t, outdir_abs):
                ok += 1
            else:
                fail += 1
        print(f"\nDescarga completada: {ok} exitosas, {fail} fallidas.")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
