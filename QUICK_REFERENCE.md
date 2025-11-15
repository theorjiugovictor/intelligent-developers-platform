# Quick Reference Card

## 🚀 Quick Start

```bash
# Clone and navigate
cd intelligent-developers-platform

# Start everything (with fixes applied)
./fix-and-start.sh

# Or use make
make start
```

## 📊 Access URLs

| Service | URL | Credentials |
|---------|-----|-------------|
| Grafana | http://localhost:3000 | admin / admin |
| Intelligence Engine | http://localhost:8000 | - |
| API Docs | http://localhost:8000/docs | - |
| Prometheus | http://localhost:9090 | - |
| Loki | http://localhost:3100 | - |
| Mimir | http://localhost:9009 | - |
| Tempo | http://localhost:3200 | - |

## 🛠️ Common Commands

```bash
# Start services
docker-compose up -d
./start.sh
make start

# Stop services
docker-compose down
./stop.sh
make stop

# Restart services
docker-compose restart
make restart

# View logs (all)
docker-compose logs -f
make logs

# View logs (specific service)
docker-compose logs -f intelligence-engine
make logs-engine

# Check status
docker-compose ps
make status

# Health checks
curl http://localhost:8000/health
curl http://localhost:3000/api/health
make test

# Rebuild services
docker-compose build
make build

# Complete cleanup
docker-compose down -v
make clean

# Fix and restart
./fix-and-start.sh
```

## 🔍 Debugging

```bash
# Check if service is running
docker-compose ps <service-name>

# View real-time logs
docker-compose logs -f <service-name>

# Enter container
docker-compose exec <service-name> /bin/bash

# Check network connectivity
docker-compose exec intelligence-engine ping loki

# View container resource usage
docker stats
```

## 📝 Key Files

| File | Purpose |
|------|---------|
| `docker-compose.yml` | Main services configuration |
| `README.md` | Complete documentation |
| `TROUBLESHOOTING.md` | Common issues and solutions |
| `FIXES_APPLIED.md` | Issues fixed and how |
| `Makefile` | Convenient commands |
| `start.sh` | Quick start script |
| `stop.sh` | Quick stop script |
| `fix-and-start.sh` | Fix issues and start |

## 🧪 Testing the Platform

### 1. Test Breaking Change Detection
```bash
curl -X POST http://localhost:8000/api/v1/analyze/commit \
  -H "Content-Type: application/json" \
  -d '{
    "repository": "my-app",
    "commit_hash": "abc123"
  }'
```

### 2. Get Recommendations
```bash
curl http://localhost:8000/api/v1/recommendations?limit=5
```

### 3. Trigger Self-Healing
```bash
curl -X POST http://localhost:8000/api/v1/heal \
  -H "Content-Type: application/json" \
  -d '{
    "issue_type": "high_memory",
    "context": {"service": "api-gateway"}
  }'
```

## ⚡ Service Dependencies

```
Grafana → Mimir, Loki, Tempo
Intelligence Engine → PostgreSQL, Redis, Loki, Mimir, Tempo
Data Collector → Intelligence Engine, Loki, Mimir, Tempo
Prometheus → Mimir
```

## 📊 Grafana Dashboards

1. **IDP Overview** - Main dashboard with all metrics
2. **Code Quality & Predictions** - Breaking change predictions
3. **Self-Healing & Optimization** - Healing actions and recommendations
4. **Performance Analytics & Traces** - Service performance and traces

## 🔧 Configuration Files

| Service | Config File |
|---------|-------------|
| Mimir | `mimir/config.yaml` |
| Loki | `loki/config.yaml` |
| Tempo | `tempo/config.yaml` |
| Prometheus | `prometheus/prometheus.yml` |
| Grafana Datasources | `grafana/provisioning/datasources/` |
| Grafana Dashboards | `grafana/provisioning/dashboards/` |

## 🚨 Common Issues

| Issue | Solution |
|-------|----------|
| Service won't start | `docker-compose restart <service>` |
| Port already in use | Change port in `docker-compose.yml` |
| Out of memory | Increase Docker memory allocation |
| Connection refused | Wait 60s for services to fully start |
| Config error | Check YAML syntax and indentation |

## 💡 Tips

- Wait ~60 seconds after startup for all services to be ready
- Check logs first when troubleshooting: `docker-compose logs -f`
- Use `make help` to see all available make commands
- Grafana datasources are auto-provisioned on first start
- Models directory is created automatically
- Default retention: Logs 168h, Metrics 15d, Traces 168h

## 📚 Documentation

- Full documentation: `README.md`
- Troubleshooting: `TROUBLESHOOTING.md`
- What was fixed: `FIXES_APPLIED.md`
- API documentation: http://localhost:8000/docs (when running)

## 🎯 System Requirements

- Docker Engine 20.10+
- Docker Compose 2.0+
- 8GB+ RAM
- 20GB+ disk space
- macOS, Linux, or Windows with WSL2

## 📞 Getting Help

1. Check `TROUBLESHOOTING.md`
2. Run `make test` for health checks
3. View logs: `make logs`
4. Check service status: `make status`
5. Review `FIXES_APPLIED.md` for known issues

