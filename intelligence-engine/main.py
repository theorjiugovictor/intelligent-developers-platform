"""
Main FastAPI application for the Intelligence Engine
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

from config import settings
from database import init_db, get_db
from models.predictions import BreakingChangeDetector, AnomalyDetector, PerformancePredictor
from services.commit_analyzer import CommitAnalyzer
from services.log_analyzer import LogAnalyzer
from services.trace_analyzer import TraceAnalyzer
from services.self_healer import SelfHealer
from services.optimizer import Optimizer
from api.routes import router
from monitoring import setup_monitoring

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler"""
    # Startup
    logger.info("Starting Intelligence Engine...")
    await init_db()

    # Initialize ML models
    logger.info("Loading ML models...")
    app.state.breaking_change_detector = BreakingChangeDetector()
    app.state.anomaly_detector = AnomalyDetector()
    app.state.performance_predictor = PerformancePredictor()

    # Initialize services
    app.state.commit_analyzer = CommitAnalyzer()
    app.state.log_analyzer = LogAnalyzer()
    app.state.trace_analyzer = TraceAnalyzer()
    app.state.self_healer = SelfHealer()
    app.state.optimizer = Optimizer()

    logger.info("Intelligence Engine started successfully!")

    yield

    # Shutdown
    logger.info("Shutting down Intelligence Engine...")

# Create FastAPI app
app = FastAPI(
    title="Intelligent Development Platform - Intelligence Engine",
    description="AI/ML powered platform for predictive development insights",
    version="1.0.0",
    lifespan=lifespan
)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup monitoring
setup_monitoring(app)

# Include routers
app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Intelligence Engine",
        "status": "running",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "components": {
            "database": "connected",
            "ml_models": "loaded",
            "services": "ready"
        }
    }

@app.post("/api/v1/analyze/commit")
async def analyze_commit(
    repository: str,
    commit_hash: str,
    background_tasks: BackgroundTasks
):
    """Analyze a commit for breaking changes and issues"""
    try:
        analyzer = app.state.commit_analyzer
        result = await analyzer.analyze_commit(repository, commit_hash)

        # Trigger background analysis
        background_tasks.add_task(
            app.state.breaking_change_detector.predict,
            result
        )

        return result
    except Exception as e:
        logger.error(f"Error analyzing commit: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/analyze/logs")
async def analyze_logs(
    logs: List[Dict[str, Any]],
    background_tasks: BackgroundTasks
):
    """Analyze logs for patterns and anomalies"""
    try:
        analyzer = app.state.log_analyzer
        result = await analyzer.analyze_logs(logs)

        # Trigger anomaly detection
        background_tasks.add_task(
            app.state.anomaly_detector.detect_anomalies,
            result
        )

        return result
    except Exception as e:
        logger.error(f"Error analyzing logs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/analyze/traces")
async def analyze_traces(
    traces: List[Dict[str, Any]],
    background_tasks: BackgroundTasks
):
    """Analyze traces for performance issues"""
    try:
        analyzer = app.state.trace_analyzer
        result = await analyzer.analyze_traces(traces)

        # Trigger performance prediction
        background_tasks.add_task(
            app.state.performance_predictor.predict,
            result
        )

        return result
    except Exception as e:
        logger.error(f"Error analyzing traces: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/heal")
async def trigger_healing(
    issue_type: str,
    context: Dict[str, Any]
):
    """Trigger self-healing for an issue"""
    try:
        healer = app.state.self_healer
        result = await healer.heal(issue_type, context)
        return result
    except Exception as e:
        logger.error(f"Error triggering healing: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/recommendations")
async def get_recommendations(
    limit: int = 10,
    severity: Optional[str] = None
):
    """Get optimization recommendations"""
    try:
        optimizer = app.state.optimizer
        recommendations = await optimizer.get_recommendations(
            limit=limit,
            severity=severity
        )
        return recommendations
    except Exception as e:
        logger.error(f"Error getting recommendations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/train")
async def trigger_training(
    model_type: str,
    background_tasks: BackgroundTasks
):
    """Trigger model training"""
    try:
        if model_type == "breaking_change":
            background_tasks.add_task(
                app.state.breaking_change_detector.train
            )
        elif model_type == "anomaly":
            background_tasks.add_task(
                app.state.anomaly_detector.train
            )
        elif model_type == "performance":
            background_tasks.add_task(
                app.state.performance_predictor.train
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unknown model type: {model_type}"
            )

        return {
            "status": "training_started",
            "model_type": model_type,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error triggering training: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

