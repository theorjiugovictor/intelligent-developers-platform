"""
Monitoring and observability setup
"""
from fastapi import FastAPI
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import time

# Metrics
request_count = Counter(
    'idp_http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'idp_http_request_duration_seconds',
    'HTTP request duration',
    ['endpoint'],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
)


# Business metrics
predictions_total = Counter(
    'idp_predictions_total',
    'Total predictions made',
    ['model_type', 'result']
)

log_analyses_total = Counter(
    'idp_log_analyses_total',
    'Total log analyses performed',
    ['result']
)

trace_analyses_total = Counter(
    'idp_trace_analyses_total',
    'Total trace analyses performed',
    ['result']
)

recommendations_total = Counter(
    'idp_recommendations_total',
    'Total recommendations generated',
    ['severity']
)

active_models = Gauge(
    'idp_active_models',
    'Number of active ML models'
)

healing_actions_total = Counter(
    'idp_healing_actions_total',
    'Total healing actions',
    ['action_type', 'status']
)

db_operations_total = Counter(
    'idp_db_operations_total',
    'Total database operations',
    ['operation', 'status']
)

def setup_monitoring(app: FastAPI):
    """Setup monitoring for the application"""

    @app.middleware("http")
    async def monitor_requests(request, call_next):
        """Monitor HTTP requests"""
        start_time = time.time()

        response = await call_next(request)

        duration = time.time() - start_time

        # Record metrics
        request_count.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code
        ).inc()

        request_duration.labels(
            endpoint=request.url.path
        ).observe(duration)

        return response

    @app.get("/metrics")
    async def metrics():
        """Prometheus metrics endpoint"""
        return Response(
            content=generate_latest(),
            media_type=CONTENT_TYPE_LATEST
        )
