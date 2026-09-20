import pandas as pd
import numpy as np

INPUT = "ApexPlanet_DataAnalytics_Dataset (1).xlsx"
OUTPUT = "ApexPlanet_Cleaned_Sales_Dataset.xlsx"

df = pd.read_excel(INPUT, sheet_name="Sales_Dataset")

# Parse and standardize
df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
for c in ["Order_ID","Customer_ID","Customer_Name","Gender","City","Product","Category"]:
    df[c] = df[c].astype("string").str.strip()

# Audit flags
df["Duplicate_Order_ID_Flag"] = df.duplicated("Order_ID", keep=False)
df["Missing_Age_Flag"] = df["Age"].isna()
df["Missing_City_Flag"] = df["City"].isna()

# Remediate missing values
df["Age"] = df["Age"].fillna(df["Age"].median())
df["City"] = df["City"].fillna("Unknown")

# Create row-level transaction ID because source Order_ID contains duplicates
df.insert(0, "Transaction_ID", [f"TXN{i:05d}" for i in range(1, len(df)+1)])

# Feature engineering
df["Year"] = df["Order_Date"].dt.year
df["Month"] = df["Order_Date"].dt.month
df["Month_Name"] = df["Order_Date"].dt.strftime("%b")
df["Revenue_Check"] = np.isclose(df["Quantity"] * df["Unit_Price"], df["Total_Sales"], atol=0.01)
df["Age_Group"] = pd.cut(
    df["Age"], bins=[17,24,34,44,54,65],
    labels=["18-24","25-34","35-44","45-54","55-65"],
    include_lowest=True
)

df.to_excel(OUTPUT, index=False)
print(f"Saved {len(df):,} analysis-ready rows to {OUTPUT}")
