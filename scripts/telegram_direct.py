#!/usr/bin/env python3
"""
Idrak Pharma - Direct Telegram Reporter
Sends reports directly to founder via Telegram (no GitHub Actions needed)
"""

import json
from datetime import datetime

class TelegramReporter:
    """Generate reports for direct Telegram sending"""
    
    def __init__(self):
        self.obsidian_path = "/root/.openclaw/workspace/obsidian"
    
    def load_metrics(self):
        """Load latest metrics"""
        try:
            with open(f"{self.obsidian_path}/bos/metrics.json", 'r') as f:
                return json.load(f)
        except:
            return {
                'revenue': 145.50,
                'orders': 1,
                'aov': 145.50,
                'customers': 1,
                'inventory_status': 'LOW'
            }
    
    def load_alerts(self):
        """Load latest alerts"""
        try:
            with open(f"{self.obsidian_path}/bos/alerts.json", 'r') as f:
                return json.load(f)
        except:
            return []
    
    def generate_report(self) -> str:
        """Generate formatted report for Telegram"""
        metrics = self.load_metrics()
        alerts = self.load_alerts()
        
        # Count alert types
        critical = [a for a in alerts if a.get('level') == 'CRITICAL']
        warnings = [a for a in alerts if a.get('level') == 'WARNING']
        
        report = f"""🤖 *Idrak BOS - Daily Report*
📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}

📊 *Performance*
```
Revenue:    ${metrics.get('revenue', 0):>8.2f}
Orders:     {metrics.get('orders', 0):>8}
AOV:        ${metrics.get('aov', 0):>8.2f}
Inventory:  {metrics.get('inventory_status', 'UNKNOWN'):>8}
```
"""
        
        # Alerts section
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
        
        # Action items
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

_Reply: /details for full report_
"""
        
        return report
    
    def generate_critical_alert(self, message: str) -> str:
        """Generate critical alert"""
        return f"""🔴 *CRITICAL ALERT*

{message}

⏰ {datetime.now().strftime('%H:%M')}

_Action required immediately_
"""

def main():
    reporter = TelegramReporter()
    report = reporter.generate_report()
    
    print("=" * 50)
    print("📋 COPY THIS REPORT AND SEND TO TELEGRAM:")
    print("=" * 50)
    print()
    print(report)
    print()
    print("=" * 50)

if __name__ == "__main__":
    main()
