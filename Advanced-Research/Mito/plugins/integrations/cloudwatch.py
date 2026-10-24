"""
CloudWatch Plugin
AWS CloudWatch metrics and logs.
"""
import logging
from typing import Any, Dict, List

logger = logging.getLogger("mito.plugins.cloudwatch")

try:
    import boto3
    BOTO_AVAILABLE = True
except ImportError:
    BOTO_AVAILABLE = False


def _cw(region: str = "us-east-1"):
    if not BOTO_AVAILABLE:
        raise ImportError("boto3 not installed. Run: pip install boto3")
    return boto3.client("cloudwatch", region_name=region)


def cloudwatch_metric_cmd(namespace: str = "AWS/EC2", metric: str = "CPUUtilization",
                           stat: str = "Average", period: int = 300, region: str = "us-east-1") -> Dict:
    c = _cw(region)
    response = c.get_metric_statistics(
        Namespace=namespace, MetricName=metric,
        Period=period, Statistics=[stat],
        StartTime=__import__("datetime").datetime.utcnow() - __import__("datetime").timedelta(hours=1),
        EndTime=__import__("datetime").datetime.utcnow(),
    )
    return {"namespace": namespace, "metric": metric, "stat": stat, "datapoints": response.get("Datapoints", [])}


def cloudwatch_alarm_cmd(alarm: str = "", region: str = "us-east-1") -> Dict:
    c = _cw(region)
    response = c.describe_alarms(AlarmNames=[alarm]) if alarm else c.describe_alarms()
    return {"alarms": response.get("MetricAlarms", []), "count": len(response.get("MetricAlarms", []))}


def cloudwatch_logs_cmd(log_group: str = "", filter_pattern: str = "", limit: int = 100,
                         region: str = "us-east-1") -> List[Dict]:
    c = _cw(region)
    kwargs = {"logGroupName": log_group}
    if filter_pattern:
        kwargs["filterPattern"] = filter_pattern
    else:
        kwargs["logStreamName"] = log_group.split("/")[-1] if "/" in log_group else log_group
    if filter_pattern:
        response = c.filter_log_events(**kwargs, limit=limit)
        events = response.get("events", [])
    else:
        response = c.get_log_events(**{k: v for k, v in kwargs.items() if k != "filterPattern"}, limit=limit)
        events = response.get("events", [])
    return {"log_group": log_group, "events": events, "count": len(events)}


def cloudwatch_put_metric_cmd(namespace: str = "Mito", metric: str = "", value: float = 1.0,
                               unit: str = "Count", region: str = "us-east-1") -> Dict:
    c = _cw(region)
    c.put_metric_data(Namespace=namespace, MetricData=[{"MetricName": metric, "Value": value, "Unit": unit}])
    return {"status": "ok", "namespace": namespace, "metric": metric, "value": value}


def cloudwatch_dashboard_cmd(dashboard: str = "", region: str = "us-east-1") -> Dict:
    c = _cw(region)
    if dashboard:
        response = c.get_dashboard(DashboardName=dashboard)
    else:
        response = c.list_dashboards()
    return dict(response)


def register(plugin):
    plugin.register_command("metric", cloudwatch_metric_cmd)
    plugin.register_command("alarm", cloudwatch_alarm_cmd)
    plugin.register_command("logs", cloudwatch_logs_cmd)
    plugin.register_command("put_metric", cloudwatch_put_metric_cmd)
    plugin.register_command("dashboard", cloudwatch_dashboard_cmd)


PLUGIN_METADATA = {
    "name": "cloudwatch", "version": "1.0.0",
    "description": "AWS CloudWatch metrics, alarms, and log management",
    "author": "Mito Team", "license": "MIT",
    "tags": ["aws", "monitoring", "cloudwatch", "metrics"],
    "dependencies": ["boto3"], "permissions": ["cloudwatch_write"],
    "min_mito_version": "1.0.1",
}

cloudwatch_plugin = {"metadata": PLUGIN_METADATA, "register": register}
