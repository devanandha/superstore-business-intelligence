-- Reproducible KPI queries for the Superstore SQLite database.

SELECT COUNT(*) AS total_rows FROM orders;

SELECT COUNT(DISTINCT "Customer ID") AS unique_customers FROM orders;

SELECT
    MIN(date(OrderDate_clean)) AS start_date,
    MAX(date(OrderDate_clean)) AS end_date
FROM orders;

SELECT
    ROUND(SUM(Sales), 2) AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit,
    COUNT(DISTINCT "Order ID") AS total_orders
FROM orders;

SELECT Category, ROUND(SUM(Sales), 2) AS total_sales
FROM orders
GROUP BY Category
ORDER BY total_sales DESC;

SELECT
    strftime('%Y-%m', OrderDate_clean) AS month,
    ROUND(SUM(Sales), 2) AS monthly_sales
FROM orders
GROUP BY month
ORDER BY month;

SELECT
    ROUND(COUNT(r."Order ID") * 1.0 / COUNT(o."Order ID"), 4) AS row_level_return_rate
FROM orders AS o
LEFT JOIN returns AS r ON o."Order ID" = r."Order ID";

SELECT Region, ROUND(SUM(Profit), 2) AS total_profit
FROM orders
GROUP BY Region
ORDER BY total_profit DESC;

SELECT "Product Name", ROUND(SUM(Sales), 2) AS total_sales
FROM orders
GROUP BY "Product Name"
ORDER BY total_sales DESC
LIMIT 10;
