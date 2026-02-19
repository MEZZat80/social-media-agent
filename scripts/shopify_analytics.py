#!/usr/bin/env python3
"""
Idrak Pharma - Shopify Analytics Fetcher
Fetches sales data from Shopify
"""

import os
import json
import requests
from datetime import datetime, timedelta

SHOPIFY_STORE = os.getenv('SHOPIFY_STORE', 'exhz4h-a3.myshopify.com')
SHOPIFY_TOKEN = os.getenv('SHOPIFY_ACCESS_TOKEN')

def fetch_orders():
    """Fetch recent orders from Shopify"""
    if not SHOPIFY_TOKEN:
        print("❌ SHOPIFY_ACCESS_TOKEN not found")
        return None
    
    url = f"https://{SHOPIFY_STORE}/admin/api/2024-01/orders.json?limit=50&status=any"
    headers = {
        "X-Shopify-Access-Token": SHOPIFY_TOKEN,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error fetching orders: {e}")
        return None

def fetch_products():
    """Fetch products from Shopify"""
    if not SHOPIFY_TOKEN:
        return None
    
    url = f"https://{SHOPIFY_STORE}/admin/api/2024-01/products.json?limit=50"
    headers = {
        "X-Shopify-Access-Token": SHOPIFY_TOKEN,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error fetching products: {e}")
        return None

def analyze_sales(orders_data):
    """Analyze sales data"""
    if not orders_data or 'orders' not in orders_data:
        return None
    
    orders = orders_data['orders']
    
    total_revenue = 0
    total_orders = len(orders)
    product_sales = {}
    
    for order in orders:
        # Revenue
        total_revenue += float(order.get('total_price', 0))
        
        # Product breakdown
        for item in order.get('line_items', []):
            product = item.get('title', 'Unknown')
            quantity = item.get('quantity', 0)
            product_sales[product] = product_sales.get(product, 0) + quantity
    
    return {
        'total_orders': total_orders,
        'total_revenue': round(total_revenue, 2),
        'avg_order_value': round(total_revenue / total_orders, 2) if total_orders > 0 else 0,
        'top_products': sorted(product_sales.items(), key=lambda x: x[1], reverse=True)[:5]
    }

def main():
    print(f"🚀 Idrak Pharma Analytics - {datetime.now()}")
    print(f"Store: {SHOPIFY_STORE}")
    
    # Fetch data
    orders = fetch_orders()
    products = fetch_products()
    
    if not orders:
        print("❌ Failed to fetch orders")
        return 1
    
    # Analyze
    analysis = analyze_sales(orders)
    
    if analysis:
        print("\n📊 Sales Analysis:")
        print(f"Total Orders: {analysis['total_orders']}")
        print(f"Total Revenue: ${analysis['total_revenue']}")
        print(f"Avg Order Value: ${analysis['avg_order_value']}")
        print("\n🔥 Top Products:")
        for product, qty in analysis['top_products']:
            print(f"  - {product}: {qty} units")
    
    # Save to file
    output = {
        'timestamp': datetime.now().isoformat(),
        'analysis': analysis,
        'raw_orders': len(orders.get('orders', []))
    }
    
    with open('shopify_analytics.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print("\n✅ Analytics saved to shopify_analytics.json")
    return 0

if __name__ == "__main__":
    exit(main())
