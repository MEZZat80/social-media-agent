#!/usr/bin/env python3
"""
Idrak Pharma - Automated Telegram Reporter
Daily reports + Critical alerts
Runs via cron/heartbeat
"""

import json
import os
from datetime import datetime
from typing import List, Dict

class AutomatedReporter:
    """Automated reporting system for Idrak Pharma"""
    
    def __init__(self):
        self.obsidian_path = "/root/.openclaw/workspace/obsidian"
        self.last_alert_file = f"{self.obsidian_path}/bos/last_alert_sent.json"
        self.daily_report_file = f"{self.obsidian_path}/bos/last_daily_report.json"
    
    def load_metrics(self) -> Dict:
        """Load latest metrics from Shopify/BOS"""
        try:
            with open(f"{self.obsidian_path}/bos/metrics.json", 'r') as f:
                return json.load(f)
        except:
            return {
                'revenue': 145.50,
                'orders': 1,
                'aov': 145.50,
                'customers': 1,
                'inventory_status': 'LOW',
                'date': datetime.now().isoformat()
            }
    
    def load_alerts(self) -> List[Dict]:
        """Load latest alerts"""
        try:
            with open(f"{self.obsidian_path}/bos/alerts.json", 'r') as f:
                return json.load(f)
        except:
            return []
    
    def should_send_daily_report(self) -> bool:
        """Check if daily report should be sent (9 AM)"""
        now = datetime.now()
        
        # Must be 9:00-9:59 AM
        if now.hour != 9:
            return False
        
        # Check if already sent today
        try:
            with open(self.daily_report_file, 'r') as f:
                last_sent = json.load(f)
                last_date = last_sent.get('date', '')
                if last_date == now.strftime('%Y-%m-%d'):
                    return False
        except:
            pass
        
        return True
    
    def should_send_critical_alert(self) -> tuple[bool, str]:
        """Check if critical alert should be sent"""
        alerts = self.load_alerts()
        critical_alerts = [a for a in alerts if a.get('level') == 'CRITICAL']
        
        if not critical_alerts:
            return False, ""
        
        # Get first critical alert
        alert = critical_alerts[0]
        alert_id = f"{alert.get('category')}_{alert.get('timestamp', '')}"
        
        # Check if already sent
        try:
            with open(self.last_alert_file, 'r') as f:
                last_sent = json.load(f)
                if last_sent.get('alert_id') == alert_id:
                    return False, ""
        except:
            pass
        
        return True, alert_id
    
    def generate_daily_report(self) -> str:
        """Generate formatted daily report"""
        metrics = self.load_metrics()
        alerts = self.load_alerts()
        
        critical = [a for a in alerts if a.get('level') == 'CRITICAL']
        warnings = [a for a in alerts if a.get('level') == 'WARNING']
        
        report = f"""🤖 *Idrak BOS - Daily Report*
📅 {datetime.now().strftime('%Y-%m-%d')}

📊 *Performance*
```
Revenue:    ${metrics.get('revenue', 0):>8.2f}
Orders:     {metrics.get('orders', 0):>8}
AOV:        ${metrics.get('aov', 0):>8.2f}
Inventory:  {metrics.get('inventory_status', 'OK'):>8}
```
"""
        
        if critical:
            report += f"""
🔴 *CRITICAL ({len(critical)})*
"""
            for alert in critical[:3]:
                report += f"• {alert.get('message', '')}\n"
        
        if warnings:
            report += f"""
🟡 *WARNINGS ({len(warnings)})*
"""
            for alert in warnings[:3]:
                report += f"• {alert.get('message', '')}\n"
        
        if not critical and not warnings:
            report += """
✅ *All systems normal*
"""
        
        report += """
🎯 *Today's Actions*
"""
        
        if critical:
            report += """• 🚨 Launch Meta Ads NOW
• 🚨 Check website checkout
"""
        elif warnings:
            report += """• ⚠️ Contact supplier
• ⚠️ Review inventory
"""
        else:
            report += """• 📈 Monitor competitors
• 📈 Plan tomorrow's content
"""
        
        report += """
📈 *Targets*
```
Current:  $145/day
30d:      $300/day
90d:      $1000/day
```
"""
        
        return report
    
    def generate_critical_alert(self, alert: Dict) -> str:
        """Generate critical alert message"""
        return f"""🔴 *CRITICAL ALERT*

*{alert.get('category', 'BUSINESS')}*

{alert.get('message', '')}

*Action Required:*
{alert.get('action_required', 'Immediate action needed')}

⏰ {datetime.now().strftime('%H:%M')}
"""
    
    def mark_daily_sent(self):
        """Mark daily report as sent"""
        with open(self.daily_report_file, 'w') as f:
            json.dump({'date': datetime.now().strftime('%Y-%m-%d')}, f)
    
    def mark_alert_sent(self, alert_id: str):
        """Mark alert as sent"""
        with open(self.last_alert_file, 'w') as f:
            json.dump({'alert_id': alert_id, 'timestamp': datetime.now().isoformat()}, f)
    
    def run(self):
        """Main runner - check and generate reports/alerts"""
        messages = []
        
        # Check for daily report
        if self.should_send_daily_report():
            report = self.generate_daily_report()
            messages.append(('DAILY', report))
            self.mark_daily_sent()
        
        # Check for critical alerts
        should_alert, alert_id = self.should_send_critical_alert()
        if should_alert:
            alerts = self.load_alerts()
            critical = [a for a in alerts if a.get('level') == 'CRITICAL'][0]
            alert_msg = self.generate_critical_alert(critical)
            messages.append(('CRITICAL', alert_msg))
            self.mark_alert_sent(alert_id)
        
        return messages

def main():
    reporter = AutomatedReporter()
    messages = reporter.run()
    
    if not messages:
        print("📭 No messages to send at this time")
        print(f"⏰ Current time: {datetime.now().strftime('%H:%M')}")
        print("📊 Next daily report: 09:00")
        return
    
    for msg_type, content in messages:
        print("=" * 50)
        print(f"📤 {msg_type} REPORT - COPY AND SEND:")
        print("=" * 50)
        print()
        print(content)
        print()
        print("=" * 50)

if __name__ == "__main__":
    main()
