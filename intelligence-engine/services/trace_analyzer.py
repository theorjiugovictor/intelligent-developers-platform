"""Trace analysis service stub.
Summarizes trace spans for simple performance indicators.
"""
from __future__ import annotations


from typing import Dict, Any, List
from datetime import datetime, timezone
import logging
import random
from monitoring import trace_analyses_total
logger = logging.getLogger(__name__)

class TraceAnalyzer:
    def __init__(self):
        self.initialized = True

    async def analyze_traces(self, traces: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Compute simple latency stats from trace data."""
        span_durations = [t.get("duration_ms", random.randint(10, 500)) for t in traces]
        count = len(span_durations)
        avg_duration = sum(span_durations)/count if count else 0.0
        p95 = sorted(span_durations)[int(0.95*count)-1] if count >= 1 else 0
        services = list({t.get("service") for t in traces if t.get("service")})
        slow_threshold = 1000  # 1 second
        slow_count = len([d for d in span_durations if d > slow_threshold])
        
        # Increment Prometheus metric for trace analysis
        result = "success" if count > 0 else "empty"
        trace_analyses_total.labels(result=result).inc()
        return {
            "trace_count": count,
            "avg_duration_ms": round(avg_duration, 2),
            "max_duration_ms": max(span_durations) if count else 0,
            "min_duration_ms": min(span_durations) if count else 0,
            "slow_traces": slow_count,
            "distinct_services": services,
            "p95_latency_ms": p95,
            "throughput_req_s": round(random.uniform(5, 150), 2),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
