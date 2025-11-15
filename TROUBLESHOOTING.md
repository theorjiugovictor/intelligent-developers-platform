# Troubleshooting Guide

## Common Issues and Solutions

### 1. Intelligence Engine Fails to Start

**Error**: `ERROR: Attribute "app" not found in module "main"`

**Solution**:
- Ensure all `__init__.py` files exist in subdirectories
- Rebuild the container:
```bash
docker-compose down
docker-compose build intelligence-engine
docker-compose up -d
```

### 2. Loki Config Error

**Error**: `yaml: line 2: mapping values are not allowed in this context`

**Solution**:
- Check YAML indentation in `loki/config.yaml`
- Ensure all YAML keys are properly formatted
- Restart Loki:
```bash
docker-compose restart loki
```

### 3. Mimir Config Error

**Error**: `error loading config from /etc/mimir/config.yaml: EOF`

**Solution**:
- Verify `mimir/config.yaml` is not empty
- Check file permissions
- Recreate the config file if corrupted

### 4. Tempo Permission Denied

**Error**: `mkdir /tmp/tempo/blocks: permission denied`

**Solution**:
- Tempo now runs as root in docker-compose
- If issue persists, manually create directory:
```bash
docker-compose down
docker volume rm intelligent-developers-platform_tempo-data
docker-compose up -d tempo
```

### 5. Data Collector Connection Errors

**Error**: `Error sending to intelligence engine: All connection attempts failed`

**Solution**:
- Wait for intelligence engine to fully start (can take 30-60 seconds)
- Check if intelligence engine is running:
```bash
docker-compose logs intelligence-engine
curl http://localhost:8000/health
```

### 6. PostgreSQL Connection Issues

**Solution**:
```bash
# Check PostgreSQL logs
docker-compose logs postgres

# Restart PostgreSQL
docker-compose restart postgres

# Connect to PostgreSQL directly
docker-compose exec postgres psql -U idp_user -d idp_intelligence
```

### 7. Grafana Data Source Issues

**Solution**:
1. Login to Grafana (http://localhost:3000)
2. Go to Configuration → Data Sources
3. Verify all data sources are connected:
   - Mimir (http://mimir:9009/prometheus)
   - Loki (http://loki:3100)
   - Tempo (http://tempo:3200)

### 8. Services Not Starting

**Check Docker Resources**:
- Ensure Docker has at least 8GB RAM allocated
- Check disk space: `df -h`
- Verify Docker is running: `docker info`

**Complete Reset**:
```bash
# Stop all services
docker-compose down -v

# Remove all volumes
docker volume prune -f

# Start fresh
docker-compose up -d
```

### 9. Slow Performance

**Solutions**:
- Increase Docker memory allocation
- Reduce log retention periods in Loki config
- Limit metrics cardinality in Mimir
- Reduce trace sampling rate in Tempo

### 10. Port Conflicts

**Error**: `port is already allocated`

**Solution**:
```bash
# Find process using the port (example: 3000)
lsof -i :3000

# Kill the process or change port in docker-compose.yml
# Example: Change Grafana port
# ports:
#   - "3001:3000"
```

## Debugging Commands

### View All Logs
```bash
docker-compose logs -f
```

### View Specific Service Logs
```bash
docker-compose logs -f intelligence-engine
docker-compose logs -f data-collector
docker-compose logs -f grafana
docker-compose logs -f loki
docker-compose logs -f mimir
docker-compose logs -f tempo
```

### Check Service Status
```bash
docker-compose ps
```

### Restart Specific Service
```bash
docker-compose restart <service-name>
```

### Rebuild Service
```bash
docker-compose build <service-name>
docker-compose up -d <service-name>
```

### Enter Container Shell
```bash
docker-compose exec intelligence-engine /bin/bash
docker-compose exec data-collector /bin/bash
```

### Check Network Connectivity
```bash
# From intelligence-engine to postgres
docker-compose exec intelligence-engine ping postgres

# From intelligence-engine to loki
docker-compose exec intelligence-engine ping loki
```

## Health Check URLs

- Grafana: http://localhost:3000/api/health
- Intelligence Engine: http://localhost:8000/health
- Prometheus: http://localhost:9090/-/healthy
- Mimir: http://localhost:9009/ready
- Loki: http://localhost:3100/ready
- Tempo: http://localhost:3200/ready

## Getting Help

1. Check the logs first: `docker-compose logs -f`
2. Verify all services are running: `docker-compose ps`
3. Run health checks: `make test`
4. Check individual service documentation
5. File an issue with:
   - Full error logs
   - Docker version: `docker --version`
   - Docker Compose version: `docker-compose --version`
   - OS and version
   - Steps to reproduce

## Performance Tuning

### For Low Memory Systems (<8GB)

Edit `docker-compose.yml` and add resource limits:
```yaml
services:
  intelligence-engine:
    deploy:
      resources:
        limits:
          memory: 1G
```

### For Production Deployments

1. Use external databases (managed PostgreSQL)
2. Configure persistent volumes with proper backup
3. Enable TLS for all services
4. Implement proper authentication
5. Set up monitoring and alerting
6. Configure log rotation
7. Use managed observability services

