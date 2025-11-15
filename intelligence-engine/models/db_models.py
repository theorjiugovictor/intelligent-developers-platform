"""
Database models for storing analysis results
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, JSON
from datetime import datetime, timezone
from database import Base
from sqlalchemy.sql import func


class CommitAnalysis(Base):
    """Store commit analysis results"""
    __tablename__ = "commit_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    repository = Column(String, index=True)
    commit_hash = Column(String, index=True)
    changed_files = Column(Integer)
    lines_added = Column(Integer)
    lines_deleted = Column(Integer)
    risky_patterns = Column(JSON)
    complexity_delta = Column(Float)
    should_commit = Column(Boolean, default=True)
    code_quality_score = Column(Float)
    test_coverage = Column(Float)
    breaking_changes = Column(Integer, default=0)
    confidence = Column(Float)
    recommendation = Column(String)
    reasons = Column(JSON)
    issues = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class LogAnalysis(Base):
    """Store log analysis results"""
    __tablename__ = "log_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    log_count = Column(Integer)
    error_count = Column(Integer)
    warning_count = Column(Integer)
    info_count = Column(Integer)
    distinct_services = Column(JSON)
    error_rate = Column(Float)
    dominant_level = Column(String)
    spike_score = Column(Float)
    anomalies_detected = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class TraceAnalysis(Base):
    """Store trace analysis results"""
    __tablename__ = "trace_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    trace_count = Column(Integer)
    avg_duration_ms = Column(Float)
    max_duration_ms = Column(Float)
    min_duration_ms = Column(Float)
    slow_traces = Column(Integer)
    distinct_services = Column(JSON)
    performance_issues = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class HealingAction(Base):
    """Store self-healing actions"""
    __tablename__ = "healing_actions"
    
    id = Column(Integer, primary_key=True, index=True)
    action_id = Column(String, unique=True, index=True)
    issue_type = Column(String, index=True)
    service = Column(String, index=True)
    status = Column(String, default="pending")  # pending, in_progress, completed, failed
    action_taken = Column(Text)
    success = Column(Boolean, nullable=True)
    error_message = Column(Text, nullable=True)
    context = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
