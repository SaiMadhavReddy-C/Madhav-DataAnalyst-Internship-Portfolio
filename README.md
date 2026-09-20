# ApexPlanet Data Analyst Internship Portfolio

## Overview

This repository is my consolidated portfolio for the ApexPlanet 60-Day Data Analytics Internship.

The project follows an end-to-end analytics workflow:

**Data Wrangling → Exploratory Data Analysis → Business Intelligence → KPI & Dashboard Development → Statistical Validation → Portfolio Storytelling**

The work uses a supplied sales transaction dataset and demonstrates practical skills in Python, Pandas, SQL, Excel, dashboarding, statistical analysis, and data storytelling.

---

## Dataset

- 1,000 supplied sales transaction rows
- 12 source columns
- 6 products across 5 categories
- Transaction dates spanning January 2025 to January 2026
- Total sales: **139,399,439.65**

---

## Project Tasks

### Task 1 — Data Immersion & Wrangling

**Focus:** Data quality assessment, cleaning, validation, and feature engineering.

Files:

- `Task-1-Data-Wrangling/Task1_Data_Dictionary.csv`
- `Task-1-Data-Wrangling/Task1_Data_Quality_Profile.csv`
- `Task-1-Data-Wrangling/Task1_Cleaning_Script.py`
- `Task-1-Data-Wrangling/ApexPlanet_Cleaned_Sales_Dataset.xlsx`

Key treatment:

- Missing Age values: median imputation
- Missing City values: `Unknown`
- Repeated `Order_ID` values: flagged rather than discarded
- Unique `Transaction_ID` created for transaction-level analysis
- Date parsing and time-based feature engineering completed
- Revenue calculation validated using Quantity × Unit_Price

---

### Task 2 — EDA & Business Intelligence

**Focus:** Exploratory analysis and business-question-driven investigation.

Files:

- `Task-2-EDA-Business-Intelligence/Task2_EDA_Report.md`
- `Task-2-EDA-Business-Intelligence/Task2_SQL_Business_Questions.sql`
- `Task-2-EDA-Business-Intelligence/Task2_EDA_Workbook.xlsx`
- `Task-2-EDA-Business-Intelligence/Task2_Static_Dashboard_Mockup.xlsx`

Business questions covered sales trends, category performance, product performance, city performance, gender, age groups, and the relationship between unit price and total sales.

---

### Task 3 — Deep-Dive & Interactive Dashboarding

**Focus:** KPI development, category/product analysis, and interactive dashboarding.

Files:

- `Task-3-Deep-Dive-Dashboard/Task3_Core_KPIs.csv`
- `Task-3-Deep-Dive-Dashboard/Task3_Category_Product_Deep_Dive.csv`
- `Task-3-Deep-Dive-Dashboard/Task3_Deep_Dive_Report.md`
- `Task-3-Deep-Dive-Dashboard/Task3_Interactive_Dashboard.html`

### Live Dashboard

[Open the Interactive Sales Dashboard](https://saimadhavreddy-c.github.io/Madhav-DataAnalyst-Internship-Portfolio/Task-3-Deep-Dive-Dashboard/Task3_Interactive_Dashboard.html)

Core portfolio metrics include:

- Total Sales: **139,399,439.65**
- Transactions: **1,000**
- Unique Customers: **947**
- Average Transaction Value: **139,399.44**
- Units Sold: **5,435**

---

### Task 4 — Data Storytelling & Statistical Validation

**Focus:** Statistical hypothesis testing and communicating analytical findings to stakeholders.

Files:

- `Task-4-Statistical-Validation/Task4_Hypothesis_Testing_Summary.md`
- `Task-4-Statistical-Validation/Task4_Statistical_Results.csv`
- `Task-4-Statistical-Validation/Task4_Final_Presentation.pptx`

The statistical analysis used a Welch independent two-sample t-test to examine whether the mean transaction sales differed between female and male transactions.

- Significance level: **α = 0.05**
- p-value: **0.495011**
- 95% confidence interval for Female − Male mean difference:
  **[-19,079.85, 9,231.58]**
- Statistical decision: **Fail to reject the null hypothesis**

The result is interpreted as statistical evidence from this dataset rather than as a causal explanation.

---

## Task 5 — Capstone Integration & Portfolio Finalization

This master repository consolidates the four analytical stages into one portfolio:

**Task 1 → Task 2 → Task 3 → Task 4 → Final Portfolio**

### Portfolio Navigation

- [Task 1 — Data Wrangling](./Task-1-Data-Wrangling/)
- [Task 2 — EDA & Business Intelligence](./Task-2-EDA-Business-Intelligence/)
- [Task 3 — Deep-Dive & Dashboard](./Task-3-Deep-Dive-Dashboard/)
- [Task 4 — Statistical Validation](./Task-4-Statistical-Validation/)
- [Task 5 — Final Portfolio](./Task-5-Final-Portfolio/)

### Final Deliverables

- [Interactive Dashboard](https://saimadhavreddy-c.github.io/Madhav-DataAnalyst-Internship-Portfolio/Task-3-Deep-Dive-Dashboard/Task3_Interactive_Dashboard.html)
- [Final Statistical Presentation](./Task-4-Statistical-Validation/Task4_Final_Presentation.pptx)
- [Task 5 LinkedIn Post Draft](./Task-5-Final-Portfolio/Task5_LinkedIn_Post_Draft.txt)
- [Task 5 Portfolio Walkthrough Script](./Task-5-Final-Portfolio/Task5_LinkedIn_Video_Script.txt)

---

## Key Analytical Highlights

- **Total Sales:** 139,399,439.65
- **Transactions:** 1,000
- **Unique Customers:** 947
- **Units Sold:** 5,435
- **Top Category by Sales:** Electronics — 50,778,581.70
- **Top Product by Sales:** Laptop — 25,443,008.51
- **Highest-Sales Month in 2025:** March 2025 — 13,059,899.94
- **Highest-Sales Age Group:** 35–44 — 32,800,713.26
- **Unit Price vs Total Sales Pearson Correlation:** 0.6863

These figures are descriptive results from the supplied dataset.

---

## Technical Skills Demonstrated

**Programming & Data Analysis**

- Python
- Pandas
- NumPy
- Excel
- SQL

**Analytics**

- Data Cleaning
- Data Quality Profiling
- Exploratory Data Analysis
- Business Question Development
- Data Validation
- KPI Design
- Statistical Hypothesis Testing

**Visualization & Communication**

- Interactive Dashboard Design
- Excel Dashboarding
- Plotly
- PowerPoint Data Storytelling
- Business Insight Communication

**Professional Workflow**

- Git
- GitHub
- Portfolio Organization
- Documentation

---

## Data Quality Note

The supplied source contains repeated `Order_ID` values even though the rows are not exact duplicates.

Rather than silently removing those records, the portfolio flags the repeated identifiers and creates a unique transaction-level identifier for analysis.

---

## Internship Learning Reflection

The project reinforced that effective analytics is not only about producing charts.

A reliable workflow begins with understanding and validating the data, continues with meaningful business questions and analysis, and ends with communicating evidence clearly enough for stakeholders to understand the result.

This portfolio represents that complete workflow from raw transaction data through analysis, dashboarding, statistical validation, and final presentation.
