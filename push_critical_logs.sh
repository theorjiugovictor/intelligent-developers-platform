#!/bin/bash
##
# Quick script to push ERROR and INFO logs to Loki
##

LOKI_URL="http://localhost:3100"

echo "Pushing ERROR, CRITICAL, and INFO logs to Loki..."

# Get current timestamp in nanoseconds
get_timestamp() {
    echo "$(date +%s)000000000"
}

# Push ERROR logs
echo "Pushing ERROR logs..."
curl -s -X POST "$LOKI_URL/loki/api/v1/push" \
  -H "Content-Type: application/json" \
  -d '{
    "streams": [
      {
        "stream": {
          "job": "intelligent-platform",
          "service": "intelligence-engine",
          "level": "ERROR"
        },
        "values": [
          ["'$(get_timestamp)'", "{\"message\":\"Database connection failed\",\"service\":\"intelligence-engine\",\"level\":\"ERROR\"}"],
          ["'$(get_timestamp)'", "{\"message\":\"Authentication failed\",\"service\":\"api-gateway\",\"level\":\"ERROR\"}"],
          ["'$(get_timestamp)'", "{\"message\":\"Timeout occurred\",\"service\":\"user-service\",\"level\":\"ERROR\"}"],
          ["'$(get_timestamp)'", "{\"message\":\"Service unavailable\",\"service\":\"data-collector\",\"level\":\"ERROR\"}"]
        ]
      }
    ]
  }' && echo "✓ ERROR logs pushed"

# Push CRITICAL logs
echo "Pushing CRITICAL logs..."
curl -s -X POST "$LOKI_URL/loki/api/v1/push" \
  -H "Content-Type: application/json" \
  -d '{
    "streams": [
      {
        "stream": {
          "job": "intelligent-platform",
          "service": "intelligence-engine",
          "level": "CRITICAL"
        },
        "values": [
          ["'$(get_timestamp)'", "{\"message\":\"System failure detected\",\"service\":\"intelligence-engine\",\"level\":\"CRITICAL\"}"],
          ["'$(get_timestamp)'", "{\"message\":\"Data corruption detected\",\"service\":\"data-collector\",\"level\":\"CRITICAL\"}"]
        ]
      }
    ]
  }' && echo "✓ CRITICAL logs pushed"

# Push INFO logs
echo "Pushing INFO logs..."
curl -s -X POST "$LOKI_URL/loki/api/v1/push" \
  -H "Content-Type: application/json" \
  -d '{
    "streams": [
      {
        "stream": {
          "job": "intelligent-platform",
          "service": "intelligence-engine",
          "level": "INFO"
        },
        "values": [
          ["'$(get_timestamp)'", "{\"message\":\"Request processed successfully\",\"service\":\"intelligence-engine\",\"level\":\"INFO\"}"],
          ["'$(get_timestamp)'", "{\"message\":\"Service started\",\"service\":\"api-gateway\",\"level\":\"INFO\"}"],
          ["'$(get_timestamp)'", "{\"message\":\"Health check passed\",\"service\":\"user-service\",\"level\":\"INFO\"}"],
          ["'$(get_timestamp)'", "{\"message\":\"Cache hit\",\"service\":\"data-collector\",\"level\":\"INFO\"}"],
          ["'$(get_timestamp)'", "{\"message\":\"User logged in\",\"service\":\"auth-service\",\"level\":\"INFO\"}"],
          ["'$(get_timestamp)'", "{\"message\":\"Data synced\",\"service\":\"data-collector\",\"level\":\"INFO\"}"]
        ]
      }
    ]
  }' && echo "✓ INFO logs pushed"

echo ""
echo "✅ All log levels pushed successfully!"
echo "You should now be able to see logs in Grafana dashboard"
