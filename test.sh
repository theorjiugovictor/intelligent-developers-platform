#!/bin/bash
BASE_URL="http://localhost:8000"

echo "🎯 Testing GOOD States (Healthy System)"
echo "========================================"

echo "✅ Good Logs..."
curl -s -X POST $BASE_URL/api/v1/analyze/logs \
  -H "Content-Type: application/json" \
  -d '{"logs":[{"timestamp":"2025-11-15T14:00:00Z","level":"INFO","message":"All good","service":"api"}]}'

echo "✅ Good Performance..."
curl -s -X POST $BASE_URL/api/v1/analyze/traces \
  -H "Content-Type: application/json" \
  -d '{"traces":[{"trace_id":"t1","span_id":"s1","service":"api","operation":"GET /","duration_ms":45.2,"timestamp":"2025-11-15T14:00:00Z"}]}'

echo "✅ Successful Healing..."
curl -s -X POST $BASE_URL/api/v1/heal \
  -H "Content-Type: application/json" \
  -d '{"issue_type":"optimization","context":{"service":"api","severity":"low"}}'

echo ""
echo "⏱️  Wait 5 seconds, then check dashboard..."
sleep 5

echo ""
echo "🔥 Testing BAD States (System Issues)"
echo "========================================"

echo "❌ Critical Errors..."
curl -s -X POST $BASE_URL/api/v1/analyze/logs \
  -H "Content-Type: application/json" \
  -d '{"logs":[{"timestamp":"2025-11-15T14:00:00Z","level":"ERROR","message":"DB down","service":"db"},{"timestamp":"2025-11-15T14:01:00Z","level":"ERROR","message":"API crash","service":"api"},{"timestamp":"2025-11-15T14:02:00Z","level":"CRITICAL","message":"Out of memory","service":"worker"}]}'

echo "❌ Performance Issues..."
curl -s -X POST $BASE_URL/api/v1/analyze/traces \
  -H "Content-Type: application/json" \
  -d '{"traces":[{"trace_id":"t1","span_id":"s1","service":"db","operation":"SELECT","duration_ms":8456.2,"timestamp":"2025-11-15T14:00:00Z"},{"trace_id":"t2","span_id":"s2","service":"api","operation":"GET","duration_ms":5234.8,"timestamp":"2025-11-15T14:01:00Z"}]}'

echo "❌ Critical Healing Required..."
curl -s -X POST $BASE_URL/api/v1/heal \
  -H "Content-Type: application/json" \
  -d '{"issue_type":"memory_leak_critical","context":{"service":"worker","severity":"critical","memory_percent":98}}'

echo ""
echo "✅ Done! Check dashboard at: http://localhost:8000/main"
echo "🔄 Click refresh buttons or wait for auto-refresh"
