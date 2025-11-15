# Intelligent Development Platform (IDP)

An intelligent internal development platform that learns from the historical lifecycle of your software product. It analyzes commits, changes, logs, metrics, and traces to provide predictive insights instead of reactive responses.

## 🚀 Features

### 🧠 Intelligent Prediction
- **Breaking Change Detection**: AI-powered analysis of code commits to predict breaking changes before they happen
- **Anomaly Detection**: Automatically identifies unusual patterns in logs and metrics
- **Performance Prediction**: Forecasts performance degradation based on historical trends

### 🔄 Self-Healing
- Automatically fixes common issues like high memory usage, CPU spikes, and connection timeouts
- Implements circuit breakers and rollback strategies
- Optimizes database queries and caching strategies

### 📊 Comprehensive Observability
- **Grafana**: Advanced visualization and dashboards
- **Mimir**: Long-term metrics storage with unlimited cardinality
- **Loki**: Log aggregation and analysis
- **Tempo**: Distributed tracing for microservices

### 🎯 Optimization Recommendations
- AI-generated recommendations for performance, security, and cost optimization
- Auto-fixable suggestions with one-click implementation
- Impact estimation for each recommendation

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Grafana                               │
│              (Visualization & Interaction)                   │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐   ┌───────▼────────┐   ┌───────▼────────┐
│     Mimir      │   │      Loki      │   │     Tempo      │
│   (Metrics)    │   │     (Logs)     │   │   (Traces)     │
└───────┬────────┘   └───────┬────────┘   └───────┬────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                   ┌──────────▼───────────┐
                   │  Intelligence Engine  │
                   │    (AI/ML Core)       │
                   └──────────┬───────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐   ┌───────▼────────┐   ┌───────▼────────┐
│ Breaking Change│   │    Anomaly     │   │  Performance   │
│   Detector     │   │    Detector    │   │   Predictor    │
└────────────────┘   └────────────────┘   └────────────────┘
                              │
                   ┌──────────▼───────────┐
                   │    Self-Healer       │
                   │    Optimizer         │
                   └──────────────────────┘
```

## 🛠️ Tech Stack

- **Grafana**: Visualization and interaction layer
- **Mimir**: Metrics storage (Prometheus-compatible)
- **Loki**: Log aggregation and querying
- **Tempo**: Distributed tracing backend
- **Python/FastAPI**: Intelligence Engine backend
- **PostgreSQL**: Historical data and ML model storage
- **Redis**: Real-time caching
- **scikit-learn, XGBoost**: Machine learning models
- **Docker**: Containerization

## 📦 Quick Start

### Prerequisites

- Docker & Docker Compose
- 8GB+ RAM recommended
- 20GB+ disk space

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd intelligent-developers-platform
```

2. Start the platform:
```bash
docker-compose up -d
```

3. Wait for services to be ready (2-3 minutes):
```bash
docker-compose logs -f
```

4. Access the platform:
- Grafana: http://localhost:3000 (admin/admin)
- Intelligence Engine API: http://localhost:8000
- Prometheus: http://localhost:9090

### First Steps

1. **Access Grafana Dashboards**:
   - Navigate to http://localhost:3000
   - Login with `admin/admin`
   - Explore pre-configured dashboards:
     - IDP Overview
     - Code Quality & Predictions
     - Self-Healing & Optimization
     - Performance Analytics & Traces

2. **API Documentation**:
   - Visit http://localhost:8000/docs for interactive API documentation

3. **Test Breaking Change Detection**:
```bash
curl -X POST http://localhost:8000/api/v1/analyze/commit \
  -H "Content-Type: application/json" \
  -d '{
    "repository": "my-repo",
    "commit_hash": "abc123"
  }'
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Database
DATABASE_URL=postgresql://idp_user:idp_pass@postgres:5432/idp_intelligence

# Redis
REDIS_URL=redis://redis:6379

# Observability
LOKI_URL=http://loki:3100
MIMIR_URL=http://mimir:9009
TEMPO_URL=http://tempo:3200

# Intelligence Engine
BREAKING_CHANGE_THRESHOLD=0.7
ANOMALY_THRESHOLD=0.8
AUTO_HEAL_ENABLED=true
AUTO_HEAL_DRY_RUN=false
```

## 📖 Usage Examples

### Analyze a Commit

