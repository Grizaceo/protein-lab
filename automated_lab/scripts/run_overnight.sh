#!/usr/bin/env bash
# automated_lab/scripts/run_overnight.sh
# Master campaign launcher — corre campaña nocturna completa.
# Uso: bash scripts/run_overnight.sh [campaign] [hours] [max_experiments]

set -euo pipefail

LAB_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$LAB_DIR"

CAMPAIGN="${1:-fibromialgia_ruta_b}"
HOURS="${2:-8}"
MAX_EXPERIMENTS="${3:-}"

# Defaults for the cloud investigator. Override from the shell if needed.
export AUTOMATED_LAB_PROVIDER="${AUTOMATED_LAB_PROVIDER:-ollama-cloud}"
export AUTOMATED_LAB_MODEL="${AUTOMATED_LAB_MODEL:-nemotron-3-super}"
export OLLAMA_BASE_URL="${OLLAMA_BASE_URL:-https://ollama.com/v1}"
export KISS_DISCOVERY_ENGINE_DIR="${KISS_DISCOVERY_ENGINE_DIR:-/home/gris/.hermes/workspace/repos/kiss_discovery_engine}"
export KISS_GENERATOR_PROVIDER="${KISS_GENERATOR_PROVIDER:-$AUTOMATED_LAB_PROVIDER}"
export KISS_GENERATOR_MODEL="${KISS_GENERATOR_MODEL:-$AUTOMATED_LAB_MODEL}"
export KISS_MAX_TOKENS="${KISS_MAX_TOKENS:-2200}"
export KISS_MAX_CONCURRENT="${KISS_MAX_CONCURRENT:-2}"

mkdir -p results/logs
LOG_FILE="results/logs/${CAMPAIGN}_$(date +%Y%m%d_%H%M%S).log"

{
  echo "============================================"
  echo "   AUTOMATED LAB — OVERNIGHT CAMPAIGN"
  echo "============================================"
  echo "  Campaign:  $CAMPAIGN"
  echo "  Duration:  ${HOURS}h"
  echo "  Provider:  ${AUTOMATED_LAB_PROVIDER}/${AUTOMATED_LAB_MODEL}"
  echo "  Start:     $(date)"
  echo "  Working:   $(pwd)"
  echo "============================================"
  echo ""

  nvidia-smi --query-gpu=name,memory.free,memory.total,temperature.gpu --format=csv,noheader 2>/dev/null || echo "⚠ No GPU detected"
  echo ""

  if [[ -z "${OLLAMA_API_KEY:-}" && -z "${OPENROUTER_API_KEY:-}" && -z "${NVIDIA_API_KEY:-}" && -z "${NIM_API_KEY:-}" ]]; then
    echo "⚠ No cloud researcher API key detected. DTI will run; KISS/reviewer will fall back mechanically."
  fi

  CMD=(python -m engine.scheduler --campaign "$CAMPAIGN" --overnight "$HOURS")
  if [[ -n "$MAX_EXPERIMENTS" ]]; then
    CMD+=(--max-experiments "$MAX_EXPERIMENTS")
  fi
  "${CMD[@]}"

  echo ""
  echo "============================================"
  echo "   CAMPAIGN COMPLETE"
  echo "  End: $(date)"
  echo "============================================"
} 2>&1 | tee "$LOG_FILE"

echo "Log: $LOG_FILE"
