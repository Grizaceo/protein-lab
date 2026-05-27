import logging
import math
import random
from typing import List, Dict, Any, Tuple
from eac_bridge.ledger import ResearchLedger

logger = logging.getLogger(__name__)

class TFIDFProxyEmbedder:
    """Lightweight, self-contained bag-of-words / TF-IDF embedder to calculate cosine similarity locally."""
    @staticmethod
    def tokenize(text: str) -> List[str]:
        return re.findall(r'\w+', text.lower()) if 're' in globals() else text.lower().split()

    @staticmethod
    def get_cosine_similarity(text_a: str, text_b: str) -> float:
        import re
        words_a = re.findall(r'\w+', text_a.lower())
        words_b = re.findall(r'\w+', text_b.lower())
        
        dict_a = {}
        for w in words_a:
            dict_a[w] = dict_a.get(w, 0) + 1
            
        dict_b = {}
        for w in words_b:
            dict_b[w] = dict_b.get(w, 0) + 1
            
        intersection = set(dict_a.keys()) & set(dict_b.keys())
        numerator = sum([dict_a[x] * dict_b[x] for x in intersection])
        
        sum1 = sum([dict_a[x]**2 for x in dict_a.keys()])
        sum2 = sum([dict_b[x]**2 for x in dict_b.keys()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)
        
        if not denominator:
            return 0.0
        return float(numerator) / denominator

class LocalWorldModel:
    """
    Surrogate World Model (derived from AGENTIC_METRIC_DISCOVERY's LocalWorldModel).
    Estimates pKd and uncertainty for candidate hypotheses without running MAMMAL.
    Integrates UCB selection, novelty penalties, and shadow calibration cycles.
    """
    def __init__(self, ledger: ResearchLedger, config: dict):
        self.ledger = ledger
        self.config = config
        
        wm_config = config.get("world_model", {})
        self.enabled = wm_config.get("enabled", True)
        self.mode = wm_config.get("mode", "shadow")
        self.shadow_cycles = int(wm_config.get("shadow_cycles", 10))
        self.shadow_budget_usd = float(wm_config.get("shadow_budget_usd", 5.0))
        
        weights = wm_config.get("weights", {})
        self.w_ledger = float(weights.get("w_ledger", 0.5))
        self.w_novelty_penalty = float(weights.get("w_novelty_penalty", 0.3))
        
        gates = wm_config.get("gates", {})
        self.min_samples = int(gates.get("min_samples", 10))
        self.min_spearman_rho = float(gates.get("min_spearman_rho", 0.5))
        self.min_top_k_recall = float(gates.get("min_top_k_recall", 0.7))
        self.max_false_negative_rate = float(gates.get("max_false_negative_rate", 0.2))

        self.current_cycle = 0
        self.recent_evaluated: List[str] = []

    def predict(self, statement: str) -> Tuple[float, float, float]:
        """
        Predicts:
          1. fitness_hat (estimated pKd)
          2. uncertainty (higher if cold start or low similarity)
          3. novelty_score (1.0 = completely unique, 0.0 = redundant)
        """
        # Load historical runs from the SQLite ledger
        history = self.ledger.load_world_model_observations(limit=500)
        
        # 1. k-NN regression over history statement strings
        if not history:
            # Cold-start defaults
            ledger_hat = 5.0  # intermediate pKd
            uncertainty = 1.0  # max uncertainty
        else:
            similarities = []
            for entry in history:
                sim = TFIDFProxyEmbedder.get_cosine_similarity(statement, entry["statement"])
                similarities.append((sim, entry["fitness"]))
            
            # Sort by similarity descending
            similarities.sort(key=lambda x: x[0], reverse=True)
            top_k = similarities[:5]
            
            # Weighted average
            inv_weights = [x[0] for x in top_k]
            total_w = sum(inv_weights)
            if total_w > 0:
                ledger_hat = sum([x[1] * w for x, w in zip(top_k, inv_weights)]) / total_w
                # Uncertainty scales inversely with the best similarity score
                best_sim = top_k[0][0]
                uncertainty = max(0.1, 1.0 - best_sim)
            else:
                ledger_hat = 5.0
                uncertainty = 1.0

        # 2. Novelty Scorer Penalty
        novelty_score = 1.0
        if self.recent_evaluated:
            max_sim = max([TFIDFProxyEmbedder.get_cosine_similarity(statement, prev) for prev in self.recent_evaluated], default=0.0)
            novelty_score = 1.0 - max_sim

        # Calculate final fitness_hat using weights
        fitness_hat = self.w_ledger * ledger_hat - self.w_novelty_penalty * (1.0 - novelty_score)
        
        return float(fitness_hat), float(uncertainty), float(novelty_score)

    def select_top_k(self, candidates: List[Any], k: int, beta: float = 0.5, eps: float = 0.25) -> List[Any]:
        """
        Selects top k candidates using UCB:
          score = predicted_pkd + beta * uncertainty.
        Includes epsilon-greedy random exploration index to keep search space diverse.
        """
        if not candidates:
            return []

        # If World Model is disabled, bypass it and just return the first K
        if not self.enabled or self.mode == "disabled":
            return candidates[:k]

        predictions = []
        for c in candidates:
            statement = c.statement
            fit_hat, unc, nov = self.predict(statement)
            ucb_score = fit_hat + beta * unc
            predictions.append((c, ucb_score, fit_hat, unc, nov))

        # Save predictions to the ledger before pruning
        for c, _, fit_hat, unc, nov in predictions:
            self.ledger.save_prediction(c.id, fit_hat, unc, regime=3, novelty_score=nov, details={"wm_mode": self.mode})

        # Sort by UCB score descending
        predictions.sort(key=lambda x: x[1], reverse=True)

        n_random = max(0, math.floor(eps * k))
        n_top = max(1, k - n_random)

        winners = [x[0] for x in predictions[:n_top]]
        remaining = [x[0] for x in predictions[n_top:]]

        if n_random > 0 and remaining:
            random_sample = random.sample(remaining, min(n_random, len(remaining)))
            winners.extend(random_sample)

        # Update recently evaluated window
        for w in winners:
            self.recent_evaluated.append(w.statement)
            if len(self.recent_evaluated) > 20:
                self.recent_evaluated.pop(0)

        logger.info(f"World Model selected {len(winners)} hypotheses out of {len(candidates)} using UCB (mode={self.mode})")
        return winners

    def tick_shadow_cycle(self):
        """Ticks the shadow mode and checks if the gates to active mode can be unlocked."""
        if not self.enabled or self.mode != "shadow":
            return

        self.current_cycle += 1
        if self.current_cycle < self.shadow_cycles:
            return

        # Perform calibration calculations
        data = self.ledger.get_calibration_data()
        if len(data) < self.min_samples:
            logger.info(f"Shadow cycle tick: not enough samples for calibration yet ({len(data)}/{self.min_samples})")
            return

        # Calculate Mean Absolute Error
        hats = [d["hat"] for d in data]
        reals = [d["real"] for d in data]
        mae = sum([abs(h - r) for h, r in zip(hats, reals)]) / len(data)

        # Calculate a simple correlation proxy
        # (Spearman rho proxy: check if top candidates match top actuals)
        k = min(3, len(data))
        real_top = sorted(range(len(data)), key=lambda i: reals[i], reverse=True)[:k]
        pred_top = sorted(range(len(data)), key=lambda i: hats[i], reverse=True)[:k]
        overlap = len(set(real_top) & set(pred_top))
        recall = overlap / k

        logger.info(f"World Model Shadow calibration report: MAE={mae:.3f}, top-{k} recall={recall:.2f}")

        # Check gates
        if recall >= self.min_top_k_recall:
            self.mode = "active"
            logger.info("World Model successfully calibrated and promoted to ACTIVE mode!")
            # Save promotion details to file
            Path("artifacts/world_model_promotion.json").write_text(json.dumps({
                "mode": "active",
                "cycles": self.current_cycle,
                "mae": mae,
                "recall": recall
            }, indent=2) if 'json' in sys.modules else str({"recall": recall}))
        else:
            self.mode = "disabled"
            logger.warning("World Model calibration failed to meet top-K recall gates. Disabling surrogate layer.")
            Path("artifacts/world_model_calibration_failed.md").write_text(
                f"# Calibration Failed\nRecall={recall:.2f} (gate={self.min_top_k_recall})\nDisabling World Model.\n"
            )
