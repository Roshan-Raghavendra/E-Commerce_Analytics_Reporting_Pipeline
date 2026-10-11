-- E-Commerce Analytics & Reporting Pipeline
-- SQLite-compatible SQL analysis queries

-- 1. Overall business KPIs
SELECT
    COUNT(DISTINCT Order_ID) AS total_orders,
    ROUND(SUM(Net_Sales), 2) AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit,
    ROUND(AVG(Net_Sales), 2) AS average_order_value
FROM ecommerce_orders
WHERE Order_Status <> 'Cancelled';

-- 2. Monthly sales and profit
SELECT
    Order_Month,
    ROUND(SUM(Net_Sales), 2) AS sales,
    ROUND(SUM(Profit), 2) AS profit
FROM ecommerce_orders
WHERE Order_Status <> 'Cancelled'
GROUP BY Order_Month
ORDER BY Order_Month;

-- 3. Sales by category
SELECT
    Category,
    COUNT(DISTINCT Order_ID) AS orders,
    ROUND(SUM(Net_Sales), 2) AS sales,
    ROUND(SUM(Profit), 2) AS profit
FROM ecommerce_orders
WHERE Order_Status <> 'Cancelled'
GROUP BY Category
ORDER BY sales DESC;

-- 4. Top 10 products by sales
SELECT
    Product_Name,
    ROUND(SUM(Net_Sales), 2) AS sales,
    SUM(Quantity) AS units_sold
FROM ecommerce_orders
WHERE Order_Status <> 'Cancelled'
GROUP BY Product_Name
ORDER BY sales DESC
LIMIT 10;

-- 5. Sales by customer segment
SELECT
    Customer_Segment,
    COUNT(DISTINCT Customer_ID) AS customers,
    ROUND(SUM(Net_Sales), 2) AS sales,
    ROUND(SUM(Profit), 2) AS profit
FROM ecommerce_orders
WHERE Order_Status <> 'Cancelled'
GROUP BY Customer_Segment
ORDER BY sales DESC;

-- 6. Payment method usage
SELECT
    Payment_Method,
    COUNT(DISTINCT Order_ID) AS orders,
    ROUND(SUM(Net_Sales), 2) AS sales
FROM ecommerce_orders
GROUP BY Payment_Method
ORDER BY orders DESC;
