"""
Request models for API endpoints
"""
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime


class LogEntry(BaseModel):
    """Individual log entry"""
    timestamp: str
    level: str
    message: str
    service: str
    metadata: Optional[Dict[str, Any]] = None


class LogAnalysisRequest(BaseModel):
    """Request body for log analysis"""
    logs: List[LogEntry]


class TraceEntry(BaseModel):
    """Individual trace entry"""
    trace_id: str
    span_id: str
    service: str
    operation: str
    duration_ms: float
    timestamp: str
    metadata: Optional[Dict[str, Any]] = None


class TraceAnalysisRequest(BaseModel):
    """Request body for trace analysis"""
    traces: List[TraceEntry]


class HealingRequest(BaseModel):
    """Request body for triggering healing"""
    issue_type: str
    context: Dict[str, Any]


class TrainingRequest(BaseModel):
    """Request body for model training"""
    model_type: str
