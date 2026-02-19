#!/usr/bin/env python3
"""
Idrak Pharma - Business Operating System (BOS)
Automated business management and decision support
"""

import os
import json
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional

@dataclass
class BusinessMetrics:
    """Core business metrics"""
    date: str
    revenue: float
    orders: int
    customers: int
    cac: float  # Customer Acquisition Cost
    ltv: float  # Lifetime Value
    aov: float  # Average Order Value
    inventory_status: str
    
@dataclass
class Alert:
    """Business alerts"""
    level: str  # CRITICAL, WARNING, INFO
    category: str
    message: str
    action_required: str
    timestamp: str

class BusinessOperatingSystem:
    """
    Automated business management system for Idrak Pharma
    """
    
    def __init__(self):
        self.obsidian_path = "/root/.openclaw/workspace/obsidian/bos"
        self.metrics_file = f"{self.obsidian_path}/metrics.json"
        self.alerts_file = f"{self.obsidian_path}/alerts.json"
        self.decisions_file = f"{self.obsidian_path}/decisions.md"
        
        os.makedirs(self.obsidian_path, exist_ok=True)
        
        # Business rules and thresholds
        self.rules = {
            'min_daily_revenue': 100,  # $100/day minimum
            'min_orders_per_week': 5,
            'max_cac': 50,  # $50 max customer acquisition cost
            'min_inventory_days': 30,
            'cash_runway_warning': 90,  # 90 days warning
        }
    
    def fetch_current_metrics(self) -> BusinessMetrics:
        """Fetch current business metrics from Shopify"""
        # TODO: Integrate with Shopify API
        # For now, using placeholder data
        return BusinessMetrics(
            date=datetime.now().strftime('%Y-%m-%d'),
            revenue=145.50,
            orders=1,
            customers=1,
            cac=0,  # Organic traffic
            ltv=145.50,  # First order
            aov=145.50,
            inventory_status='LOW'  # Based on previous analysis
        )
    
    def analyze_health(self, metrics: BusinessMetrics) -> List[Alert]:
        """Analyze business health and generate alerts"""
        alerts = []
        
        # Revenue check
        if metrics.revenue < self.rules['min_daily_revenue']:
            alerts.append(Alert(
                level='CRITICAL',
                category='REVENUE',
                message=f'Daily revenue ${metrics.revenue} below minimum ${self.rules["min_daily_revenue"]}',
                action_required='Launch paid acquisition campaign immediately',
                timestamp=datetime.now().isoformat()
            ))
        
        # Order velocity check
        if metrics.orders < 1:
            alerts.append(Alert(
                level='CRITICAL',
                category='SALES',
                message='No orders in last 24 hours',
                action_required='Check website functionality, launch retargeting',
                timestamp=datetime.now().isoformat()
            ))
        
        # Inventory check
        if metrics.inventory_status == 'LOW':
            alerts.append(Alert(
                level='WARNING',
                category='INVENTORY',
                message='Inventory running low',
                action_required='Reorder top-selling SKUs within 7 days',
                timestamp=datetime.now().isoformat()
            ))
        
        # CAC efficiency
        if metrics.cac > self.rules['max_cac'] and metrics.cac > 0:
            alerts.append(Alert(
                level='WARNING',
                category='MARKETING',
                message=f'CAC ${metrics.cac} exceeds target ${self.rules["max_cac"]}',
                action_required='Optimize ad targeting or switch channels',
                timestamp=datetime.now().isoformat()
            ))
        
        return alerts
    
    def generate_decisions(self, metrics: BusinessMetrics, alerts: List[Alert]) -> str:
        """Generate automated business decisions"""
        
        decisions = f"""---
date: {datetime.now().strftime('%Y-%m-%d %H:%M')}
type: automated-decisions
---

# 🤖 Business Operating System - Daily Decisions

## 📊 Current State

| Metric | Value | Status |
|--------|-------|--------|
| Revenue | ${metrics.revenue:.2f} | {'✅ OK' if metrics.revenue >= self.rules['min_daily_revenue'] else '❌ LOW'} |
| Orders | {metrics.orders} | {'✅ OK' if metrics.orders >= 1 else '❌ NONE'} |
| AOV | ${metrics.aov:.2f} | ✅ OK |
| Inventory | {metrics.inventory_status} | {'✅ OK' if metrics.inventory_status == 'OK' else '⚠️ WARNING'} |

## 🚨 Active Alerts ({len(alerts)})

"""
        
        for alert in alerts:
            emoji = '🔴' if alert.level == 'CRITICAL' else '🟡' if alert.level == 'WARNING' else '🟢'
            decisions += f"""
### {emoji} {alert.level}: {alert.category}

**Issue:** {alert.message}

**Action Required:** {alert.action_required}

---
"""
        
        decisions += f"""
## 🎯 Automated Decisions

### Immediate (Today)
"""
        
        # Auto-generate decisions based on alerts
        if any(a.level == 'CRITICAL' for a in alerts):
            decisions += """
- [ ] **PRIORITY 1**: Launch Meta Ads campaign (Budget: $50/day)
- [ ] **PRIORITY 1**: Send email to existing customers with 15% discount
- [ ] **PRIORITY 1**: Check website checkout flow for errors
"""
        
        if any(a.category == 'INVENTORY' for a in alerts):
            decisions += """
- [ ] **PRIORITY 2**: Contact supplier for Neuro-Blue restock
- [ ] **PRIORITY 2**: Consider pre-order campaign for out-of-stock items
"""
        
        decisions += f"""
### This Week
- [ ] Review competitor pricing (Thorne, Qualia)
- [ ] Analyze customer feedback from last 5 orders
- [ ] Prepare content calendar for next 2 weeks
- [ ] Test new landing page headline

### This Month
- [ ] Launch subscription model (compete with Elysium)
- [ ] Partner with 2 health influencers
- [ ] Apply for Amazon Seller account
- [ ] Draft whitepaper on AI formulation

## 📈 Growth Targets

| Metric | Current | Target (30d) | Target (90d) |
|--------|---------|--------------|--------------|
| Daily Revenue | ${metrics.revenue:.2f} | $300 | $1,000 |
| Orders/Week | {metrics.orders * 7} | 20 | 50 |
| Customer LTV | ${metrics.ltv:.2f} | $200 | $400 |
| Email List | 0 | 100 | 500 |

## 🎲 Scenario Planning

### Best Case (Revenue 3x)
- Increase ad spend to $200/day
- Hire customer service VA
- Launch 2 new SKUs

### Worst Case (Revenue 0.5x)
- Pause all paid ads
- Focus on organic content
- Cut non-essential costs
- Pivot to B2B wholesale

### Most Likely (Revenue 1.5x)
- Maintain current ad spend
- Optimize conversion rate
- Launch email marketing
- Build referral program

---

*Generated by Idrak BOS v1.0*
*Next review: Tomorrow 9:00 AM*
"""
        
        return decisions
    
    def run_daily_check(self):
        """Run daily business health check"""
        print(f"🤖 Running Idrak BOS Daily Check - {datetime.now()}")
        
        # Fetch metrics
        metrics = self.fetch_current_metrics()
        print(f"📊 Revenue: ${metrics.revenue}, Orders: {metrics.orders}")
        
        # Analyze health
        alerts = self.analyze_health(metrics)
        print(f"🚨 {len(alerts)} alerts generated")
        
        # Generate decisions
        decisions = self.generate_decisions(metrics, alerts)
        
        # Save to files
        with open(self.decisions_file, 'w', encoding='utf-8') as f:
            f.write(decisions)
        
        with open(self.metrics_file, 'w') as f:
            json.dump(asdict(metrics), f, indent=2)
        
        with open(self.alerts_file, 'w') as f:
            json.dump([asdict(a) for a in alerts], f, indent=2)
        
        print(f"✅ BOS check complete. Decisions saved to: {self.decisions_file}")
        
        return {
            'metrics': metrics,
            'alerts': alerts,
            'decisions_file': self.decisions_file
        }

def main():
    bos = BusinessOperatingSystem()
    result = bos.run_daily_check()
    
    # Print critical alerts
    critical = [a for a in result['alerts'] if a.level == 'CRITICAL']
    if critical:
        print(f"\n🔴 {len(critical)} CRITICAL issues require immediate action!")
        for alert in critical:
            print(f"  - {alert.message}")

if __name__ == "__main__":
    main()
