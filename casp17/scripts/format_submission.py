#!/usr/bin/env python3
"""
format_submission.py — Formateador de modelos PDB al estándar CASP TS

Convierte archivos PDB (salida de ColabFold/AlphaFold/ESM) al formato
oficial CASP TS (Tertiary Structure) para envío al Prediction Center.

Formato de referencia:
  https://predictioncenter.org/casp17/index.cgi  (Format Specification)

Estructura del archivo TS:
  PFRMAT TS
  TARGET <id>
  AUTHOR <registration_code>
  METHOD <description>
  MODEL  <n>
  PARENT <template(s) | N/A>
  ATOM   ...
  TER
  END
"""
import os
import sys
import argparse


# ---------------------------------------------------------------------------
# CASP TS formatting
# ---------------------------------------------------------------------------

# Placeholder para el código de registro — el usuario debe reemplazarlo
# con su código real tras registrarse en predictioncenter.org/casp17
DEFAULT_AUTHOR = "XXXX-XXXX-XXXX"


def pad_pdb_line(line):
    """Asegura que una línea PDB tenga exactamente 80 caracteres (estándar PDB)."""
    line = line.rstrip("\r\n")
    if len(line) > 80:
        line = line[:80]
    return line.ljust(80)


def read_pdb_coordinates(pdb_path):
    """Lee las líneas de coordenadas de un archivo PDB.

    Retorna solo ATOM y TER (excluyendo HETATM para CASP TS de proteínas).
    """
    coordinate_lines = []

    with open(pdb_path, "r", encoding="utf-8") as f:
        for line in f:
            record = line[:6].strip()
            if record == "ATOM" or record == "TER":
                coordinate_lines.append(line)

    return coordinate_lines


