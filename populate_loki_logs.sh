#!/bin/bash
##
# Script to populate Loki with logs directly
##

LOKI_URL="http://localhost:3100"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "============================================================"
echo "Starting Loki Log Population"
echo "============================================================"
echo ""

# Check if Loki is running
echo "Checking Loki status..."
loki_status=$(curl -s "$LOKI_URL/ready" 2>&1)
if [[ "$loki_status" =~ "ready" ]] || [[ "$loki_status" =~ "Ingester" ]]; then
    echo -e "${YELLOW}⚠ Loki is starting up, will attempt to push logs${NC}"
elif curl -s -f "$LOKI_URL/ready" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Loki is ready${NC}"
else
    echo -e "${YELLOW}⚠ Loki status unknown, will attempt to push logs anyway${NC}"
fi
echo ""

total_batches=0
successful_batches=0

# Services and messages
services=("api-gateway" "user-service" "data-collector" "intelligence-engine" "auth-service" "payment-service")
info_messages=("Request processed successfully" "Service started" "Health check passed" "Cache hit" "User logged in" "Data synced" "API call completed")
warning_messages=("Slow query detected" "High memory usage" "Rate limit approaching" "Cache miss" "Retry attempt" "Deprecated API used")
error_messages=("Database connection failed" "Authentication failed" "Timeout occurred" "Invalid input" "Permission denied" "Service unavailable" "Connection refused")

# Function to generate Loki-compatible timestamp (nanoseconds)
generate_timestamp_ns() {
    local offset_sec=$1
    local now=$(date -u +%s)
    local timestamp=$((now - offset_sec))
    echo "${timestamp}000000000"
}

# Function to push a batch of logs to Loki
push_logs_batch() {
    local batch_size=$1
    local error_rate=$2
    
    # Start building JSON
    local json='{"streams":['
    
    # Track streams by label combination
    declare -A stream_data
    
    for i in $(seq 1 $batch_size); do
        # Determine log level
        local rand=$((RANDOM % 100))
        if [ $rand -lt $((error_rate)) ]; then
            level="ERROR"
            message=${error_messages[$((RANDOM % ${#error_messages[@]}))]}
        elif [ $rand -lt 40 ]; then
            level="WARNING"
            message=${warning_messages[$((RANDOM % ${#warning_messages[@]}))]}
        elif [ $rand -lt 60 ]; then
            level="DEBUG"
            message="Processing data chunk"
        else
            level="INFO"
            message=${info_messages[$((RANDOM % ${#info_messages[@]}))]}
        fi
        
        # Select random service
        service=${services[$((RANDOM % ${#services[@]}))]}
        
        # Generate timestamp (random offset within last hour)
        timestamp=$(generate_timestamp_ns $((RANDOM % 3600)))
        
        # Create log line
        log_line=$(printf '{"message":"%s","service":"%s","level":"%s","request_id":"req-%04d","user_id":"user-%d"}' \
            "$message" "$service" "$level" $((RANDOM % 10000)) $((RANDOM % 100)))
        
        # Escape for JSON
        log_line=$(echo "$log_line" | sed 's/"/\\"/g')
        
        # Create label key
        label_key="${service}_${level}"
        
        # Add to stream data
        if [ -z "${stream_data[$label_key]}" ]; then
            stream_data[$label_key]='{"stream":{"job":"intelligent-platform","service":"'$service'","level":"'$level'"},"values":[["'$timestamp'","'$log_line'"]'
        else
            stream_data[$label_key]="${stream_data[$label_key]}"',["'$timestamp'","'$log_line'"]'
        fi
    done
    
    # Build final JSON from streams
    local first=true
    for key in "${!stream_data[@]}"; do
        if [ "$first" = true ]; then
            first=false
        else
            json="${json},"
        fi
        json="${json}${stream_data[$key]}]}"
    done
    
    json="${json}]}"
    
    # Push to Loki
    response=$(curl -s -w "\n%{http_code}" -X POST "$LOKI_URL/loki/api/v1/push" \
        -H "Content-Type: application/json" \
        -d "$json" 2>/dev/null)
    
    http_code=$(echo "$response" | tail -n1)
    
    if [ "$http_code" = "204" ]; then
        echo -e "${GREEN}✓ Pushed $batch_size logs to Loki${NC}"
        return 0
    else
        echo -e "${RED}✗ Failed to push logs: HTTP $http_code${NC}"
        return 1
    fi
}

# Main loop - generate batches of logs
rounds=30

for round in $(seq 1 $rounds); do
    echo -e "${YELLOW}--- Batch $round/$rounds ---${NC}"
    
    # Random batch size and error rate
    batch_size=$((RANDOM % 80 + 20))
    error_rate=$((RANDOM % 20 + 5))
    
    if push_logs_batch $batch_size $error_rate; then
        successful_batches=$((successful_batches + 1))
    fi
    total_batches=$((total_batches + 1))
    
    sleep 0.5
done

echo ""
echo "============================================================"
echo "Log Population Complete!"
echo "============================================================"
echo "Total batches: $total_batches"
echo "Successful: $successful_batches"
echo "Failed: $((total_batches - successful_batches))"
success_rate=$((successful_batches * 100 / total_batches))
echo "Success rate: ${success_rate}%"
echo ""
echo "Logs are now available in Loki!"
echo "You can query them in Grafana at: http://localhost:3000"
echo ""
