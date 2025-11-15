#!/usr/bin/env python3
"""
Script to populate Grafana by making many requests to the Intelligence Engine API.
This generates metrics, logs, and traces that will be visualized in the dashboard.
"""
import requests
import random
import time
from datetime import datetime, timedelta, timezone
import json

BASE_URL = "http://localhost:8000"

# Sample data generators
SERVICES = ["api-gateway", "user-service", "data-collector", "intelligence-engine", "auth-service", "payment-service"]
LOG_LEVELS = ["INFO", "WARNING", "ERROR", "DEBUG"]
LOG_MESSAGES = {
    "INFO": [
        "Request processed successfully",
        "Service started",
        "Health check passed",
        "Cache hit",
        "User logged in",
        "Data synced",
        "API call completed"
    ],
    "WARNING": [
        "Slow query detected",
        "High memory usage",
        "Rate limit approaching",
        "Cache miss",
        "Retry attempt",
        "Deprecated API used"
    ],
    "ERROR": [
        "Database connection failed",
        "Authentication failed",
        "Timeout occurred",
        "Invalid input",
        "Permission denied",
        "Service unavailable",
        "Connection refused"
    ],
    "DEBUG": [
        "Variable value: 42",
        "Function called",
        "Loop iteration",
        "Processing data chunk"
    ]
}

OPERATIONS = [
    "http.request",
    "database.query",
    "cache.get",
    "api.call",
    "auth.validate",
    "data.process",
    "file.read",
    "queue.publish"
]

ISSUE_TYPES = ["memory_leak", "slow_query", "connection_timeout", "high_cpu", "disk_space"]

def generate_timestamp(offset_minutes=0):
    """Generate ISO timestamp"""
    dt = datetime.now(timezone.utc) - timedelta(minutes=offset_minutes)
    return dt.isoformat()

def generate_logs(count=10, error_rate=0.1):
    """Generate random log entries"""
    logs = []
    for i in range(count):
        # Determine log level based on error rate
        if random.random() < error_rate:
            level = "ERROR"
        elif random.random() < 0.3:
            level = "WARNING"
        elif random.random() < 0.15:
            level = "DEBUG"
        else:
            level = "INFO"
        
        service = random.choice(SERVICES)
        message = random.choice(LOG_MESSAGES[level])
        
        logs.append({
            "timestamp": generate_timestamp(random.randint(0, 60)),
            "level": level,
            "message": message,
            "service": service,
            "metadata": {
                "request_id": f"req-{random.randint(1000, 9999)}",
                "user_id": f"user-{random.randint(1, 100)}"
            }
        })
    
    return logs

def generate_traces(count=10, slow_rate=0.15):
    """Generate random trace entries"""
    traces = []
    for i in range(count):
        service = random.choice(SERVICES)
        operation = random.choice(OPERATIONS)
        
        # Generate duration with some slow traces
        if random.random() < slow_rate:
            duration = random.uniform(500, 3000)  # Slow trace
        else:
            duration = random.uniform(10, 200)  # Normal trace
        
        traces.append({
            "trace_id": f"trace-{random.randint(10000, 99999)}",
            "span_id": f"span-{random.randint(1000, 9999)}",
            "service": service,
            "operation": operation,
            "duration_ms": round(duration, 2),
            "timestamp": generate_timestamp(random.randint(0, 60)),
            "metadata": {
                "http_status": random.choice([200, 200, 200, 201, 400, 404, 500]),
                "endpoint": f"/api/v1/{operation.split('.')[0]}"
            }
        })
    
    return traces

def send_log_analysis(logs_count=20, error_rate=0.1):
    """Send log analysis request"""
    try:
        logs = generate_logs(logs_count, error_rate)
        response = requests.post(
            f"{BASE_URL}/api/v1/analyze/logs",
            json={"logs": logs},
            timeout=10
        )
        if response.status_code == 200:
            print(f"✓ Log analysis: {logs_count} logs, error_rate={error_rate:.2f}")
            return True
        else:
            print(f"✗ Log analysis failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Log analysis error: {e}")
        return False

def send_breaking_change_prediction(is_breaking=False):
    """Send a prediction to simulate breaking change detection"""
    try:
        # This will trigger metrics via the commit analyzer
        repo = random.choice(["frontend", "backend", "api", "services", "infrastructure"])
        commit = f"abc{random.randint(1000, 9999)}"
        
        response = requests.post(
            f"{BASE_URL}/api/v1/analyze/commit",
            params={
                "repository": repo,
                "commit_hash": commit
            },
            timeout=10
        )
        if response.status_code == 200:
            result = "breaking" if is_breaking else "safe"
            print(f"✓ Breaking change prediction: {result}")
            return True
        else:
            print(f"✗ Breaking change prediction failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Breaking change prediction error: {e}")
        return False

