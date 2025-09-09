#!/usr/bin/env python3
"""
Budget Monitoring System
Tracks OpenAI API usage and costs in real-time
"""

import os
import json
import time
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

class BudgetMonitor:
    """Monitor OpenAI API usage and costs"""
    
    def __init__(self, budget_file: str = "budget_tracking.json"):
        self.budget_file = budget_file
        self.daily_limit = 5.0  # $5 daily limit
        self.monthly_limit = 50.0  # $50 monthly limit
        self.load_budget_data()
    
    def load_budget_data(self):
        """Load existing budget data"""
        if os.path.exists(self.budget_file):
            with open(self.budget_file, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = {
                "daily_usage": {},
                "monthly_usage": {},
                "total_spent": 0.0,
                "alerts_sent": [],
                "settings": {
                    "daily_limit": self.daily_limit,
                    "monthly_limit": self.monthly_limit,
                    "alert_threshold": 0.8  # Alert at 80% of limit
                }
            }
    
    def save_budget_data(self):
        """Save budget data to file"""
        with open(self.budget_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def track_usage(self, tokens: int, model: str = "gpt-4-turbo") -> Dict[str, Any]:
        """Track API usage and calculate costs"""
        
        # Model pricing (per 1K tokens)
        pricing = {
            "gpt-4": {"input": 0.03, "output": 0.06},
            "gpt-4-turbo": {"input": 0.01, "output": 0.03},
            "gpt-3.5-turbo": {"input": 0.001, "output": 0.002}
        }
        
        # Estimate input/output split (roughly 40% input, 60% output)
        input_tokens = int(tokens * 0.4)
        output_tokens = int(tokens * 0.6)
        
        # Calculate cost
        model_pricing = pricing.get(model, pricing["gpt-4-turbo"])
        cost = (input_tokens * model_pricing["input"] + output_tokens * model_pricing["output"]) / 1000
        
        # Get current date
        today = datetime.now().strftime("%Y-%m-%d")
        current_month = datetime.now().strftime("%Y-%m")
        
        # Update daily usage
        if today not in self.data["daily_usage"]:
            self.data["daily_usage"][today] = {"tokens": 0, "cost": 0.0, "calls": 0}
        
        self.data["daily_usage"][today]["tokens"] += tokens
        self.data["daily_usage"][today]["cost"] += cost
        self.data["daily_usage"][today]["calls"] += 1
        
        # Update monthly usage
        if current_month not in self.data["monthly_usage"]:
            self.data["monthly_usage"][current_month] = {"tokens": 0, "cost": 0.0, "calls": 0}
        
        self.data["monthly_usage"][current_month]["tokens"] += tokens
        self.data["monthly_usage"][current_month]["cost"] += cost
        self.data["monthly_usage"][current_month]["calls"] += 1
        
        # Update total spent
        self.data["total_spent"] += cost
        
        # Check limits and send alerts
        self.check_limits(today, current_month)
        
        # Save data
        self.save_budget_data()
        
        return {
            "tokens": tokens,
            "cost": cost,
            "daily_cost": self.data["daily_usage"][today]["cost"],
            "monthly_cost": self.data["monthly_usage"][current_month]["cost"],
            "total_spent": self.data["total_spent"]
        }
    
    def check_limits(self, today: str, current_month: str):
        """Check if usage exceeds limits and send alerts"""
        
        daily_cost = self.data["daily_usage"][today]["cost"]
        monthly_cost = self.data["monthly_usage"][current_month]["cost"]
        
        daily_limit = self.data["settings"]["daily_limit"]
        monthly_limit = self.data["settings"]["monthly_limit"]
        alert_threshold = self.data["settings"]["alert_threshold"]
        
        alerts = []
        
        # Check daily limit
        if daily_cost >= daily_limit:
            alerts.append(f"🚨 DAILY LIMIT EXCEEDED: ${daily_cost:.2f} >= ${daily_limit}")
        elif daily_cost >= daily_limit * alert_threshold:
            alerts.append(f"⚠️ Daily usage at {daily_cost/daily_limit*100:.1f}% of limit (${daily_cost:.2f})")
        
        # Check monthly limit
        if monthly_cost >= monthly_limit:
            alerts.append(f"🚨 MONTHLY LIMIT EXCEEDED: ${monthly_cost:.2f} >= ${monthly_limit}")
        elif monthly_cost >= monthly_limit * alert_threshold:
            alerts.append(f"⚠️ Monthly usage at {monthly_cost/monthly_limit*100:.1f}% of limit (${monthly_cost:.2f})")
        
        # Send alerts
        for alert in alerts:
            if alert not in self.data["alerts_sent"]:
                print(alert)
                self.data["alerts_sent"].append(alert)
    
    def get_usage_summary(self) -> Dict[str, Any]:
        """Get current usage summary"""
        today = datetime.now().strftime("%Y-%m-%d")
        current_month = datetime.now().strftime("%Y-%m")
        
        daily_usage = self.data["daily_usage"].get(today, {"tokens": 0, "cost": 0.0, "calls": 0})
        monthly_usage = self.data["monthly_usage"].get(current_month, {"tokens": 0, "cost": 0.0, "calls": 0})
        
        return {
            "today": {
                "tokens": daily_usage["tokens"],
                "cost": daily_usage["cost"],
                "calls": daily_usage["calls"],
                "limit": self.data["settings"]["daily_limit"],
                "percentage": (daily_usage["cost"] / self.data["settings"]["daily_limit"]) * 100
            },
            "this_month": {
                "tokens": monthly_usage["tokens"],
                "cost": monthly_usage["cost"],
                "calls": monthly_usage["calls"],
                "limit": self.data["settings"]["monthly_limit"],
                "percentage": (monthly_usage["cost"] / self.data["settings"]["monthly_limit"]) * 100
            },
            "total_spent": self.data["total_spent"],
            "remaining_daily": max(0, self.data["settings"]["daily_limit"] - daily_usage["cost"]),
            "remaining_monthly": max(0, self.data["settings"]["monthly_limit"] - monthly_usage["cost"])
        }
    
    def set_limits(self, daily_limit: float, monthly_limit: float):
        """Set new budget limits"""
        self.data["settings"]["daily_limit"] = daily_limit
        self.data["settings"]["monthly_limit"] = monthly_limit
        self.daily_limit = daily_limit
        self.monthly_limit = monthly_limit
        self.save_budget_data()
        print(f"✅ Budget limits updated: Daily ${daily_limit}, Monthly ${monthly_limit}")
    
    def reset_daily_usage(self):
        """Reset daily usage (for testing)"""
        today = datetime.now().strftime("%Y-%m-%d")
        if today in self.data["daily_usage"]:
            del self.data["daily_usage"][today]
        self.save_budget_data()
        print("✅ Daily usage reset")

def main():
    """Test the budget monitoring system"""
    print("💰 Budget Monitoring System Test")
    print("=" * 40)
    
    monitor = BudgetMonitor()
    
    # Test tracking usage
    print("\n📊 Testing usage tracking...")
    
    # Simulate 5 lessons
    for i in range(5):
        tokens = 4720  # Average from our mock test
        result = monitor.track_usage(tokens, "gpt-4-turbo")
        print(f"Lesson {i+1}: {tokens:,} tokens, ${result['cost']:.4f}")
    
    # Show summary
    summary = monitor.get_usage_summary()
    print(f"\n📈 Usage Summary:")
    print(f"Today: ${summary['today']['cost']:.2f} ({summary['today']['percentage']:.1f}% of daily limit)")
    print(f"This month: ${summary['this_month']['cost']:.2f} ({summary['this_month']['percentage']:.1f}% of monthly limit)")
    print(f"Total spent: ${summary['total_spent']:.2f}")
    print(f"Remaining today: ${summary['remaining_daily']:.2f}")
    print(f"Remaining this month: ${summary['remaining_monthly']:.2f}")

if __name__ == "__main__":
    main()
