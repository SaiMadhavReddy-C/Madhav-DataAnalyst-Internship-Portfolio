# ApexPlanet Data Analyst Internship Portfolio

## Overview
This repository consolidates the complete 60-day Data Analytics internship workflow specified by ApexPlanet: Data Immersion & Wrangling, EDA & Business Intelligence, Deep-Dive Analysis & Interactive Dashboarding, Data Storytelling & Statistical Validation, and Capstone Portfolio Finalization.

## Dataset
- 1,000 supplied sales transaction rows
- 12 source columns
- 2025 transaction dates
- 6 products across 5 categories

## Tasks

### Task 1 — Data Immersion & Wrangling
Files:
- `Task1_Data_Dictionary.csv`
- `Task1_Data_Quality_Profile.csv`
- `Task1_Cleaning_Script.py`
- `ApexPlanet_Cleaned_Sales_Dataset.xlsx`

Key treatment:
- Missing Age: median imputation
- Missing City: `Unknown`
- Repeated `Order_ID`: flagged; row-level `Transaction_ID` created
- Date parsing and feature engineering completed
- Revenue formula validated

### Task 2 — EDA & Business Intelligence
Files:
- `Task2_EDA_Report.md`
- `Task2_SQL_Business_Questions.sql`
- `Task2_EDA_Workbook.xlsx`
- `Task2_Static_Dashboard_Mockup.xlsx`

### Task 3 — Deep-Dive & Interactive Dashboarding
Files:
- `Task3_Core_KPIs.csv`
- `Task3_Category_Product_Deep_Dive.csv`
- `Task3_Deep_Dive_Report.md`
- `Task3_Interactive_Dashboard.html`

### Task 4 — Data Storytelling & Statistical Validation
Files:
- `Task4_Hypothesis_Testing_Summary.md`
- `Task4_Statistical_Results.csv`
- `Task4_Final_Presentation.pptx`

### Task 5 — Capstone Integration & Portfolio Finalization
This README is the master portfolio homepage. Add links to the four task repositories (if separate), the final dashboard, and LinkedIn videos after publishing them.

## Internship Submission Checklist
According to the internship brief, each task should be completed before submission, screen-recorded, uploaded to LinkedIn Featured, and the video link copied. Project files should be uploaded to a public GitHub repository, and the relevant task should then be submitted through the ApexPlanet internship portal. After submission, open the next task and repeat.

## Technical Skills Demonstrated
Python, Pandas, NumPy, Excel, SQL, exploratory data analysis, data cleaning, data validation, KPI design, dashboard design, statistical hypothesis testing, PowerPoint storytelling, Git/GitHub portfolio organization.

## Data-quality note
The supplied source has repeated `Order_ID` values even though the rows are not exact duplicates. This portfolio does not silently discard those records; it flags the condition and creates a unique transaction-level identifier for analysis.
