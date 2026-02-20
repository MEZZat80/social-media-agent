#!/usr/bin/env python3
"""
Shopify Monitor - Alert formatting for Telegram and other channels
"""

from datetime import datetime
from typing import Dict, List

class AlertFormatter:
    """Format alerts for different channels"""
    
    @staticmethod
    def telegram_daily_report(metrics: Dict, alerts: List[Dict]) -> str:
        """Format daily report for Telegram"""
        
        critical = [a for a in alerts if a['level'] == 'CRITICAL']
        warnings = [a for a in alerts if a['level'] == 'WARNING']
        
        report = f"""🤖 *Idrak Store Monitor*
📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}

📊 *Last 24 Hours*
```
Orders:     {metrics['orders_24h']:>3}
Revenue:    ${metrics['revenue_24h']:>7.2f}
AOV:        ${metrics['avg_order_value']:>7.2f}
```
"""
        
        if critical:
            report += f"\n🔴 *CRITICAL ({len(critical)})*\n"
            for alert in critical:
                report += f"⚠️ {alert['message']}\n"
        
        if warnings:
            report += f"\n🟡 *WARNINGS ({len(warnings)})*\n"
            for alert in warnings:
                report += f"• {alert['message']}\n"
        
        if not critical and not warnings:
            report += "\n✅ *All systems normal*\n"
        
        # Inventory status
        if metrics.get('out_of_stock'):
            report += f"\n📦 *Out of Stock:*\n"
            for item in metrics['out_of_stock'][:3]:
                report += f"  ❌ {item}\n"
        
        if metrics.get('low_stock'):
            report += f"\n📦 *Low Stock:*\n"
            for item in metrics['low_stock'][:3]:
                report += f"  ⚠️ {item['name']} ({item['qty']} left)\n"
        
        report += """
🎯 *Actions Needed*
"""
        
        if critical:
            report += "• 🚨 Address critical issues NOW\n"
        if metrics.get('out_of_stock'):
            report += "• 📞 Contact suppliers\n"
        if not critical and not warnings:
            report += "• 📈 Monitor competitors\n"
        
        report += "• 📊 Review marketing performance\n"
        
        return report
    
    @staticmethod
    def telegram_critical_alert(alert: Dict) -> str:
        """Format critical alert for immediate notification"""
        return f"""🔴 *CRITICAL ALERT*

*{alert['category']}*

{alert['message']}

*Action Required:*
{alert['action']}

⏰ {datetime.now().strftime('%H:%M')}

_Immediate response needed_
"""
    
    @staticmethod
    def slack_webhook_payload(metrics: Dict, alerts: List[Dict]) -> Dict:
        """Format payload for Slack webhook"""
        critical_count = len([a for a in alerts if a['level'] == 'CRITICAL'])
        
        color = 'danger' if critical_count > 0 else 'warning' if alerts else 'good'
        
        return {
            'attachments': [{
                'color': color,
                'title': 'Idrak Store Monitor',
                'fields': [
                    {'title': 'Orders 24h', 'value': metrics['orders_24h'], 'short': True},
                    {'title': 'Revenue 24h', 'value': f"${metrics['revenue_24h']:.2f}", 'short': True},
                    {'title': 'Alerts', 'value': len(alerts), 'short': True},
                ],
                'footer': datetime.now().strftime('%Y-%m-%d %H:%M')
            }]
        }
    
    @staticmethod
    def email_subject(alerts: List[Dict]) -> str:
        """Generate email subject line"""
        critical = len([a for a in alerts if a['level'] == 'CRITICAL'])
        
        if critical > 0:
            return f"🔴 URGENT: {critical} Critical Issues - Idrak Store"
        elif alerts:
            return f"⚠️ {len(alerts)} Warnings - Idrak Store Daily Report"
        else:
            return "✅ Idrak Store Daily Report - All Good"

def main():
    # Test formatting
    test_metrics = {
        'orders_24h': 2,
        'revenue_24h': 291.00,
        'avg_order_value': 145.50,
        'out_of_stock': ['AgeCore NAD+'],
        'low_stock': [{'name': 'Neuro-Blue', 'qty': 5}]
    }
    
    test_alerts = [
        {
            'level': 'CRITICAL',
            'category': 'INVENTORY',
            'message': 'AgeCore NAD+ is out of stock',
            'action': 'Contact supplier immediately'
        }
    ]
    
    formatter = AlertFormatter()
    print(formatter.telegram_daily_report(test_metrics, test_alerts))

if __name__ == "__main__":
    main()
