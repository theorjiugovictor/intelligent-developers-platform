"""
Data Collector Service
Collects commits, logs, metrics, and traces from various sources
"""
import asyncio
import logging
import os
from datetime import datetime
from typing import Dict, Any, List
import httpx
from pythonjsonlogger import jsonlogger

# Setup logging
logger = logging.getLogger(__name__)
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

# Configuration
LOKI_URL = os.getenv('LOKI_URL', 'http://loki:3100')
MIMIR_URL = os.getenv('MIMIR_URL', 'http://mimir:9009')
TEMPO_URL = os.getenv('TEMPO_URL', 'http://tempo:3200')
INTELLIGENCE_ENGINE_URL = os.getenv('INTELLIGENCE_ENGINE_URL', 'http://intelligence-engine:8000')

class DataCollector:
    """Collects data from various sources"""

    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
        self.running = False

    async def start(self):
        """Start collecting data"""
        self.running = True
        logger.info("Data Collector started")

        # Run collection tasks
        await asyncio.gather(
            self.collect_git_data(),
            self.collect_logs(),
            self.collect_metrics(),
            self.collect_traces(),
        )

    async def collect_git_data(self):
        """Collect Git commit data"""
        while self.running:
            try:
                logger.info("Collecting Git data...")

                # In production, this would monitor Git repositories
                # For demo, send sample data to intelligence engine
                sample_commit = {
                    'repository': 'example-repo',
                    'commit_hash': 'abc123',
                    'message': 'Update API endpoints',
                    'files_changed': ['api/users.py', 'api/auth.py'],
                    'lines_added': 50,
                    'lines_deleted': 20,
                    'files_changed_count': 2
                }

                # Send to intelligence engine
                await self.send_to_intelligence_engine(
                    '/api/v1/analyze/commit',
                    sample_commit
                )

                # Wait before next collection
                await asyncio.sleep(300)  # 5 minutes

            except Exception as e:
                logger.error(f"Error collecting Git data: {e}")
                await asyncio.sleep(60)

    async def collect_logs(self):
        """Collect and forward logs"""
        while self.running:
            try:
                logger.info("Collecting logs from Loki...")

                # Query Loki for recent logs
                response = await self.client.get(
                    f"{LOKI_URL}/loki/api/v1/query_range",
                    params={
                        'query': '{job=~".+"}',
                        'limit': 1000
                    }
                )

                if response.status_code == 200:
                    data = response.json()
                    logs = self._parse_loki_response(data)

                    if logs:
                        # Send to intelligence engine for analysis
                        await self.send_to_intelligence_engine(
                            '/api/v1/analyze/logs',
                            {'logs': logs}
                        )

                await asyncio.sleep(60)  # 1 minute

            except Exception as e:
                logger.error(f"Error collecting logs: {e}")
                await asyncio.sleep(60)

    async def collect_metrics(self):
        """Collect metrics"""
        while self.running:
            try:
                logger.info("Collecting metrics...")

                # In production, collect from Mimir/Prometheus
                # For now, log the activity

                await asyncio.sleep(60)  # 1 minute

            except Exception as e:
                logger.error(f"Error collecting metrics: {e}")
                await asyncio.sleep(60)

    async def collect_traces(self):
        """Collect distributed traces"""
        while self.running:
            try:
                logger.info("Collecting traces from Tempo...")

                # In production, query Tempo for traces
                # For now, send sample data
                sample_traces = [
                    {
                        'trace_id': 'trace-123',
                        'service_name': 'api-gateway',
                        'operation_name': 'GET /api/users',
                        'duration_ms': 1500,
                        'error': False,
                        'timestamp': datetime.utcnow().isoformat()
                    }
                ]

                # Send to intelligence engine
                await self.send_to_intelligence_engine(
                    '/api/v1/analyze/traces',
                    {'traces': sample_traces}
                )

                await asyncio.sleep(60)  # 1 minute

            except Exception as e:
                logger.error(f"Error collecting traces: {e}")
                await asyncio.sleep(60)

    async def send_to_intelligence_engine(self, endpoint: str, data: Dict[str, Any]):
        """Send data to intelligence engine"""
        try:
            url = f"{INTELLIGENCE_ENGINE_URL}{endpoint}"
            response = await self.client.post(url, json=data)

            if response.status_code == 200:
                logger.info(f"Data sent to intelligence engine: {endpoint}")
            else:
                logger.error(f"Error sending data: {response.status_code}")

        except Exception as e:
            logger.error(f"Error sending to intelligence engine: {e}")

    def _parse_loki_response(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse Loki response"""
        logs = []

        try:
            for stream in data.get('data', {}).get('result', []):
                labels = stream.get('stream', {})

                for value in stream.get('values', []):
                    logs.append({
                        'timestamp': value[0],
                        'message': value[1],
                        'labels': labels,
                        'level': labels.get('level', 'info')
                    })
        except Exception as e:
            logger.error(f"Error parsing Loki response: {e}")

        return logs

    async def stop(self):
        """Stop collecting data"""
        self.running = False
        await self.client.aclose()
        logger.info("Data Collector stopped")

async def main():
    """Main entry point"""
    collector = DataCollector()

    try:
        await collector.start()
    except KeyboardInterrupt:
        logger.info("Received shutdown signal")
    finally:
        await collector.stop()

if __name__ == "__main__":
    asyncio.run(main())

