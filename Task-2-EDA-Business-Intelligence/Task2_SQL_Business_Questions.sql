-- ApexPlanet Data Analytics Internship - Task 2
-- Table name assumed: sales_cleaned

-- Q1 Monthly sales trend
SELECT EXTRACT(YEAR FROM order_date) AS year,
       EXTRACT(MONTH FROM order_date) AS month,
       SUM(total_sales) AS total_sales
FROM sales_cleaned
GROUP BY EXTRACT(YEAR FROM order_date), EXTRACT(MONTH FROM order_date)
ORDER BY year, month;

-- Q2 Top categories
SELECT category, SUM(total_sales) AS total_sales
FROM sales_cleaned
GROUP BY category
ORDER BY total_sales DESC;

-- Q3 Top products
SELECT product, SUM(total_sales) AS total_sales
FROM sales_cleaned
GROUP BY product
ORDER BY total_sales DESC;

-- Q4 Sales by city
SELECT city, SUM(total_sales) AS total_sales
FROM sales_cleaned
GROUP BY city
ORDER BY total_sales DESC;

-- Q5 Sales by gender
SELECT gender, SUM(total_sales) AS total_sales
FROM sales_cleaned
GROUP BY gender
ORDER BY total_sales DESC;

-- Q6 Sales by age group
SELECT age_group, SUM(total_sales) AS total_sales
FROM sales_cleaned
GROUP BY age_group
ORDER BY total_sales DESC;

-- Q7 Unit price vs sales relationship
SELECT CORR(unit_price, total_sales) AS price_sales_correlation
FROM sales_cleaned;
