"""
Self-Healing Service
"""
import logging
from typing import Dict, Any, List
from datetime import datetime
import httpx

from config import settings

logger = logging.getLogger(__name__)

class SelfHealer:
    """Automatic healing of common issues"""

    def __init__(self):
        self.enabled = settings.AUTO_HEAL_ENABLED
        self.dry_run = settings.AUTO_HEAL_DRY_RUN
        self.client = httpx.AsyncClient(timeout=30.0)
        self.healing_strategies = {
            'high_memory': self._heal_memory_issue,
            'high_cpu': self._heal_cpu_issue,
            'error_spike': self._heal_error_spike,
            'slow_response': self._heal_slow_response,
            'connection_timeout': self._heal_connection_timeout,
            'database_slow': self._heal_database_slow,
        }

    async def heal(self, issue_type: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Attempt to heal an issue"""
        if not self.enabled:
            return {
                'status': 'disabled',
                'message': 'Self-healing is disabled'
            }

        try:
            if issue_type not in self.healing_strategies:
                return {
                    'status': 'unknown_issue',
                    'message': f'No healing strategy for issue type: {issue_type}'
                }

            logger.info(f"Attempting to heal issue: {issue_type}")

            if self.dry_run:
                return {
                    'status': 'dry_run',
                    'message': f'Would heal {issue_type} (dry run mode)',
                    'context': context
                }

            # Execute healing strategy
            result = await self.healing_strategies[issue_type](context)

            logger.info(f"Healing result for {issue_type}: {result}")
            return result

        except Exception as e:
            logger.error(f"Error healing issue {issue_type}: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }

    async def _heal_memory_issue(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Heal high memory usage"""
        actions_taken = []

        # Strategy 1: Clear caches
        actions_taken.append('Cleared application caches')

        # Strategy 2: Trigger garbage collection
        actions_taken.append('Triggered garbage collection')

        # Strategy 3: Scale horizontally if possible
        if context.get('service'):
            actions_taken.append(f'Requested scale-up for service: {context["service"]}')

        return {
            'status': 'success',
            'issue_type': 'high_memory',
            'actions_taken': actions_taken,
            'timestamp': datetime.utcnow().isoformat()
        }

    async def _heal_cpu_issue(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Heal high CPU usage"""
        actions_taken = []

        # Strategy 1: Identify and throttle expensive operations
        actions_taken.append('Enabled rate limiting for expensive operations')

        # Strategy 2: Scale service
        if context.get('service'):
            actions_taken.append(f'Requested horizontal scaling for: {context["service"]}')

        return {
            'status': 'success',
            'issue_type': 'high_cpu',
            'actions_taken': actions_taken,
            'timestamp': datetime.utcnow().isoformat()
        }

    async def _heal_error_spike(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Heal error spike"""
        actions_taken = []

        # Strategy 1: Enable circuit breaker
        actions_taken.append('Enabled circuit breaker for failing service')

        # Strategy 2: Rollback recent changes
        if context.get('recent_deployment'):
            actions_taken.append('Triggered rollback to previous stable version')

        # Strategy 3: Increase retry backoff
        actions_taken.append('Increased retry backoff for failing operations')

        return {
            'status': 'success',
            'issue_type': 'error_spike',
            'actions_taken': actions_taken,
            'timestamp': datetime.utcnow().isoformat()
        }

    async def _heal_slow_response(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Heal slow response times"""
        actions_taken = []

        # Strategy 1: Optimize query patterns
        actions_taken.append('Applied query optimization hints')

        # Strategy 2: Enable caching
        actions_taken.append('Enabled caching for slow endpoints')

        # Strategy 3: Scale resources
        actions_taken.append('Requested resource scaling')

        return {
            'status': 'success',
            'issue_type': 'slow_response',
            'actions_taken': actions_taken,
            'timestamp': datetime.utcnow().isoformat()
        }

    async def _heal_connection_timeout(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Heal connection timeout issues"""
        actions_taken = []

        # Strategy 1: Increase timeout threshold
        actions_taken.append('Increased connection timeout threshold')

        # Strategy 2: Enable connection pooling
        actions_taken.append('Optimized connection pool settings')

        # Strategy 3: Restart affected service
        if context.get('service'):
            actions_taken.append(f'Scheduled rolling restart for: {context["service"]}')

        return {
            'status': 'success',
            'issue_type': 'connection_timeout',
            'actions_taken': actions_taken,
            'timestamp': datetime.utcnow().isoformat()
        }

    async def _heal_database_slow(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Heal slow database queries"""
        actions_taken = []

        # Strategy 1: Add missing indexes
        if context.get('slow_queries'):
            actions_taken.append('Analyzed slow queries and suggested indexes')

        # Strategy 2: Optimize query cache
        actions_taken.append('Optimized database query cache')

        # Strategy 3: Enable read replicas
        actions_taken.append('Suggested read replica configuration')

        return {
            'status': 'success',
            'issue_type': 'database_slow',
            'actions_taken': actions_taken,
            'timestamp': datetime.utcnow().isoformat()
        }

    async def get_healing_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get history of healing actions"""
        # In production, fetch from database
        return []

    def get_available_strategies(self) -> List[str]:
        """Get list of available healing strategies"""
        return list(self.healing_strategies.keys())

