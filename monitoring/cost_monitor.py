"""
Cost Monitoring System
Tracks API usage and costs for budget protection
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List
from pathlib import Path

logger = logging.getLogger('phoenix.monitoring.cost')


class CostMonitor:
    """
    Monitors API usage and costs to prevent budget overruns.
    """
    
    def __init__(self, budget_file: str = "budget_tracking.json"):
        self.budget_file = Path(budget_file)
        self.budget_data = self._load_budget_data()
        
        # Cost limits (configurable)
        self.daily_limit = 5.0  # $5 per day
        self.monthly_limit = 50.0  # $50 per month
        self.model_costs = {
            "gpt-3.5-turbo": {"input": 0.001, "output": 0.002},  # per 1K tokens
            "gpt-4": {"input": 0.03, "output": 0.06},
            "gpt-4-turbo": {"input": 0.01, "output": 0.03}
        }
    
    def _load_budget_data(self) -> Dict[str, Any]:
        """Load budget tracking data from file"""
        if self.budget_file.exists():
            try:
                with open(self.budget_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading budget data: {e}")
        
        # Initialize with default data
        return {
            "daily_usage": {},
            "monthly_usage": {},
            "total_spent": 0.0,
            "last_reset": datetime.now().isoformat()
        }
    
    def _save_budget_data(self):
        """Save budget tracking data to file"""
        try:
            with open(self.budget_file, 'w') as f:
                json.dump(self.budget_data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving budget data: {e}")
    
    def track_api_call(self, 
                      model: str, 
                      input_tokens: int, 
                      output_tokens: int,
                      operation: str = "unknown") -> Dict[str, Any]:
        """
        Track an API call and calculate cost.
        Returns cost information and budget status.
        """
        # Calculate cost
        if model not in self.model_costs:
            logger.warning(f"Unknown model: {model}, using gpt-3.5-turbo costs")
            model = "gpt-3.5-turbo"
        
        input_cost = (input_tokens / 1000) * self.model_costs[model]["input"]
        output_cost = (output_tokens / 1000) * self.model_costs[model]["output"]
        total_cost = input_cost + output_cost
        
        # Update tracking data
        today = datetime.now().strftime("%Y-%m-%d")
        this_month = datetime.now().strftime("%Y-%m")
        
        # Daily tracking
        if today not in self.budget_data["daily_usage"]:
            self.budget_data["daily_usage"][today] = {"cost": 0.0, "calls": 0, "operations": {}}
        
        self.budget_data["daily_usage"][today]["cost"] += total_cost
        self.budget_data["daily_usage"][today]["calls"] += 1
        
        if operation not in self.budget_data["daily_usage"][today]["operations"]:
            self.budget_data["daily_usage"][today]["operations"][operation] = 0
        self.budget_data["daily_usage"][today]["operations"][operation] += 1
        
        # Monthly tracking
        if this_month not in self.budget_data["monthly_usage"]:
            self.budget_data["monthly_usage"][this_month] = {"cost": 0.0, "calls": 0}
        
        self.budget_data["monthly_usage"][this_month]["cost"] += total_cost
        self.budget_data["monthly_usage"][this_month]["calls"] += 1
        
        # Total spent
        self.budget_data["total_spent"] += total_cost
        
        # Save data
        self._save_budget_data()
        
        # Check budget status
        budget_status = self._check_budget_status()
        
        return {
            "cost": total_cost,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "model": model,
            "operation": operation,
            "budget_status": budget_status,
            "daily_remaining": max(0, self.daily_limit - self.budget_data["daily_usage"][today]["cost"]),
            "monthly_remaining": max(0, self.monthly_limit - self.budget_data["monthly_usage"][this_month]["cost"])
        }
    
    def _check_budget_status(self) -> Dict[str, Any]:
        """Check current budget status and return warnings if needed"""
        today = datetime.now().strftime("%Y-%m-%d")
        this_month = datetime.now().strftime("%Y-%m")
        
        daily_cost = self.budget_data["daily_usage"].get(today, {}).get("cost", 0.0)
        monthly_cost = self.budget_data["monthly_usage"].get(this_month, {}).get("cost", 0.0)
        
        status = {
            "daily_limit_exceeded": daily_cost > self.daily_limit,
            "monthly_limit_exceeded": monthly_cost > self.monthly_limit,
            "daily_warning": daily_cost > (self.daily_limit * 0.8),  # 80% warning
            "monthly_warning": monthly_cost > (self.monthly_limit * 0.8),  # 80% warning
            "daily_cost": daily_cost,
            "monthly_cost": monthly_cost,
            "daily_limit": self.daily_limit,
            "monthly_limit": self.monthly_limit
        }
        
        # Log warnings
        if status["daily_limit_exceeded"]:
            logger.warning(f"Daily budget exceeded: ${daily_cost:.2f} / ${self.daily_limit}")
        elif status["daily_warning"]:
            logger.warning(f"Daily budget warning: ${daily_cost:.2f} / ${self.daily_limit}")
        
        if status["monthly_limit_exceeded"]:
            logger.warning(f"Monthly budget exceeded: ${monthly_cost:.2f} / ${self.monthly_limit}")
        elif status["monthly_warning"]:
            logger.warning(f"Monthly budget warning: ${monthly_cost:.2f} / ${self.monthly_limit}")
        
        return status
    
    def get_usage_summary(self, days: int = 7) -> Dict[str, Any]:
        """Get usage summary for the last N days"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        summary = {
            "period": f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
            "total_cost": 0.0,
            "total_calls": 0,
            "daily_breakdown": [],
            "operations": {},
            "models_used": set()
        }
        
        for i in range(days):
            date = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
            if date in self.budget_data["daily_usage"]:
                day_data = self.budget_data["daily_usage"][date]
                summary["total_cost"] += day_data["cost"]
                summary["total_calls"] += day_data["calls"]
                
                summary["daily_breakdown"].append({
                    "date": date,
                    "cost": day_data["cost"],
                    "calls": day_data["calls"]
                })
                
                # Track operations
                for operation, count in day_data.get("operations", {}).items():
                    if operation not in summary["operations"]:
                        summary["operations"][operation] = 0
                    summary["operations"][operation] += count
        
        return summary
    
    def reset_daily_budget(self):
        """Reset daily budget (call this daily)"""
        today = datetime.now().strftime("%Y-%m-%d")
        if today in self.budget_data["daily_usage"]:
            del self.budget_data["daily_usage"][today]
        self.budget_data["last_reset"] = datetime.now().isoformat()
        self._save_budget_data()
        logger.info("Daily budget reset")
    
    def set_budget_limits(self, daily_limit: float, monthly_limit: float):
        """Set new budget limits"""
        self.daily_limit = daily_limit
        self.monthly_limit = monthly_limit
        logger.info(f"Budget limits updated: Daily ${daily_limit}, Monthly ${monthly_limit}")


# Global instance
cost_monitor = CostMonitor()
