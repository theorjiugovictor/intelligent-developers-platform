#!/bin/bash
##
# Script to populate Grafana by making many requests to the Intelligence Engine API.
# This generates metrics, logs, and traces that will be visualized in the dashboard.
##

BASE_URL="http://localhost:8000"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "============================================================"
echo "Starting Grafana Data Population"
echo "============================================================"
echo ""

# Check if service is running
echo "Checking service health..."
if curl -s -f "$BASE_URL/health" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Service is healthy${NC}"
else
    echo -e "${RED}✗ Service is not running!${NC}"
    exit 1
fi
echo ""

total_requests=0
successful_requests=0

# Function to generate random log data
generate_logs() {
    local count=$1
    local error_rate=$2
    
    local logs="["
    for i in $(seq 1 $count); do
        # Random log level
        local rand=$((RANDOM % 100))
        if [ $rand -lt $((error_rate * 100)) ]; then
            level="ERROR"
            message="Database connection failed"
        elif [ $rand -lt 40 ]; then
            level="WARNING"
            message="Slow query detected"
        elif [ $rand -lt 60 ]; then
            level="DEBUG"
            message="Processing data chunk"
        else
            level="INFO"
            message="Request processed successfully"
        fi
        
        # Random service
        services=("api-gateway" "user-service" "data-collector" "intelligence-engine" "auth-service" "payment-service")
        service=${services[$((RANDOM % 6))]}
        
        # Random timestamp (within last hour)
        timestamp=$(date -u -v-$((RANDOM % 60))M +"%Y-%m-%dT%H:%M:%S.000Z" 2>/dev/null || date -u --date="-$((RANDOM % 60)) minutes" +"%Y-%m-%dT%H:%M:%S.000Z" 2>/dev/null || date -u +"%Y-%m-%dT%H:%M:%S.000Z")
        
        if [ $i -gt 1 ]; then
            logs+=","
        fi
        logs+="{\"timestamp\":\"$timestamp\",\"level\":\"$level\",\"message\":\"$message\",\"service\":\"$service\",\"metadata\":{\"request_id\":\"req-$((RANDOM % 9000 + 1000))\"}}"
    done
    logs+="]"
    
    echo "$logs"
}

# Function to generate random trace data
generate_traces() {
    local count=$1
    local slow_rate=$2
    
    local traces="["
    for i in $(seq 1 $count); do
        # Random service
        services=("api-gateway" "user-service" "data-collector" "intelligence-engine" "auth-service" "payment-service")
        service=${services[$((RANDOM % 6))]}
        
        # Random operation
        operations=("http.request" "database.query" "cache.get" "api.call" "auth.validate" "data.process")
        operation=${operations[$((RANDOM % 6))]}
        
        # Duration (slow or normal)
        local rand=$((RANDOM % 100))
        if [ $rand -lt $((slow_rate * 100)) ]; then
            duration=$((RANDOM % 2500 + 500))
        else
            duration=$((RANDOM % 190 + 10))
        fi
        
        # Random timestamp
        timestamp=$(date -u -v-$((RANDOM % 60))M +"%Y-%m-%dT%H:%M:%S.000Z" 2>/dev/null || date -u --date="-$((RANDOM % 60)) minutes" +"%Y-%m-%dT%H:%M:%S.000Z" 2>/dev/null || date -u +"%Y-%m-%dT%H:%M:%S.000Z")
        
        if [ $i -gt 1 ]; then
            traces+=","
        fi
        traces+="{\"trace_id\":\"trace-$((RANDOM % 90000 + 10000))\",\"span_id\":\"span-$((RANDOM % 9000 + 1000))\",\"service\":\"$service\",\"operation\":\"$operation\",\"duration_ms\":$duration,\"timestamp\":\"$timestamp\",\"metadata\":{\"http_status\":200}}"
    done
    traces+="]"
    
    echo "$traces"
}

# Main loop
rounds=50

