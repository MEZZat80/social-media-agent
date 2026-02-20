---
name: shopify-monitor
description: Real-time Shopify store monitoring with instant alerts. Tracks sales, inventory, orders, and customer behavior. Sends notifications when critical events occur (zero sales, low stock, new orders). Use when continuous monitoring of e-commerce performance is needed without manual checking.
---

# Shopify Monitor

Real-time monitoring and alerting for Shopify stores.

## Capabilities

- **Sales Monitoring**: Track revenue, orders, AOV in real-time
- **Inventory Alerts**: Notify when products run low or out of stock
- **Order Notifications**: Instant alerts for new orders
- **Performance Metrics**: CAC, LTV, conversion rates
- **Competitor Price Tracking**: Monitor competitor pricing changes

## Quick Start

```python
from shopify_monitor import ShopifyMonitor

monitor = ShopifyMonitor(
    store='your-store.myshopify.com',
    token='your-access-token'
)

# Check now
status = monitor.check_store_health()

# Start continuous monitoring
monitor.start_monitoring(interval_minutes=15)
```

## Alert Types

| Level | Trigger | Action |
|-------|---------|--------|
| 🔴 CRITICAL | No sales for 2+ hours | Immediate notification |
| 🔴 CRITICAL | Product out of stock | Restock alert |
| 🟡 WARNING | Inventory < 10 units | Low stock warning |
| 🟡 WARNING | CAC > $50 | Marketing efficiency alert |
| 🟢 INFO | New order received | Confirmation |

## Scripts

- `scripts/monitor.py` - Main monitoring engine
- `scripts/alerts.py` - Alert generation and formatting
- `scripts/reports.py` - Daily/weekly report generation

## Usage Patterns

### Monitor Single Store
```python
monitor = ShopifyMonitor(store, token)
monitor.check_now()
```

### Continuous Monitoring
```python
monitor.start_monitoring(interval=900)  # Every 15 min
```

### Custom Alerts
```python
monitor.add_alert_rule(
    condition='revenue < 100',
    level='CRITICAL',
    message='Daily revenue below target'
)
```
