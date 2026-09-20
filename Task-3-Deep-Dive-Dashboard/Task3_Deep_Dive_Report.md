# Task 3 — Deep-Dive Analysis & Interactive Dashboarding

## Chosen business area
**Category and product performance**.

## Core KPIs
1. Total Sales = SUM(Total_Sales)
2. Average Order Value = SUM(Total_Sales) / COUNT(Transaction_ID)
3. Transactions = COUNT(Transaction_ID)
4. Unique Customers = COUNT(DISTINCT Customer_ID)
5. Units Sold = SUM(Quantity)

## Deep-dive findings
The analysis ranks categories and products by total sales, transaction volume, and quantity. The full ranking is in `Task3_Category_Product_Deep_Dive.csv`.

## Dashboard design
Recommended interactive controls:
- Date/year/month filter
- Category filter
- Product filter
- City filter
- Gender filter
- KPI cards for Total Sales, AOV, Transactions, Customers
- Monthly sales line chart
- Category sales bar chart
- Product/category matrix
- City sales bar chart

## Important data-quality note
The source dataset contains repeated Order_ID values. The analysis therefore uses the generated `Transaction_ID` as the row-level transaction key while retaining `Order_ID` as a source field and audit flag.