for round in $(seq 1 $rounds); do
    echo -e "${YELLOW}--- Round $round/$rounds ---${NC}"
    
    # Random parameters
    logs_count=$((RANDOM % 36 + 15))
    traces_count=$((RANDOM % 21 + 10))
    error_rate=0.$((RANDOM % 20 + 5))
    slow_rate=0.$((RANDOM % 20 + 10))
    
    # Send log analysis
    logs=$(generate_logs $logs_count 15)
    response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/v1/analyze/logs" \
        -H "Content-Type: application/json" \
        -d "{\"logs\": $logs}" 2>/dev/null)
    http_code=$(echo "$response" | tail -n1)
    
    total_requests=$((total_requests + 1))
    if [ "$http_code" = "200" ]; then
        echo -e "${GREEN}✓ Log analysis: $logs_count logs${NC}"
        successful_requests=$((successful_requests + 1))
    else
        echo -e "${RED}✗ Log analysis failed: $http_code${NC}"
    fi
    sleep 0.1
    
    # Send trace analysis
    traces=$(generate_traces $traces_count 15)
    response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/v1/analyze/traces" \
        -H "Content-Type: application/json" \
        -d "{\"traces\": $traces}" 2>/dev/null)
    http_code=$(echo "$response" | tail -n1)
    
    total_requests=$((total_requests + 1))
    if [ "$http_code" = "200" ]; then
        echo -e "${GREEN}✓ Trace analysis: $traces_count traces${NC}"
        successful_requests=$((successful_requests + 1))
    else
        echo -e "${RED}✗ Trace analysis failed: $http_code${NC}"
    fi
    sleep 0.1
    
    # Send commit analysis (every 3 rounds)
    if [ $((round % 3)) -eq 0 ]; then
        repos=("frontend" "backend" "api" "services" "infrastructure")
        repo=${repos[$((RANDOM % 5))]}
        commit="abc$((RANDOM % 9000 + 1000))"
        
        response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/v1/analyze/commit?repository=$repo&commit_hash=$commit" 2>/dev/null)
        http_code=$(echo "$response" | tail -n1)
        
        total_requests=$((total_requests + 1))
        if [ "$http_code" = "200" ]; then
            echo -e "${GREEN}✓ Commit analysis: $repo/$commit${NC}"
            successful_requests=$((successful_requests + 1))
        else
            echo -e "${RED}✗ Commit analysis failed: $http_code${NC}"
        fi
        sleep 0.1
    fi
    
    # Send healing request (every 5 rounds)
    if [ $((round % 5)) -eq 0 ]; then
        issues=("memory_leak" "slow_query" "connection_timeout" "high_cpu" "disk_space")
        issue=${issues[$((RANDOM % 5))]}
        services=("api-gateway" "user-service" "data-collector" "intelligence-engine")
        service_name=${services[$((RANDOM % 4))]}
        
        response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/v1/heal" \
            -H "Content-Type: application/json" \
            -d "{\"issue_type\":\"$issue\",\"context\":{\"service\":\"$service_name\",\"severity\":\"medium\"}}" 2>/dev/null)
        http_code=$(echo "$response" | tail -n1)
        
        total_requests=$((total_requests + 1))
        if [ "$http_code" = "200" ]; then
            echo -e "${GREEN}✓ Healing request: $issue in $service_name${NC}"
            successful_requests=$((successful_requests + 1))
        else
            echo -e "${RED}✗ Healing request failed: $http_code${NC}"
        fi
        sleep 0.1
    fi
    
    # Call status endpoints (every 10 rounds)
    if [ $((round % 10)) -eq 0 ]; then
        echo -e "${YELLOW}Calling status endpoints...${NC}"
        curl -s "$BASE_URL/api/v1/commit-status" > /dev/null
        curl -s "$BASE_URL/api/v1/self-healing-status" > /dev/null
        curl -s "$BASE_URL/api/v1/logs-status" > /dev/null
        curl -s "$BASE_URL/api/v1/traces-status" > /dev/null
        curl -s "$BASE_URL/api/v1/platform-overview" > /dev/null
        echo -e "${GREEN}✓ Status endpoints called${NC}"
    fi
    
    sleep 0.2
done

echo ""
echo "============================================================"
echo "Data Population Complete!"
echo "============================================================"
echo "Total requests: $total_requests"
echo "Successful: $successful_requests"
echo "Failed: $((total_requests - successful_requests))"
success_rate=$((successful_requests * 100 / total_requests))
echo "Success rate: ${success_rate}%"
echo ""
echo "You can now check Grafana at: http://localhost:3000"
echo "Dashboard: Unified Platform Overview"
echo ""
