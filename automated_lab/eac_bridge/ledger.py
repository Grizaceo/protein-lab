import sqlite3
import os
import json
import logging
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)

class ResearchLedger:
    """
    SQLite-based research ledger with concurrent WAL mode enabled.
    Stores all hypotheses, predictions, outcomes, and Harness safety logs.
    Serves as the memory core for k-NN regression of the Surrogate World Model.
    """
    def __init__(self, db_path: str = "artifacts/eac_research_ledger.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            # Table for generated hypotheses
            conn.execute("""
                CREATE TABLE IF NOT EXISTS hypotheses (
                    id TEXT PRIMARY KEY,
                    statement TEXT,
                    rationale TEXT,
                    novelty_claim TEXT,
                    test_strategy TEXT,
                    metadata TEXT,
                    status TEXT,
                    score REAL DEFAULT 0.0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # Table for world model predictions
            conn.execute("""
                CREATE TABLE IF NOT EXISTS predictions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    hypothesis_id TEXT,
                    predicted_score REAL,
                    uncertainty REAL,
                    regime INTEGER,
                    novelty_score REAL,
                    details TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # Table for physical/computational results
            conn.execute("""
                CREATE TABLE IF NOT EXISTS results (
                    hypothesis_id TEXT PRIMARY KEY,
                    status TEXT, -- 'ok', 'error'
                    pkd REAL,
                    plddt REAL,
                    ihara_zeta REAL,
                    error_msg TEXT,
                    execution_time_ms REAL,
                    raw_output TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(hypothesis_id) REFERENCES hypotheses(id)
                );
            """)

            # Table for safety audits & Harness signatures
            conn.execute("""
                CREATE TABLE IF NOT EXISTS safety_audits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    run_id TEXT,
                    signature TEXT, -- 'S01', 'S02', etc.
                    details TEXT,
                    verdict TEXT -- 'abort', 'logged'
                );
            """)
            conn.commit()

    def save_hypothesis(self, hyp: dict[str, Any]):
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO hypotheses (id, statement, rationale, novelty_claim, test_strategy, metadata, status, score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    status=excluded.status,
                    score=excluded.score;
            """, (
                hyp["id"],
                hyp["statement"],
                hyp["rationale"],
                hyp["novelty_claim"],
                hyp["test_strategy"],
                json.dumps(hyp.get("metadata", {})),
                hyp.get("status", "generated"),
                hyp.get("score", 0.0)
            ))
            conn.commit()

    def save_prediction(self, hyp_id: str, predicted_score: float, uncertainty: float, regime: int, novelty_score: float, details: dict[str, Any]):
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO predictions (hypothesis_id, predicted_score, uncertainty, regime, novelty_score, details)
                VALUES (?, ?, ?, ?, ?, ?);
            """, (
                hyp_id,
                predicted_score,
                uncertainty,
                regime,
                novelty_score,
                json.dumps(details)
            ))
            conn.commit()

    def save_result(self, hyp_id: str, status: str, pkd: Optional[float] = None, plddt: Optional[float] = None, ihara_zeta: Optional[float] = None, error_msg: Optional[str] = None, execution_time_ms: float = 0.0, raw_output: Optional[dict[str, Any]] = None):
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO results (hypothesis_id, status, pkd, plddt, ihara_zeta, error_msg, execution_time_ms, raw_output)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(hypothesis_id) DO UPDATE SET
                    status=excluded.status,
                    pkd=excluded.pkd,
                    plddt=excluded.plddt,
                    ihara_zeta=excluded.ihara_zeta,
                    error_msg=excluded.error_msg,
                    execution_time_ms=excluded.execution_time_ms,
                    raw_output=excluded.raw_output,
                    updated_at=CURRENT_TIMESTAMP;
            """, (
                hyp_id,
                status,
                pkd,
                plddt,
                ihara_zeta,
                error_msg,
                execution_time_ms,
                json.dumps(raw_output or {})
            ))
            # Also update the hypothesis score to match the actual pkd/surrogate metric
            if pkd is not None:
                conn.execute("UPDATE hypotheses SET score = ? WHERE id = ?;", (pkd, hyp_id))
            conn.commit()

    def log_safety_violation(self, run_id: str, signature: str, details: str, verdict: str):
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO safety_audits (run_id, signature, details, verdict)
                VALUES (?, ?, ?, ?);
            """, (run_id, signature, details, verdict))
            conn.commit()

    def load_world_model_observations(self, limit: int = 500) -> list[dict[str, Any]]:
        """Loads historical pairings of hypothesis statements + actual pkd/score for k-NN regression."""
        with self._get_connection() as conn:
            cursor = conn.execute("""
                SELECT h.statement, r.pkd, r.plddt, r.ihara_zeta
                FROM hypotheses h
                JOIN results r ON h.id = r.hypothesis_id
                WHERE r.status = 'ok' AND r.pkd IS NOT NULL
                ORDER BY r.updated_at DESC
                LIMIT ?;
            """, (limit,))
            rows = cursor.fetchall()
            return [
                {
                    "statement": row[0],
                    "fitness": row[1],
                    "plddt": row[2],
                    "ihara_zeta": row[3]
                }
                for row in rows
            ]

    def get_calibration_data(self) -> list[dict[str, float]]:
        """Retrieves prediction vs actual outcomes for model quality metrics."""
        with self._get_connection() as conn:
            cursor = conn.execute("""
                SELECT p.predicted_score, r.pkd
                FROM predictions p
                JOIN results r ON p.hypothesis_id = r.hypothesis_id
                WHERE r.status = 'ok' AND r.pkd IS NOT NULL;
            """)
            rows = cursor.fetchall()
            return [{"hat": row[0], "real": row[1]} for row in rows]