def format_pdb_to_casp_ts(
    pdb_path, target_id, model_index, method, parent, author, out_path
):
    """Convierte un archivo PDB al formato CASP TS."""

    if not os.path.exists(pdb_path):
        print(f"Error: El archivo PDB no existe: {pdb_path}", file=sys.stderr)
        return False

    # Validar el código de autor
    if author == DEFAULT_AUTHOR:
        print(
            "ADVERTENCIA: Estás usando el código de autor por defecto "
            f"({DEFAULT_AUTHOR}).\n"
            "  Debes reemplazarlo con tu código de registro real de CASP17.\n"
            "  Regístrate en: https://predictioncenter.org/casp17/index.cgi\n",
            file=sys.stderr,
        )

    print(f"Leyendo coordenadas desde {pdb_path} ...")
    coordinate_lines = read_pdb_coordinates(pdb_path)

    if not coordinate_lines:
        print(
            "Error: No se encontraron líneas ATOM/TER en el archivo PDB.",
            file=sys.stderr,
        )
        return False

    atom_count = sum(1 for l in coordinate_lines if l[:4] == "ATOM")
    ter_count = sum(1 for l in coordinate_lines if l[:3] == "TER")
    print(f"  {atom_count} líneas ATOM, {ter_count} TER encontrados.")

    # Crear carpeta de salida
    out_dir = os.path.dirname(out_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    # Escribir archivo TS con line endings Unix (LF)
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        # --- Cabeceras globales (una sola vez) ---
        f.write("PFRMAT TS\n")
        f.write(f"TARGET {target_id.upper()}\n")
        f.write(f"AUTHOR {author}\n")

        # METHOD puede ocupar varias líneas si es largo
        method_lines = method.split("\n")
        for ml in method_lines:
            f.write(f"METHOD {ml.strip()}\n")

        # --- Bloque MODEL ---
        f.write(f"MODEL  {model_index}\n")
        f.write(f"PARENT {parent}\n")

        # Coordenadas con padding a 80 caracteres
        for line in coordinate_lines:
            f.write(pad_pdb_line(line) + "\n")

        # Asegurar terminación TER + END
        last_record = coordinate_lines[-1][:6].strip() if coordinate_lines else ""
        if last_record != "TER":
            f.write(pad_pdb_line("TER") + "\n")
        f.write("END\n")

    print(f"  Archivo TS guardado: {out_path}")
    return True


def format_multi_model(pdb_paths, target_id, method, parent, author, out_path):
    """Combina hasta 5 modelos PDB en un solo archivo TS multi-modelo."""

    if len(pdb_paths) > 5:
        print("Error: CASP permite máximo 5 modelos por target.", file=sys.stderr)
        return False

    out_dir = os.path.dirname(out_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        # Cabeceras globales
        f.write("PFRMAT TS\n")
        f.write(f"TARGET {target_id.upper()}\n")
        f.write(f"AUTHOR {author}\n")
        for ml in method.split("\n"):
            f.write(f"METHOD {ml.strip()}\n")

        for idx, pdb_path in enumerate(pdb_paths, 1):
            if not os.path.exists(pdb_path):
                print(f"  WARN: Modelo {idx} no existe: {pdb_path}", file=sys.stderr)
                continue

            coords = read_pdb_coordinates(pdb_path)
            if not coords:
                print(f"  WARN: Modelo {idx} sin coordenadas: {pdb_path}", file=sys.stderr)
                continue

            f.write(f"MODEL  {idx}\n")
            f.write(f"PARENT {parent}\n")

            for line in coords:
                f.write(pad_pdb_line(line) + "\n")

            last_record = coords[-1][:6].strip() if coords else ""
            if last_record != "TER":
                f.write(pad_pdb_line("TER") + "\n")
            f.write("END\n")

            print(f"  Modelo {idx}: {os.path.basename(pdb_path)} ({len(coords)} líneas)")

    print(f"\n  Archivo multi-modelo TS guardado: {out_path}")
    return True


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Formateador de modelos PDB al formato oficial CASP TS",
        epilog=(
            "Ejemplo de uso:\n"
            "  python format_submission.py --pdb pred.pdb --target T1313 --model 1\n"
            "  python format_submission.py --multi pred1.pdb pred2.pdb --target T1313"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--pdb", type=str, help="Ruta al archivo PDB de entrada (modelo único)")
    group.add_argument("--multi", nargs="+", metavar="PDB", help="Rutas a varios PDB (multi-modelo, máx 5)")

    parser.add_argument("--target", type=str, required=True, help="ID del target CASP (ej. T1313)")
    parser.add_argument("--model", type=int, default=1, choices=range(1, 6),
                        help="Índice del modelo 1-5 (default: 1, solo para --pdb)")
    parser.add_argument("--method", type=str,
                        default="ColabFold local prediction on RTX 4060",
                        help="Descripción del método de modelado")
    parser.add_argument("--parent", type=str, default="N/A",
                        help="Templates parentales (PDB IDs separados por espacio, o N/A)")
    parser.add_argument("--author", type=str, default=DEFAULT_AUTHOR,
                        help="Código de registro CASP17 (XXXX-XXXX-XXXX)")
    parser.add_argument("--out", type=str,
                        help="Ruta del archivo de salida (opcional, default: submissions/<TARGET>_model<N>.ts)")

    args = parser.parse_args()

    # Resolver ruta de salida
    script_dir = os.path.dirname(os.path.abspath(__file__))
    casp17_dir = os.path.dirname(script_dir)

    if args.pdb:
        if args.out:
            out_path = args.out
        else:
            out_path = os.path.join(
                casp17_dir, "submissions",
                f"{args.target.upper()}_model{args.model}.ts"
            )
        format_pdb_to_casp_ts(
            pdb_path=args.pdb,
            target_id=args.target,
            model_index=args.model,
            method=args.method,
            parent=args.parent,
            author=args.author,
            out_path=out_path,
        )
    elif args.multi:
        if args.out:
            out_path = args.out
        else:
            out_path = os.path.join(
                casp17_dir, "submissions",
                f"{args.target.upper()}_multimodel.ts"
            )
        format_multi_model(
            pdb_paths=args.multi,
            target_id=args.target,
            method=args.method,
            parent=args.parent,
            author=args.author,
            out_path=out_path,
        )


if __name__ == "__main__":
    main()