```python
import httpx

response = httpx.post(
    "http://localhost:8000/api/v1/analyze/commit",
    json={
        "repository": "my-app",
        "commit_hash": "def456",
        "message": "Remove deprecated API endpoints",
        "files_changed": ["api/v1/users.py", "api/v1/auth.py"],
        "lines_added": 20,
        "lines_deleted": 150
    }
)

result = response.json()
if result['is_breaking_change']:
    print(f"⚠️ Breaking change detected with {result['confidence']*100}% confidence")
    print(f"Reasons: {result['reasons']}")
    print(f"Recommendations: {result['recommendations']}")
```

### Query Logs for Anomalies

```python
response = httpx.post(
    "http://localhost:8000/api/v1/analyze/logs",
    json={
        "logs": [
            {"timestamp": "2024-01-01T10:00:00Z", "level": "error", "message": "Connection timeout"},
            {"timestamp": "2024-01-01T10:00:01Z", "level": "error", "message": "Connection timeout"},
            # ... more logs
        ]
    }
)

result = response.json()
print(f"Anomalies detected: {result['anomalies']}")
```

### Get Optimization Recommendations

```python
response = httpx.get(
    "http://localhost:8000/api/v1/recommendations",
    params={"severity": "high", "limit": 5}
)

recommendations = response.json()
for rec in recommendations:
    print(f"{rec['title']}: {rec['description']}")
    print(f"Estimated impact: {rec['estimated_impact']*100}%")
```

### Trigger Self-Healing

```python
response = httpx.post(
    "http://localhost:8000/api/v1/heal",
    json={
        "issue_type": "high_memory",
        "context": {"service": "api-gateway", "memory_usage": 0.95}
    }
)

result = response.json()
print(f"Healing status: {result['status']}")
print(f"Actions taken: {result['actions_taken']}")
```

## 🧪 ML Models

### Breaking Change Detector
- **Algorithm**: XGBoost Classifier
- **Features**: Code metrics, file patterns, commit messages
- **Accuracy**: ~85%
- **Retraining**: Every 24 hours on new data

### Anomaly Detector
- **Algorithm**: Isolation Forest
- **Features**: Log patterns, error rates, metric distributions
- **Accuracy**: ~90%
- **Detection**: Real-time

### Performance Predictor
- **Algorithm**: Random Forest Regressor
- **Features**: Historical latency, resource usage, traffic patterns
- **Accuracy**: ~82%
- **Prediction Window**: 1-6 hours ahead

## 📊 Dashboards

### 1. IDP Overview
- Breaking change detection rate
- Total breaking changes detected
- Anomaly detection trends
- Self-healing actions
- Error logs
- API response times

### 2. Code Quality & Predictions
- Recent breaking change predictions
- Prediction confidence distribution
- Prediction types distribution
- Intelligence engine logs

### 3. Self-Healing & Optimization
- Healing actions over time
- Successful healing actions
- Active optimization recommendations
- System health score

### 4. Performance Analytics & Traces
- Service latency percentiles (p50, p95, p99)
- Service dependency map
- Slowest traces
- Performance bottlenecks
- Error rate by service

## 🔐 Security

- All credentials should be changed in production
- Use secrets management (e.g., HashiCorp Vault)
- Enable TLS for all communications
- Implement RBAC for Grafana
- Regular security audits and dependency updates

## 🚀 Production Deployment

### Kubernetes

```bash
# Convert docker-compose to Kubernetes
kompose convert

# Apply to cluster
kubectl apply -f .
```

### Scaling

- Horizontal scaling for Intelligence Engine
- Mimir, Loki, Tempo support clustering
- PostgreSQL with read replicas
- Redis Cluster for high availability

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

MIT License - see LICENSE file for details

## 🆘 Support

- Documentation: [Wiki](wiki)
- Issues: [GitHub Issues](issues)
- Discussions: [GitHub Discussions](discussions)

## 🗺️ Roadmap

- [ ] Integration with GitHub/GitLab webhooks
- [ ] Slack/Teams notifications for predictions
- [ ] Advanced ML models (LSTM for time series)
- [ ] Cost optimization recommendations
- [ ] Automatic PR comments for breaking changes
- [ ] Mobile app for alerts
- [ ] Multi-cloud support
- [ ] Custom ML model training UI

## 📈 Metrics & KPIs

The platform tracks:
- Breaking changes prevented
- Issues auto-healed
- Performance improvements
- Cost savings
- MTTR (Mean Time To Recovery)
- Deployment frequency
- Change failure rate
- Lead time for changes

---

**Built with ❤️ for intelligent development**

