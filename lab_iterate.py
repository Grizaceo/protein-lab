#!/usr/bin/env python3
"""
lab_iterate.py — Orquestador del loop Lab ↔ Colab
==================================================
Flujo completo:
  1. Detecta ZIPs nuevos en colab_runs/ y los extrae/parsea
  2. Registra las corridas nuevas en ITERATION_STATE.json
  3. Para cada target, determina la estrategia (exploit/explore)
  4. Genera los parámetros de la próxima corrida
  5. Escribe next_run/{target}/ con PDB + config + instrucciones

Uso:
  python lab_iterate.py                  # loop completo para todos los targets
  python lab_iterate.py --target nipah   # solo un target
  python lab_iterate.py --status         # muestra tabla de estado (sin generar)
  python lab_iterate.py --dry-run        # genera params pero NO guarda estado
  python lab_iterate.py --register <run_folder> --target nipah
                                         # registra manualmente un run existente

Requisitos: solo stdlib + archivos ya en el workspace.
"""

import sys
import argparse
import textwrap
from pathlib import Path

# Asegurar que src/ esté en el path de importación
WORKSPACE = Path(__file__).parent
sys.path.insert(0, str(WORKSPACE / "src"))

from iteration.state_manager import (
    load_state, save_state, get_target,
    register_run, get_strategy, summary_table,
)
from iteration.run_analyzer import (
    find_new_runs, analyze_run_folder, build_run_record,
    infer_target,
)
from iteration.param_generator import generate_next_params, rationale
from iteration.colab_prep import prepare_next_run


# ══════════════════════════════════════════════════════════════════════════════
# Utilidades de visualización
# ══════════════════════════════════════════════════════════════════════════════

def _banner(text: str):
    width = 60
    print("=" * width)
    print(f"  {text}")
    print("=" * width)


def _section(text: str):
    print(f"\n{'─' * 50}")
    print(f"  {text}")
    print(f"{'─' * 50}")


def _print_params(params: dict, target_name: str):
    print(f"    contigs:      {params.get('contigs')}")
    print(f"    hotspot:      {params.get('hotspot') or '(ninguno)'}")
    print(f"    guide_scale:  {params.get('guide_scale')}")
    print(f"    T:            {params.get('T')}")
    print(f"    num_designs:  {params.get('num_designs')}")


# ══════════════════════════════════════════════════════════════════════════════
# Paso 1 — Ingestar nuevas corridas
# ══════════════════════════════════════════════════════════════════════════════

def _ingest_and_register(state: dict, verbose: bool = True) -> tuple[dict, list]:
    """
    Detecta runs nuevos, parsea métricas y los registra en el estado.
    Retorna (state_actualizado, lista de run_ids nuevos).
    """
    new_runs = find_new_runs(state)
    registered = []

    if not new_runs:
        if verbose:
            print("  No hay corridas nuevas para registrar.")
        return state, []

    for run_info in new_runs:
        run_id  = run_info["run_id"]
        metrics = run_info["metrics"]
        target  = run_info["target"]

        if target not in state["targets"]:
            if verbose:
                print(f"  ⚠ Target '{target}' inferido para '{run_id}' no existe en el estado — skipping")
            continue

        if verbose:
            print(f"  + Registrando: {run_id} → target={target}")
            m = metrics
            if m:
                plddt_str = f"{m.get('mean_pLDDT', '?'):.3f}" if isinstance(m.get('mean_pLDDT'), float) else "?"
                iptm_str  = f"{m.get('mean_ipTM', 'N/A'):.3f}" if isinstance(m.get('mean_ipTM'), float) else "N/A"
                pae_str   = f"{m.get('mean_pAE', '?'):.1f}"   if isinstance(m.get('mean_pAE'), float) else "?"
                print(f"    pLDDT={plddt_str}  ipTM={iptm_str}  pAE={pae_str}  n={m.get('n_designs', '?')}")
            else:
                print("    (sin métricas parseables)")

        record = build_run_record(
            run_id=run_id,
            metrics=metrics,
            params={},           # params no conocidos si vino de fuera del loop
            notes="Registrado automáticamente por lab_iterate.py",
            target=target,
        )
        state = register_run(state, target, record)
        registered.append(run_id)

    return state, registered


# ══════════════════════════════════════════════════════════════════════════════
# Paso 2 — Generar próximos parámetros y preparar next_run/
# ══════════════════════════════════════════════════════════════════════════════

