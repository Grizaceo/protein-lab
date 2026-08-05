"""
automated_lab/backends/__init__.py
====================================
Registry central de adapters para todas las investigaciones del protein-lab.

Uso:
    from automated_lab.backends import get_adapter
    adapter = get_adapter("ferritina-biomaterial")
    print(adapter.summary())
"""

# Cargar .env del repo automáticamente
from pathlib import Path
from dotenv import load_dotenv

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_env_file = _REPO_ROOT / ".env"
if _env_file.exists():
    load_dotenv(_env_file)

from automated_lab.backends.ferritina_adapter import FerritinaAdapter
from automated_lab.backends.hemoglobina_adapter import HemoglobinaAdapter
from automated_lab.backends.fibromialgia_adapter import FibromialgiaAdapter
# NOTA 2026-08-05: materiales_adapter migrado a material-science-lab
# (chasis inicial P0). Esta línea ya no se registra aquí.
from automated_lab.backends.hirondellea_adapter import HirondelleaAdapter
from automated_lab.backends.replicacion_adapter import (
    ReplicacionGSE274134Adapter,
    CASP17Adapter,
)
from automated_lab.backends.colab_bridge import ColabBridge
from automated_lab.backends.local_mammal import LocalMammalBackend
from automated_lab.backends.bionemo_adapter import BioNeMoAdapter
from automated_lab.backends.dgm_adapter import DGMAdapter
from automated_lab.backends.kiss_adapter import KISSAdapter
from automated_lab.backends.kiss_dgm_bridge import KissDgmBridge

# Registry de adapters por nombre
ADAPTERS = {
    # Investigaciones internas
    "ferritina-biomaterial": FerritinaAdapter,
    "ferritina": FerritinaAdapter,
    "hemoglobina-mtr": HemoglobinaAdapter,
    "hemoglobina": HemoglobinaAdapter,
    "exp01-hemoglobina": HemoglobinaAdapter,
    "fibromialgia": FibromialgiaAdapter,
    # NOTA 2026-08-05: "materiales-avanzados-chile"/"materiales"/"catalizadores-renio"
    # migrados a material-science-lab (P0 chasis). Usar get_adapter desde ese repo.
    "hirondellea-gigas": HirondelleaAdapter,
    "hirondellea": HirondelleaAdapter,
    "baroresistencia-gh7": HirondelleaAdapter,
    "replicacion-gse274134": ReplicacionGSE274134Adapter,
    "gse274134": ReplicacionGSE274134Adapter,
    "casp17": CASP17Adapter,
    # Infraestructura
    "colab": ColabBridge,
    "local": LocalMammalBackend,
    # Proyectos OSS integrados
    "bionemo": BioNeMoAdapter,
    "nvidia-bionemo": BioNeMoAdapter,
    "dgm": DGMAdapter,
    "darwin-godel-machine": DGMAdapter,
    "kiss": KISSAdapter,
    "kiss-discovery-engine": KISSAdapter,
    # KISS + DGM combinado
    "kiss-dgm": KissDgmBridge,
    "evolve-code": KissDgmBridge,
}


def get_adapter(name: str):
    """Obtiene un adapter por nombre."""
    adapter_cls = ADAPTERS.get(name)
    if adapter_cls is None:
        raise ValueError(
            f"Adapter no encontrado: '{name}'. "
            f"Disponibles: {list(set(ADAPTERS.keys()))}"
        )
    return adapter_cls


def list_adapters() -> list[str]:
    """Lista todos los adapters disponibles (nombres canónicos)."""
    seen = set()
    result = []
    for k, v in ADAPTERS.items():
        if v not in seen:
            seen.add(v)
            result.append(k)
    return result


def summary_all() -> str:
    """Ejecuta summary() de todos los adapters."""
    seen = set()
    lines = ["=== Protein Lab — Adapter Registry ===\n"]
    for name, adapter_cls in ADAPTERS.items():
        if adapter_cls not in seen:
            seen.add(adapter_cls)
            if hasattr(adapter_cls, "summary"):
                lines.append(adapter_cls.summary())
            else:
                lines.append(f"  {name}: {adapter_cls.__name__} (sin summary)")
            lines.append("")
    return "\n".join(lines)
