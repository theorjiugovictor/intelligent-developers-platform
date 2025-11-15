#!/usr/bin/env python3
"""
Script to populate Loki with logs directly.
This generates realistic log data for the observability platform.
"""
import requests
import random
import time
from datetime import datetime, timedelta, timezone
import json

LOKI_URL = "http://localhost:3100"

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
        "API call completed",
        "Database connection established",
        "Transaction committed",
        "Background job completed"
    ],
    "WARNING": [
        "Slow query detected",
        "High memory usage",
        "Rate limit approaching",
        "Cache miss",
        "Retry attempt",
        "Deprecated API used",
        "Connection pool exhausted",
        "Disk space low",
        "CPU usage elevated"
    ],
    "ERROR": [
        "Database connection failed",
        "Authentication failed",
        "Timeout occurred",
        "Invalid input",
        "Permission denied",
        "Service unavailable",
        "Connection refused",
        "Out of memory",
        "Failed to process request",
        "Unexpected error occurred"
    ],
    "DEBUG": [
        "Variable value: 42",
        "Function called",
        "Loop iteration",
        "Processing data chunk",
        "Cache lookup",
        "Validating input"
    ]
}

def generate_timestamp_ns(offset_minutes=0):
    """Generate timestamp in nanoseconds"""
    dt = datetime.now(timezone.utc) - timedelta(minutes=offset_minutes)
    return str(int(dt.timestamp() * 1e9))

def push_logs_to_loki(count=20, error_rate=0.1):
    """Push logs directly to Loki"""
    try:
        streams = {}
        
        # Generate logs
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
            timestamp_ns = generate_timestamp_ns(random.randint(0, 60))
            
            # Create label key for grouping
            label_key = f'{{"job":"intelligent-platform","service":"{service}","level":"{level}"}}'
            
            # Initialize stream if not exists
            if label_key not in streams:
                streams[label_key] = {
                    "stream": {
                        "job": "intelligent-platform",
                        "service": service,
                        "level": level
                    },
                    "values": []
                }
            
            # Add log entry
            log_line = json.dumps({
                "message": message,
                "service": service,
                "level": level,
                "request_id": f"req-{random.randint(1000, 9999)}",
                "user_id": f"user-{random.randint(1, 100)}"
            })
            
            streams[label_key]["values"].append([timestamp_ns, log_line])
        
        # Convert to Loki format
        loki_payload = {
            "streams": list(streams.values())
        }
        
        # Push to Loki
        response = requests.post(
            f"{LOKI_URL}/loki/api/v1/push",
            json=loki_payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 204:
            print(f"✓ Pushed {count} logs to Loki (error_rate={error_rate:.2f})")
            return True
        else:
            print(f"✗ Failed to push logs to Loki: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Error pushing logs to Loki: {e}")
        return False

def main():
    """Main function to populate Loki with logs"""
    print("=" * 60)
    print("Starting Loki Log Population")
    print("=" * 60)
    print()
    
    # Check if Loki is running
    try:
        response = requests.get(f"{LOKI_URL}/ready", timeout=5)
        if response.status_code == 200:
            print("✓ Loki is ready")
            print()
        else:
            print(f"✗ Loki is not ready: {response.status_code}")
            return
    except Exception as e:
        print(f"✗ Cannot connect to Loki: {e}")
        return
    
    total_batches = 0
    successful_batches = 0
    
    # Generate multiple batches of logs
    rounds = 30  # Number of batches
    
    for round_num in range(1, rounds + 1):
        print(f"--- Batch {round_num}/{rounds} ---")
        
        # Vary the error rates and log counts
        error_rate = random.uniform(0.05, 0.25)
        log_count = random.randint(20, 100)
        
        # Push logs to Loki
        if push_logs_to_loki(log_count, error_rate):
            successful_batches += 1
        total_batches += 1
        
        # Small delay between batches
        time.sleep(0.5)
    
    print()
    print("=" * 60)
    print("Log Population Complete!")
    print("=" * 60)
    print(f"Total batches: {total_batches}")
    print(f"Successful: {successful_batches}")
    print(f"Failed: {total_batches - successful_batches}")
    print(f"Success rate: {(successful_batches/total_batches*100):.1f}%")
    print()
    print("Logs are now available in Loki!")
    print("You can query them in Grafana at: http://localhost:3000")
    print()

if __name__ == "__main__":
    main()
