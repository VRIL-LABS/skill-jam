---
name: inventory-manager
description: Tracks stock levels across locations, predicts reorder points using demand forecasting, and triggers purchase orders. Invoke when asked to manage inventory, track stock levels, forecast demand, set reorder points, generate purchase orders, or analyze inventory health.
---

# Inventory Manager

Tracks stock levels across locations and warehouses, forecasts demand using historical sales data, calculates optimal reorder points and safety stock, generates purchase orders, and surfaces inventory health insights — helping prevent stockouts and excess inventory.

## When to Use

- User wants to track current stock levels across one or more locations
- Reorder points need to be calculated for a product catalog
- A purchase order needs to be generated when stock falls below threshold
- Demand forecasting is needed to plan procurement for an upcoming period
- User asks to analyze inventory health: excess stock, dead stock, or stockout risk
- A multi-location inventory needs to be reconciled or balanced
- User asks to generate an inventory report or aging analysis

## Process

1. **Inventory data intake**:
   - Accept: inventory export (CSV, Excel, JSON), API connection to an inventory system (Shopify, NetSuite, SAP, etc.), or manual input
   - Required fields per SKU: SKU ID, product name, current stock quantity, unit of measure, location/warehouse
   - Optional fields: safety stock level, lead time (days), supplier info, cost per unit, historical sales data

2. **Calculate stock status per SKU**:
   - **Days of inventory on hand (DOH)**: `current_stock / average_daily_demand`
   - **Stock health classification**:
     - 🔴 **Stockout / Critical**: 0 units or < 7 days DOH — immediate reorder needed
     - 🟡 **Low Stock**: 7–30 days DOH — reorder soon
     - 🟢 **Healthy**: 30–90 days DOH — normal range
     - ⚪ **Excess Stock**: > 90 days DOH — capital tied up, potential obsolescence risk
     - 💀 **Dead Stock**: no sales in the last 90 days — review for write-off or promotion

3. **Demand forecasting**:
   - Calculate average daily demand from historical sales (use 90-day rolling average as default)
   - Apply seasonality adjustments if historical data shows seasonal patterns (e.g., 30% uplift in December)
   - Forecast demand for the next 30, 60, 90 days
   - Flag high-uncertainty forecasts (high variance in sales history, new products with <30 days of data)
   - For planned promotions or events: apply an uplift multiplier if the user provides expected lift percentage

4. **Calculate optimal reorder parameters**:

   **Reorder Point (ROP)**:
   `ROP = (Average Daily Demand × Lead Time) + Safety Stock`

   **Safety Stock**:
   `Safety Stock = Z-score × Standard Deviation of Demand × √Lead Time`
   - Z-score: 1.645 for 95% service level (default), 2.054 for 98%, 2.326 for 99%
   - If demand history is insufficient, use a simpler safety stock: `Safety Stock = Average Demand × Lead Time × 0.5`

   **Economic Order Quantity (EOQ)** (optional, when cost data available):
   `EOQ = √(2 × Annual Demand × Ordering Cost / Holding Cost per unit per year)`

5. **Generate purchase orders**:
   - Trigger a PO draft when: current stock ≤ ROP, or user manually requests
   - PO contents: supplier name, order date, required delivery date (order date + lead time), line items (SKU, description, quantity to order, unit cost, line total), total PO value
   - Order quantity: EOQ if calculated, or `(Target DOH × Daily Demand) − Current Stock` with minimum order quantity applied
   - Flag if ordering from this supplier requires a minimum order value

6. **Multi-location management**:
   - Roll up total stock across all locations per SKU
   - Identify imbalances: excess stock at Location A vs. stockout risk at Location B → recommend stock transfer before reordering
   - Allocate incoming PO receipts to locations based on relative demand

7. **Inventory health reports**:
   - **Summary dashboard**: total SKU count, total inventory value, stockout count, low-stock count, excess stock value, dead stock value
   - **Aging analysis**: group stock by age (<30 days, 30–90 days, 90–180 days, >180 days)
   - **ABC analysis**: classify SKUs by revenue contribution: A (top 80%), B (next 15%), C (bottom 5%) — focus reorder optimization on A items
   - **Slow-mover report**: SKUs with <1 unit sold per day for the past 60 days
   - **Stockout risk report**: SKUs expected to reach zero before the next PO can arrive

## Output Format

### Inventory Health Dashboard
```
## Inventory Health Summary — June 1, 2025
Total SKUs: 342 | Total Inventory Value: $487,230

| Status          | SKU Count | Value        |
|-----------------|-----------|--------------|
| 🔴 Stockout/Critical | 8    | $12,400      |
| 🟡 Low Stock    | 23        | $38,100      |
| 🟢 Healthy      | 287       | $390,200     |
| ⚪ Excess Stock | 19        | $36,800      |
| 💀 Dead Stock   | 5         | $9,730       |

Action Required: 8 critical SKUs need immediate purchase orders.
```

### Reorder Report
```
🔴 REORDER REQUIRED — Critical SKUs (June 1, 2025)

| SKU      | Product          | Stock | DOH  | ROP   | Order Qty | Supplier        | Est. Cost   |
|----------|------------------|-------|------|-------|-----------|-----------------|-------------|
| SKU-1042 | Blue Widget Pro  | 45    | 4.5d | 80    | 200       | WidgetCo Ltd    | $1,400.00   |
| SKU-2187 | Red Widget Mini  | 12    | 2.4d | 60    | 150       | WidgetCo Ltd    | $750.00     |
| SKU-3301 | Cable Set A      | 0     | 0d   | 40    | 100       | ConnectorPlus   | $320.00     |

Total PO Value: $2,470.00
Recommended: Combine WidgetCo orders into one PO to meet $1,000 minimum order value.
```

### Generated Purchase Order
```
PURCHASE ORDER — PO-2025-0622
Date: June 1, 2025 | Required Delivery: June 8, 2025

Supplier: WidgetCo Ltd
Contact: orders@widgetco.com | +1-800-555-0100

Line Items:
1. Blue Widget Pro (SKU-1042) × 200 @ $7.00 ea = $1,400.00
2. Red Widget Mini (SKU-2187) × 150 @ $5.00 ea = $750.00

Subtotal: $2,150.00
Shipping: TBD
Total: $2,150.00

Ship to: Main Warehouse, 123 Logistics Way, Chicago, IL 60601
Notes: Please confirm receipt of PO within 24 hours. Mark boxes with PO number.
```

## Examples

### Example Input
```
Here's my inventory CSV. Calculate reorder points for all SKUs with <30 days of stock. Lead time is 7 days and I want 95% service level.
```

### Example Output
```
Analyzed 342 SKUs. Found 31 SKUs with <30 days of stock.

Top 5 critical items:
1. SKU-1042 (Blue Widget Pro): 4.5 DOH · ROP=80 · Order 200 units from WidgetCo
2. SKU-3301 (Cable Set A): 0 DOH ❌ STOCKOUT · Order 100 units immediately
...

Safety stock calculated at 95% service level (Z=1.645).
Full reorder report attached. Generate purchase orders? [Yes/No]
```

## Boundaries

- Do NOT submit or transmit purchase orders to suppliers without explicit user confirmation of all PO details.
- Demand forecasts are estimates based on historical data — flag when historical data is insufficient or highly variable.
- When lead times or supplier minimums change, recalculate ROP before generating new POs.
- Do NOT apply demand uplifts for planned events without the user explicitly providing expected uplift figures.
- Always calculate safety stock with transparency — show the formula and inputs used.
- Flag dead stock for review but do NOT auto-write-off or recommend disposal without user confirmation.
