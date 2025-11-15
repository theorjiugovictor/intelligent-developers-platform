"""Log analysis service stub.
Aggregates log entries into simple metrics.
"""
from __future__ import annotations


from typing import Dict, Any, List
from datetime import datetime, timezone
import logging
import random
from monitoring import log_analyses_total
logger = logging.getLogger(__name__)

class LogAnalyzer:
    def __init__(self):
        self.initialized = True

    async def analyze_logs(self, logs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregate logs and derive simple stats."""
        log_count = len(logs)
        error_count = sum(1 for l in logs if l.get("level") == "error")
        warn_count = sum(1 for l in logs if l.get("level") == "warning")
        info_count = sum(1 for l in logs if l.get("level") == "info")
        services = list({l.get("service") for l in logs if l.get("service")})
        # Increment Prometheus metric for log analysis
        result = "success" if log_count > 0 else "empty"
        log_analyses_total.labels(result=result).inc()
        return {
            "log_count": log_count,
            "error_count": error_count,
            "warning_count": warn_count,
            "info_count": info_count,
            "distinct_services": services,
            "error_rate": round(error_count / log_count, 3) if log_count else 0.0,
            "dominant_level": max(("error","warning","info"), key=lambda lvl: sum(1 for l in logs if l.get("level") == lvl)) if log_count else None,
            "spike_score": round(random.uniform(0, 1), 3),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

