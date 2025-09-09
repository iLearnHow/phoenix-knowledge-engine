"""
Advanced Monitoring and Alert System for Phoenix Knowledge Engine
Tracks system health, costs, performance, and sends alerts
"""

import json
import os
import time
import smtplib
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import logging

class AlertLevel(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class AlertType(Enum):
    COST = "cost"
    PERFORMANCE = "performance"
    ERROR = "error"
    SYSTEM = "system"
    SECURITY = "security"

@dataclass
class Alert:
    """Represents a system alert"""
    id: str
    level: AlertLevel
    alert_type: AlertType
    title: str
    message: str
    timestamp: str
    resolved: bool = False
    resolved_at: Optional[str] = None
    metadata: Dict[str, Any] = None

class AlertChannel:
    """Base class for alert channels"""
    def send_alert(self, alert: Alert) -> bool:
        raise NotImplementedError

class EmailAlertChannel(AlertChannel):
    """Email alert channel"""
    
    def __init__(self, smtp_server: str, smtp_port: int, username: str, password: str, 
                 from_email: str, to_emails: List[str]):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.from_email = from_email
        self.to_emails = to_emails
    
    def send_alert(self, alert: Alert) -> bool:
        """Send alert via email"""
        try:
            subject = f"[{alert.level.value.upper()}] Phoenix Knowledge Engine: {alert.title}"
            body = f"""
Alert ID: {alert.id}
Level: {alert.level.value.upper()}
Type: {alert.alert_type.value}
Time: {alert.timestamp}

{alert.message}

Metadata: {json.dumps(alert.metadata or {}, indent=2)}
            """
            
            msg = f"Subject: {subject}\n\n{body}"
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.sendmail(self.from_email, self.to_emails, msg)
            
            return True
        except Exception as e:
            print(f"❌ Failed to send email alert: {e}")
            return False

class SlackAlertChannel(AlertChannel):
    """Slack alert channel"""
    
    def __init__(self, webhook_url: str, channel: str = "#alerts"):
        self.webhook_url = webhook_url
        self.channel = channel
    
    def send_alert(self, alert: Alert) -> bool:
        """Send alert via Slack"""
        try:
            color_map = {
                AlertLevel.INFO: "good",
                AlertLevel.WARNING: "warning",
                AlertLevel.ERROR: "danger",
                AlertLevel.CRITICAL: "danger"
            }
            
            payload = {
                "channel": self.channel,
                "attachments": [{
                    "color": color_map.get(alert.level, "good"),
                    "title": f"Phoenix Knowledge Engine Alert: {alert.title}",
                    "text": alert.message,
                    "fields": [
                        {"title": "Level", "value": alert.level.value.upper(), "short": True},
                        {"title": "Type", "value": alert.alert_type.value, "short": True},
                        {"title": "Time", "value": alert.timestamp, "short": True},
                        {"title": "Alert ID", "value": alert.id, "short": True}
                    ],
                    "footer": "Phoenix Knowledge Engine Monitoring",
                    "ts": int(time.time())
                }]
            }
            
            response = requests.post(self.webhook_url, json=payload)
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Failed to send Slack alert: {e}")
            return False

class WebhookAlertChannel(AlertChannel):
    """Generic webhook alert channel"""
    
    def __init__(self, webhook_url: str, headers: Dict[str, str] = None):
        self.webhook_url = webhook_url
        self.headers = headers or {"Content-Type": "application/json"}
    
    def send_alert(self, alert: Alert) -> bool:
        """Send alert via webhook"""
        try:
            payload = {
                "alert_id": alert.id,
                "level": alert.level.value,
                "type": alert.alert_type.value,
                "title": alert.title,
                "message": alert.message,
                "timestamp": alert.timestamp,
                "resolved": alert.resolved,
                "metadata": alert.metadata or {}
            }
            
            response = requests.post(self.webhook_url, json=payload, headers=self.headers)
            return response.status_code in [200, 201, 202]
        except Exception as e:
            print(f"❌ Failed to send webhook alert: {e}")
            return False

class MonitoringSystem:
    """Main monitoring and alerting system"""
    
    def __init__(self, config_file: str = "monitoring_config.json"):
        self.config_file = config_file
        self.alerts = []
        self.alert_channels = []
        self.metrics = {}
        self.thresholds = {}
        self.load_config()
        self.setup_logging()
    
    def load_config(self):
        """Load monitoring configuration"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                self.thresholds = config.get('thresholds', {})
                self.setup_alert_channels(config.get('alert_channels', {}))
        else:
            self._create_default_config()
    
    def _create_default_config(self):
        """Create default monitoring configuration"""
        default_config = {
            "thresholds": {
                "cost_daily_limit": 5.0,
                "cost_monthly_limit": 50.0,
                "cost_warning_percentage": 80,
                "response_time_limit": 5.0,
                "error_rate_limit": 5.0,
                "memory_usage_limit": 80.0,
                "cpu_usage_limit": 80.0
            },
            "alert_channels": {
                "email": {
                    "enabled": False,
                    "smtp_server": "smtp.gmail.com",
                    "smtp_port": 587,
                    "username": "",
                    "password": "",
                    "from_email": "",
                    "to_emails": []
                },
                "slack": {
                    "enabled": False,
                    "webhook_url": "",
                    "channel": "#alerts"
                },
                "webhook": {
                    "enabled": False,
                    "webhook_url": "",
                    "headers": {}
                }
            }
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(default_config, f, indent=2)
        
        self.thresholds = default_config["thresholds"]
    
    def setup_alert_channels(self, channels_config: Dict):
        """Setup alert channels based on configuration"""
        # Email channel
        if channels_config.get("email", {}).get("enabled", False):
            email_config = channels_config["email"]
            email_channel = EmailAlertChannel(
                smtp_server=email_config["smtp_server"],
                smtp_port=email_config["smtp_port"],
                username=email_config["username"],
                password=email_config["password"],
                from_email=email_config["from_email"],
                to_emails=email_config["to_emails"]
            )
            self.alert_channels.append(email_channel)
        
        # Slack channel
        if channels_config.get("slack", {}).get("enabled", False):
            slack_config = channels_config["slack"]
            slack_channel = SlackAlertChannel(
                webhook_url=slack_config["webhook_url"],
                channel=slack_config["channel"]
            )
            self.alert_channels.append(slack_channel)
        
        # Webhook channel
        if channels_config.get("webhook", {}).get("enabled", False):
            webhook_config = channels_config["webhook"]
            webhook_channel = WebhookAlertChannel(
                webhook_url=webhook_config["webhook_url"],
                headers=webhook_config.get("headers", {})
            )
            self.alert_channels.append(webhook_channel)
    
    def setup_logging(self):
        """Setup logging for monitoring"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('monitoring.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('PhoenixMonitoring')
    
    def create_alert(self, level: AlertLevel, alert_type: AlertType, title: str, 
                    message: str, metadata: Dict[str, Any] = None) -> Alert:
        """Create a new alert"""
        alert_id = f"alert_{int(time.time())}_{len(self.alerts)}"
        alert = Alert(
            id=alert_id,
            level=level,
            alert_type=alert_type,
            title=title,
            message=message,
            timestamp=datetime.now().isoformat(),
            metadata=metadata or {}
        )
        
        self.alerts.append(alert)
        self.logger.info(f"Created alert: {alert_id} - {title}")
        
        # Send alert through all channels
        for channel in self.alert_channels:
            try:
                channel.send_alert(alert)
            except Exception as e:
                self.logger.error(f"Failed to send alert through channel: {e}")
        
        return alert
    
    def check_cost_thresholds(self, current_cost: float, period: str = "daily"):
        """Check cost thresholds and create alerts if needed"""
        if period == "daily":
            limit = self.thresholds.get("cost_daily_limit", 5.0)
            warning_threshold = limit * (self.thresholds.get("cost_warning_percentage", 80) / 100)
        else:  # monthly
            limit = self.thresholds.get("cost_monthly_limit", 50.0)
            warning_threshold = limit * (self.thresholds.get("cost_warning_percentage", 80) / 100)
        
        if current_cost >= limit:
            self.create_alert(
                AlertLevel.CRITICAL,
                AlertType.COST,
                f"Cost Limit Exceeded - {period.title()}",
                f"Current {period} cost: ${current_cost:.2f} exceeds limit of ${limit:.2f}",
                {"current_cost": current_cost, "limit": limit, "period": period}
            )
        elif current_cost >= warning_threshold:
            self.create_alert(
                AlertLevel.WARNING,
                AlertType.COST,
                f"Cost Warning - {period.title()}",
                f"Current {period} cost: ${current_cost:.2f} is {current_cost/limit*100:.1f}% of limit",
                {"current_cost": current_cost, "limit": limit, "period": period}
            )
    
    def check_performance_metrics(self, response_time: float, error_rate: float, 
                                memory_usage: float, cpu_usage: float):
        """Check performance metrics and create alerts if needed"""
        # Response time check
        if response_time > self.thresholds.get("response_time_limit", 5.0):
            self.create_alert(
                AlertLevel.WARNING,
                AlertType.PERFORMANCE,
                "High Response Time",
                f"API response time: {response_time:.2f}s exceeds limit of {self.thresholds.get('response_time_limit', 5.0)}s",
                {"response_time": response_time, "limit": self.thresholds.get("response_time_limit", 5.0)}
            )
        
        # Error rate check
        if error_rate > self.thresholds.get("error_rate_limit", 5.0):
            self.create_alert(
                AlertLevel.ERROR,
                AlertType.ERROR,
                "High Error Rate",
                f"Error rate: {error_rate:.1f}% exceeds limit of {self.thresholds.get('error_rate_limit', 5.0)}%",
                {"error_rate": error_rate, "limit": self.thresholds.get("error_rate_limit", 5.0)}
            )
        
        # Memory usage check
        if memory_usage > self.thresholds.get("memory_usage_limit", 80.0):
            self.create_alert(
                AlertLevel.WARNING,
                AlertType.SYSTEM,
                "High Memory Usage",
                f"Memory usage: {memory_usage:.1f}% exceeds limit of {self.thresholds.get('memory_usage_limit', 80.0)}%",
                {"memory_usage": memory_usage, "limit": self.thresholds.get("memory_usage_limit", 80.0)}
            )
        
        # CPU usage check
        if cpu_usage > self.thresholds.get("cpu_usage_limit", 80.0):
            self.create_alert(
                AlertLevel.WARNING,
                AlertType.SYSTEM,
                "High CPU Usage",
                f"CPU usage: {cpu_usage:.1f}% exceeds limit of {self.thresholds.get('cpu_usage_limit', 80.0)}%",
                {"cpu_usage": cpu_usage, "limit": self.thresholds.get("cpu_usage_limit", 80.0)}
            )
    
    def track_api_call(self, model: str, input_tokens: int, output_tokens: int, 
                      response_time: float, success: bool):
        """Track an API call and update metrics"""
        # Update cost metrics
        cost = self._calculate_cost(model, input_tokens, output_tokens)
        self.metrics.setdefault("total_cost", 0)
        self.metrics["total_cost"] += cost
        
        # Update call metrics
        self.metrics.setdefault("total_calls", 0)
        self.metrics["total_calls"] += 1
        
        if success:
            self.metrics.setdefault("successful_calls", 0)
            self.metrics["successful_calls"] += 1
        else:
            self.metrics.setdefault("failed_calls", 0)
            self.metrics["failed_calls"] += 1
        
        # Update response time metrics
        self.metrics.setdefault("response_times", [])
        self.metrics["response_times"].append(response_time)
        
        # Keep only last 100 response times
        if len(self.metrics["response_times"]) > 100:
            self.metrics["response_times"] = self.metrics["response_times"][-100:]
        
        # Check thresholds
        self.check_cost_thresholds(self.metrics["total_cost"])
        
        # Calculate error rate
        total_calls = self.metrics["total_calls"]
        failed_calls = self.metrics.get("failed_calls", 0)
        error_rate = (failed_calls / total_calls) * 100 if total_calls > 0 else 0
        
        # Calculate average response time
        avg_response_time = sum(self.metrics["response_times"]) / len(self.metrics["response_times"]) if self.metrics["response_times"] else 0
        
        # Check performance thresholds
        self.check_performance_metrics(avg_response_time, error_rate, 0, 0)  # Memory and CPU would need system monitoring
    
    def _calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost for API call"""
        model_costs = {
            "gpt-3.5-turbo": {"input": 0.001, "output": 0.002},
            "gpt-4": {"input": 0.03, "output": 0.06},
            "gpt-4-turbo": {"input": 0.01, "output": 0.03}
        }
        
        if model not in model_costs:
            model = "gpt-3.5-turbo"  # Default to cheapest
        
        input_cost = (input_tokens / 1000) * model_costs[model]["input"]
        output_cost = (output_tokens / 1000) * model_costs[model]["output"]
        return input_cost + output_cost
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get current metrics summary"""
        total_calls = self.metrics.get("total_calls", 0)
        successful_calls = self.metrics.get("successful_calls", 0)
        failed_calls = self.metrics.get("failed_calls", 0)
        
        return {
            "total_cost": self.metrics.get("total_cost", 0),
            "total_calls": total_calls,
            "successful_calls": successful_calls,
            "failed_calls": failed_calls,
            "success_rate": (successful_calls / total_calls * 100) if total_calls > 0 else 0,
            "error_rate": (failed_calls / total_calls * 100) if total_calls > 0 else 0,
            "average_response_time": sum(self.metrics.get("response_times", [])) / len(self.metrics.get("response_times", [1])) if self.metrics.get("response_times") else 0,
            "active_alerts": len([a for a in self.alerts if not a.resolved]),
            "total_alerts": len(self.alerts)
        }
    
    def get_alerts(self, level: AlertLevel = None, resolved: bool = None) -> List[Alert]:
        """Get alerts with optional filtering"""
        filtered_alerts = self.alerts
        
        if level:
            filtered_alerts = [a for a in filtered_alerts if a.level == level]
        
        if resolved is not None:
            filtered_alerts = [a for a in filtered_alerts if a.resolved == resolved]
        
        return filtered_alerts
    
    def resolve_alert(self, alert_id: str) -> bool:
        """Resolve an alert"""
        for alert in self.alerts:
            if alert.id == alert_id:
                alert.resolved = True
                alert.resolved_at = datetime.now().isoformat()
                self.logger.info(f"Resolved alert: {alert_id}")
                return True
        
        return False
    
    def export_alerts(self, filename: str = None) -> str:
        """Export alerts to a file"""
        if not filename:
            filename = f"alerts_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        alerts_data = []
        for alert in self.alerts:
            alerts_data.append({
                "id": alert.id,
                "level": alert.level.value,
                "alert_type": alert.alert_type.value,
                "title": alert.title,
                "message": alert.message,
                "timestamp": alert.timestamp,
                "resolved": alert.resolved,
                "resolved_at": alert.resolved_at,
                "metadata": alert.metadata
            })
        
        with open(filename, 'w') as f:
            json.dump(alerts_data, f, indent=2)
        
        print(f"✅ Exported {len(alerts_data)} alerts to {filename}")
        return filename

# Example usage and testing
if __name__ == "__main__":
    # Create monitoring system
    monitoring = MonitoringSystem()
    
    # Simulate some API calls
    monitoring.track_api_call("gpt-3.5-turbo", 100, 50, 1.2, True)
    monitoring.track_api_call("gpt-3.5-turbo", 200, 100, 2.1, True)
    monitoring.track_api_call("gpt-3.5-turbo", 150, 75, 0.8, False)
    
    # Get metrics summary
    summary = monitoring.get_metrics_summary()
    print("Metrics Summary:", json.dumps(summary, indent=2))
    
    # Get active alerts
    active_alerts = monitoring.get_alerts(resolved=False)
    print(f"\nActive Alerts: {len(active_alerts)}")
    
    # Export alerts
    monitoring.export_alerts()
