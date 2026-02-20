#!/usr/bin/env python3
"""
Shopify Monitor - Real-time store monitoring and alerting
"""

import os
import json
import time
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable

class ShopifyMonitor:
    """
    Monitor Shopify store performance and send alerts
    """
    
    def __init__(self, store: str = None, token: str = None):
        self.store = store or os.getenv('SHOPIFY_STORE')
        self.token = token or os.getenv('SHOPIFY_ACCESS_TOKEN')
        self.base_url = f"https://{self.store}/admin/api/2024-01"
        self.headers = {
            "X-Shopify-Access-Token": self.token,
            "Content-Type": "application/json"
        }
        self.alert_rules = []
        self.alert_handlers = []
    
    def _api_get(self, endpoint: str) -> Optional[Dict]:
        """Make GET request to Shopify API"""
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ API Error: {e}")
            return None
    
    def get_orders(self, limit: int = 50, status: str = 'any') -> List[Dict]:
        """Fetch recent orders"""
        data = self._api_get(f"orders.json?limit={limit}&status={status}")
        return data.get('orders', []) if data else []
    
    def get_products(self, limit: int = 50) -> List[Dict]:
        """Fetch products with inventory info"""
        data = self._api_get(f"products.json?limit={limit}")
        return data.get('products', []) if data else []
    
    def calculate_metrics(self) -> Dict:
        """Calculate store metrics"""
        orders = self.get_orders(limit=100)
        products = self.get_products(limit=100)
        
        # Sales metrics
        total_revenue = sum(float(o.get('total_price', 0)) for o in orders)
        total_orders = len(orders)
        
        # Inventory metrics
        low_stock = []
        out_of_stock = []
        
        for product in products:
            for variant in product.get('variants', []):
                qty = variant.get('inventory_quantity', 0)
                if qty == 0:
                    out_of_stock.append(product.get('title'))
                elif qty < 10:
                    low_stock.append({
                        'name': product.get('title'),
                        'qty': qty
                    })
        
        # Time-based metrics
        now = datetime.now()
        last_24h = [o for o in orders 
                   if datetime.fromisoformat(o.get('created_at', '').replace('Z', '+00:00')).replace(tzinfo=None) > now - timedelta(hours=24)]
        
        return {
            'timestamp': now.isoformat(),
            'total_revenue': total_revenue,
            'total_orders': total_orders,
            'avg_order_value': total_revenue / total_orders if total_orders > 0 else 0,
            'orders_24h': len(last_24h),
            'revenue_24h': sum(float(o.get('total_price', 0)) for o in last_24h),
            'low_stock': low_stock,
            'out_of_stock': out_of_stock,
            'inventory_status': 'CRITICAL' if out_of_stock else 'WARNING' if low_stock else 'OK'
        }
    
    def check_alerts(self, metrics: Dict) -> List[Dict]:
        """Check for alert conditions"""
        alerts = []
        
        # Critical: No sales in 24h
        if metrics['orders_24h'] == 0:
            alerts.append({
                'level': 'CRITICAL',
                'category': 'SALES',
                'message': 'No orders in last 24 hours',
                'action': 'Launch marketing campaign immediately'
            })
        
        # Critical: Out of stock
        if metrics['out_of_stock']:
            alerts.append({
                'level': 'CRITICAL',
                'category': 'INVENTORY',
                'message': f"{len(metrics['out_of_stock'])} products out of stock",
                'action': 'Restock immediately: ' + ', '.join(metrics['out_of_stock'][:3])
            })
        
        # Warning: Low stock
        if metrics['low_stock']:
            alerts.append({
                'level': 'WARNING',
                'category': 'INVENTORY',
                'message': f"{len(metrics['low_stock'])} products running low",
                'action': 'Plan restocking for: ' + ', '.join([p['name'] for p in metrics['low_stock'][:3]])
            })
        
        return alerts
    
    def format_alert(self, alert: Dict) -> str:
        """Format alert for display"""
        emoji = '🔴' if alert['level'] == 'CRITICAL' else '🟡'
        return f"""
{emoji} {alert['level']}: {alert['category']}

{alert['message']}

Action: {alert['action']}
"""
    
    def check_now(self) -> Dict:
        """Perform immediate health check"""
        print(f"🔍 Checking {self.store} at {datetime.now()}")
        
        metrics = self.calculate_metrics()
        alerts = self.check_alerts(metrics)
        
        result = {
            'timestamp': datetime.now().isoformat(),
            'metrics': metrics,
            'alerts': alerts,
            'status': 'CRITICAL' if any(a['level'] == 'CRITICAL' for a in alerts) else 
                     'WARNING' if alerts else 'OK'
        }
        
        # Print summary
        print(f"📊 Orders 24h: {metrics['orders_24h']}")
        print(f"💰 Revenue 24h: ${metrics['revenue_24h']:.2f}")
        print(f"⚠️  Alerts: {len(alerts)}")
        
        for alert in alerts:
            print(self.format_alert(alert))
        
        return result
    
    def start_monitoring(self, interval_minutes: int = 15):
        """Start continuous monitoring"""
        print(f"🚀 Starting monitoring every {interval_minutes} minutes")
        
        while True:
            self.check_now()
            print(f"⏰ Next check in {interval_minutes} minutes...\n")
            time.sleep(interval_minutes * 60)

def main():
    import sys
    
    store = sys.argv[1] if len(sys.argv) > 1 else os.getenv('SHOPIFY_STORE')
    token = sys.argv[2] if len(sys.argv) > 2 else os.getenv('SHOPIFY_ACCESS_TOKEN')
    
    if not store or not token:
        print("❌ Usage: python monitor.py [store] [token]")
        print("   Or set SHOPIFY_STORE and SHOPIFY_ACCESS_TOKEN env vars")
        return
    
    monitor = ShopifyMonitor(store, token)
    monitor.check_now()

if __name__ == "__main__":
    main()
