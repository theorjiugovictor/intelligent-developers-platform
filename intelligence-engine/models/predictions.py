"""Prediction and ML model stubs for the Intelligence Engine.
These are lightweight placeholders so the service can start; replace with real model logic later.
"""
from __future__ import annotations

from typing import Any, Dict
from datetime import datetime, timezone
import logging
import random

from config import settings

logger = logging.getLogger(__name__)

class BaseModelStub:
    """Common stub functionality for ML models."""
    def __init__(self, name: str):
        self.name = name
        self.last_trained_at: datetime | None = None
        self.version: str = "0.1.0-stub"

    async def train(self) -> Dict[str, Any]:
        """Simulate training by updating metadata."""
        self.last_trained_at = datetime.now(timezone.utc)
        logger.info(f"[ML] Trained {self.name} model (stub)")
        return {
            "model": self.name,
            "status": "trained",
            "version": self.version,
            "trained_at": self.last_trained_at.isoformat()
        }

class BreakingChangeDetector(BaseModelStub):
    def __init__(self):
        super().__init__("breaking_change_detector")
        self.threshold = settings.BREAKING_CHANGE_THRESHOLD

    async def predict(self, commit_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Return a pseudo probability a commit introduces a breaking change."""
        probability = round(random.uniform(0, 1), 3)
        is_breaking = probability >= self.threshold
        result = {
            "model": self.name,
            "probability_breaking": probability,
            "threshold": self.threshold,
            "is_breaking": is_breaking,
            "commit": commit_analysis.get("commit_hash"),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        logger.info(f"[ML] Breaking change prediction: {result}")
        return result

class AnomalyDetector(BaseModelStub):
    def __init__(self):
        super().__init__("anomaly_detector")
        self.threshold = settings.ANOMALY_THRESHOLD

    async def detect_anomalies(self, log_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Pretend to detect anomalies in logs."""
        anomaly_score = round(random.uniform(0, 1), 3)
        has_anomaly = anomaly_score >= self.threshold
        result = {
            "model": self.name,
            "anomaly_score": anomaly_score,
            "threshold": self.threshold,
            "has_anomaly": has_anomaly,
            "log_count": log_analysis.get("log_count"),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        logger.info(f"[ML] Log anomaly detection: {result}")
        return result

class PerformancePredictor(BaseModelStub):
    def __init__(self):
        super().__init__("performance_predictor")
        self.degradation_threshold = settings.PERFORMANCE_DEGRADATION_THRESHOLD

    async def predict(self, trace_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate predicting future performance degradation."""
        predicted_degradation = round(random.uniform(0, 0.5), 3)
        at_risk = predicted_degradation >= self.degradation_threshold
        result = {
            "model": self.name,
            "predicted_degradation": predicted_degradation,
            "degradation_threshold": self.degradation_threshold,
            "at_risk": at_risk,
            "avg_latency_ms": trace_analysis.get("avg_latency_ms"),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        logger.info(f"[ML] Performance prediction: {result}")
        return result