def send_anomaly_prediction():
    """Send logs to trigger anomaly detection metrics"""
    try:
        # Send logs with high error rate to trigger anomaly
        logs = generate_logs(30, error_rate=0.3)
        response = requests.post(
            f"{BASE_URL}/api/v1/analyze/logs",
            json={"logs": logs},
            timeout=10
        )
        if response.status_code == 200:
            print(f"✓ Anomaly prediction triggered")
            return True
        else:
            print(f"✗ Anomaly prediction failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Anomaly prediction error: {e}")
        return False

def send_trace_analysis(traces_count=15, slow_rate=0.15):
    """Send trace analysis request"""
    try:
        traces = generate_traces(traces_count, slow_rate)
        response = requests.post(
            f"{BASE_URL}/api/v1/analyze/traces",
            json={"traces": traces},
            timeout=10
        )
        if response.status_code == 200:
            print(f"✓ Trace analysis: {traces_count} traces, slow_rate={slow_rate:.2f}")
            return True
        else:
            print(f"✗ Trace analysis failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Trace analysis error: {e}")
        return False

def send_commit_analysis():
    """Send commit analysis request"""
    try:
        repo = random.choice(["frontend", "backend", "api", "services", "infrastructure"])
        commit = f"abc{random.randint(1000, 9999)}"
        
        response = requests.post(
            f"{BASE_URL}/api/v1/analyze/commit",
            params={
                "repository": repo,
                "commit_hash": commit
            },
            timeout=10
        )
        if response.status_code == 200:
            print(f"✓ Commit analysis: {repo}/{commit}")
            return True
        else:
            print(f"✗ Commit analysis failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Commit analysis error: {e}")
        return False

def send_healing_request():
    """Send healing request"""
    try:
        issue = random.choice(ISSUE_TYPES)
        service = random.choice(SERVICES)
        
        response = requests.post(
            f"{BASE_URL}/api/v1/heal",
            json={
                "issue_type": issue,
                "context": {
                    "service": service,
                    "severity": random.choice(["low", "medium", "high"]),
                    "details": f"Detected {issue} in {service}"
                }
            },
            timeout=10
        )
        if response.status_code == 200:
            print(f"✓ Healing request: {issue} in {service}")
            return True
        else:
            print(f"✗ Healing request failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Healing request error: {e}")
        return False

def get_status_endpoints():
    """Call status endpoints to generate metrics"""
    endpoints = [
        "/api/v1/commit-status",
        "/api/v1/self-healing-status",
        "/api/v1/logs-status",
        "/api/v1/traces-status",
        "/api/v1/platform-overview",
        "/api/v1/recommendations"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"✓ Status check: {endpoint}")
            else:
                print(f"✗ Status check failed: {endpoint} - {response.status_code}")
        except Exception as e:
            print(f"✗ Status check error: {endpoint} - {e}")

def main():
    """Main function to populate Grafana with data"""
    print("=" * 60)
    print("Starting Grafana Data Population")
    print("=" * 60)
    print()
    
    # Check if service is running
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print("✗ Service is not healthy!")
            return
        print("✓ Service is healthy")
        print()
    except Exception as e:
        print(f"✗ Cannot connect to service: {e}")
        return
    
    total_requests = 0
    successful_requests = 0
    
    # Generate multiple rounds of data
    rounds = 50  # Number of rounds
    
    for round_num in range(1, rounds + 1):
        print(f"\n--- Round {round_num}/{rounds} ---")
        
        # Vary the error rates and patterns
        error_rate = random.uniform(0.05, 0.25)
        slow_rate = random.uniform(0.1, 0.3)
        logs_count = random.randint(15, 50)
        traces_count = random.randint(10, 30)
        
        # Send log analysis
        if send_log_analysis(logs_count, error_rate):
            successful_requests += 1
        total_requests += 1
        time.sleep(0.1)
        
        # Send trace analysis
        if send_trace_analysis(traces_count, slow_rate):
            successful_requests += 1
        total_requests += 1
        time.sleep(0.1)
        
        # Send commit analysis (less frequently)
        if round_num % 3 == 0:
            if send_commit_analysis():
                successful_requests += 1
            total_requests += 1
            time.sleep(0.1)
        
        # Send healing request (less frequently)
        if round_num % 5 == 0:
            if send_healing_request():
                successful_requests += 1
            total_requests += 1
            time.sleep(0.1)
        
        # Call status endpoints
        if round_num % 10 == 0:
            get_status_endpoints()
        
        # Small delay between rounds
        time.sleep(0.2)
    
    print()
    print("=" * 60)
    print("Data Population Complete!")
    print("=" * 60)
    print(f"Total requests: {total_requests}")
    print(f"Successful: {successful_requests}")
    print(f"Failed: {total_requests - successful_requests}")
    print(f"Success rate: {(successful_requests/total_requests*100):.1f}%")
    print()
    print("You can now check Grafana at: http://localhost:3000")
    print("Dashboard: Unified Platform Overview")
    print()

if __name__ == "__main__":
    main()
