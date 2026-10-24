"""
Real-time Monitoring Dashboard
Tracks ethical compliance, performance metrics, alignment drift, and user interactions.
Complete audit trail for every decision.
"""

import logging
from typing import Dict, List, Any
from datetime import datetime, timedelta
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class SystemMetric:
    """A single system metric entry"""
    timestamp: str
    metric_name: str
    value: float
    threshold: Optional[float] = None
    status: str = "normal"  # normal, warning, critical


class MonitoringDashboard:
    """
    Real-time system monitoring and audit trail.
    Collects metrics from all subsystems and provides compliance reporting.
    """
    
    def __init__(self):
        self.metrics: List[SystemMetric] = []
        self.audit_trail: List[Dict] = []
        self.alerts: List[Dict] = []
        self.start_time = datetime.now()
        logger.info("Monitoring Dashboard initialized")
    
    def record_metric(self, metric_name: str, value: float, threshold: Optional[float] = None) -> None:
        """Record a system metric"""
        status = "normal"
        if threshold and value > threshold:
            status = "warning"
        if threshold and value > threshold * 1.5:
            status = "critical"
        
        metric = SystemMetric(
            timestamp=datetime.now().isoformat(),
            metric_name=metric_name,
            value=value,
            threshold=threshold,
            status=status
        )
        
        self.metrics.append(metric)
        
        if status != "normal":
            self._create_alert(metric_name, value, threshold, status)
    
    def _create_alert(self, metric_name: str, value: float, threshold: float, status: str) -> None:
        """Create alert for concerning metric"""
        alert = {
            'timestamp': datetime.now().isoformat(),
            'metric': metric_name,
            'value': value,
            'threshold': threshold,
            'status': status,
            'message': f"{metric_name} exceeds threshold: {value:.2f} (threshold: {threshold:.2f})"
        }
        self.alerts.append(alert)
        logger.warning(f"ALERT: {alert['message']}")
    
    def log_decision(self, decision_id: str, decision_data: Dict) -> None:
        """Log a system decision for audit"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'decision_id': decision_id,
            'data': decision_data,
            'audit_hash': self._generate_audit_hash(decision_data)
        }
        self.audit_trail.append(entry)
    
    def _generate_audit_hash(self, data: Dict) -> str:
        """Generate immutable hash of decision for audit integrity"""
        import hashlib
        import json
        data_str = json.dumps(data, sort_keys=True, default=str)
        return hashlib.sha256(data_str.encode()).hexdigest()[:16]
    
    def get_compliance_report(self) -> Dict:
        """Generate comprehensive compliance report"""
        uptime_seconds = (datetime.now() - self.start_time).total_seconds()
        uptime_hours = uptime_seconds / 3600
        
        critical_alerts = len([a for a in self.alerts if a['status'] == 'critical'])
        warning_alerts = len([a for a in self.alerts if a['status'] == 'warning'])
        
        return {
            'reporting_period': {
                'start': self.start_time.isoformat(),
                'end': datetime.now().isoformat(),
                'duration_hours': uptime_hours
            },
            'metrics': {
                'total_recorded': len(self.metrics),
                'critical_alerts': critical_alerts,
                'warning_alerts': warning_alerts,
                'audit_trail_entries': len(self.audit_trail)
            },
            'compliance_status': 'compliant' if critical_alerts == 0 else 'non_compliant',
            'recent_alerts': self.alerts[-5:] if self.alerts else []
        }
    
    def get_audit_trail(self, decision_id: Optional[str] = None) -> List[Dict]:
        """Retrieve audit trail entries"""
        if decision_id:
            return [e for e in self.audit_trail if e['decision_id'] == decision_id]
        return self.audit_trail.copy()
    
    def generate_compliance_certificate(self) -> Dict:
        """Generate compliance certificate for governance review"""
        report = self.get_compliance_report()
        
        return {
            'certificate_timestamp': datetime.now().isoformat(),
            'system': 'NBOS_v1.0',
            'compliance_status': report['compliance_status'],
            'audit_entries': len(self.audit_trail),
            'critical_incidents': report['metrics']['critical_alerts'],
            'certifier_signature': self._generate_audit_hash(report)
        }