def _generate_for_target(state: dict, target_name: str,
                          dry_run: bool = False, verbose: bool = True) -> dict:
    """Genera parámetros y prepara next_run/{target_name}/. Retorna params."""
    target_info = get_target(state, target_name)

    params, strategy = generate_next_params(target_info, target_name)
    rationale_text   = rationale(params, strategy, target_info)

    if verbose:
        _section(f"{target_info['display_name']} — estrategia: {strategy.upper()}")
        _print_params(params, target_name)

    if not dry_run:
        out_dir = prepare_next_run(
            target_name=target_name,
            target_info=target_info,
            params=params,
            strategy=strategy,
            rationale_text=rationale_text,
        )
        if verbose:
            print(f"\n  ▶ next_run/{target_name}/ listo:")
            for f in sorted(out_dir.iterdir()):
                size = f.stat().st_size
                size_str = f"{size/1024:.1f} KB" if size > 1024 else f"{size} B"
                print(f"    {f.name:<35} {size_str}")
    else:
        if verbose:
            print("  (dry-run: next_run/ no escrito)")

    return params


# ══════════════════════════════════════════════════════════════════════════════
# Comandos
# ══════════════════════════════════════════════════════════════════════════════

def cmd_status(args):
    """Muestra tabla de estado sin generar nada."""
    state = load_state()
    print(summary_table(state))


def cmd_loop(args):
    """Loop completo: ingestar → registrar → generar."""
    _banner("lab_iterate.py — Loop Lab ↔ Colab")

    state = load_state()
    targets = [args.target] if args.target else list(state["targets"].keys())

    # Paso 1: ingestar corridas nuevas
    _section("Paso 1 — Detectar y registrar corridas nuevas")
    state, new_ids = _ingest_and_register(state, verbose=not args.quiet)

    if new_ids and not args.dry_run:
        save_state(state)
        print(f"\n  Estado guardado. {len(new_ids)} run(s) nuevos registrados.")

    # Paso 2: generar parámetros para cada target
    _section("Paso 2 — Generar parámetros para próximas corridas")
    for target_name in targets:
        if target_name not in state["targets"]:
            print(f"  ⚠ Target '{target_name}' no encontrado en el estado.")
            continue
        _generate_for_target(state, target_name,
                              dry_run=args.dry_run, verbose=not args.quiet)

    # Resumen final
    print()
    _banner("Listo")
    for target_name in targets:
        if target_name in state["targets"]:
            out = WORKSPACE / "next_run" / target_name
            if out.exists() and not args.dry_run:
                print(f"  ▶ {target_name}: next_run/{target_name}/COLAB_INSTRUCTIONS.md")
    print()
    print("  Sube los archivos a Colab, descarga el ZIP, ponlo en colab_runs/")
    print("  y vuelve a ejecutar:  python lab_iterate.py")


def cmd_register(args):
    """Registra manualmente un run_id existente."""
    if not args.register:
        print("ERROR: --register requiere un run_folder")
        sys.exit(1)
    if not args.target:
        print("ERROR: --register requiere --target <nipah|ferritin>")
        sys.exit(1)

    state = load_state()
    run_dir = Path(args.register)
    if not run_dir.exists():
        run_dir = WORKSPACE / "colab_runs" / args.register
    if not run_dir.exists():
        print(f"ERROR: Carpeta '{args.register}' no encontrada")
        sys.exit(1)

    metrics = analyze_run_folder(run_dir)
    record  = build_run_record(
        run_id=run_dir.name,
        metrics=metrics,
        params={},
        notes=f"Registrado manualmente via --register",
        target=args.target,
    )
    state = register_run(state, args.target, record)
    save_state(state)
    print(f"✓ '{run_dir.name}' registrado en target '{args.target}'")
    m = metrics
    if m:
        print(f"  pLDDT={m.get('mean_pLDDT', '?')}  ipTM={m.get('mean_ipTM', 'N/A')}  "
              f"pAE={m.get('mean_pAE', '?')}  n={m.get('n_designs', '?')}")


# ══════════════════════════════════════════════════════════════════════════════
# Punto de entrada
# ══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        prog="lab_iterate.py",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent("""\
            Orquestador del loop Lab ↔ Colab para diseño de proteínas.

            Detecta corridas nuevas en colab_runs/, actualiza el estado,
            y genera next_run/{target}/ con los parámetros para la próxima
            corrida en Google Colab (RFdiffusion + ProteinMPNN + AF2).
        """),
    )
    parser.add_argument(
        "--target", metavar="NAME",
        help="Procesar solo este target (nipah|ferritin). Por defecto: todos.",
    )
    parser.add_argument(
        "--status", action="store_true",
        help="Mostrar tabla de estado sin generar nada.",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Calcular params y mostrar, pero no guardar estado ni escribir next_run/.",
    )
    parser.add_argument(
        "--register", metavar="RUN_FOLDER",
        help="Registrar manualmente una carpeta run existente en colab_runs/.",
    )
    parser.add_argument(
        "--quiet", "-q", action="store_true",
        help="Suprimir output detallado.",
    )

    args = parser.parse_args()

    if args.status:
        cmd_status(args)
    elif args.register:
        cmd_register(args)
    else:
        cmd_loop(args)


if __name__ == "__main__":
    main()
