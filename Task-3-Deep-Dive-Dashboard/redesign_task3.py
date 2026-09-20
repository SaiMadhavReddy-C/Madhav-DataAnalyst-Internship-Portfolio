from pathlib import Path
import pandas as pd
import json
import html

# ------------------------------------------------------------
# Load the actual ApexPlanet cleaned dataset
# ------------------------------------------------------------
base = Path(__file__).resolve().parent
dataset = base.parent / "Task-1-Data-Wrangling" / "ApexPlanet_Cleaned_Sales_Dataset.xlsx"

df = pd.read_excel(dataset)

df["Order_Date"] = pd.to_datetime(df["Order_Date"])

# ------------------------------------------------------------
# Actual dataset calculations
# ------------------------------------------------------------
total_sales = float(df["Total_Sales"].sum())
transactions = int(len(df))
unique_customers = int(df["Customer_ID"].nunique())
units_sold = int(df["Quantity"].sum())
aov = total_sales / transactions

# Monthly sales
monthly_df = (
    df.assign(Month=df["Order_Date"].dt.strftime("%b %Y"))
      .groupby("Month", sort=False)["Total_Sales"]
      .sum()
      .reset_index()
)

# Force chronological order
months = pd.date_range(
    df["Order_Date"].min().replace(day=1),
    df["Order_Date"].max().replace(day=1),
    freq="MS"
).strftime("%b %Y").tolist()

monthly_map = dict(zip(monthly_df["Month"], monthly_df["Total_Sales"]))
monthly_sales = [float(monthly_map.get(m, 0)) for m in months]

# Monthly transaction count
monthly_txn = (
    df.assign(Month=df["Order_Date"].dt.strftime("%b %Y"))
      .groupby("Month", sort=False)
      .size()
)
monthly_transactions = [int(monthly_txn.get(m, 0)) for m in months]

# Category performance
category_df = (
    df.groupby("Category")
      .agg(
          Sales=("Total_Sales", "sum"),
          Transactions=("Transaction_ID", "count"),
          Units=("Quantity", "sum")
      )
      .sort_values("Sales", ascending=False)
      .reset_index()
)

# Product performance
product_df = (
    df.groupby(["Category", "Product"])
      .agg(
          Sales=("Total_Sales", "sum"),
          Transactions=("Transaction_ID", "count"),
          Units=("Quantity", "sum"),
          Avg_Unit_Price=("Unit_Price", "mean")
      )
      .sort_values("Sales", ascending=False)
      .reset_index()
)

category_names = category_df["Category"].tolist()
category_sales = category_df["Sales"].round(2).tolist()

product_names = product_df["Product"].tolist()
product_sales = product_df["Sales"].round(2).tolist()
product_units = product_df["Units"].tolist()
product_prices = product_df["Avg_Unit_Price"].round(2).tolist()
product_categories = product_df["Category"].tolist()

# Sales share
category_share = (category_df["Sales"] / total_sales * 100).round(2).tolist()

# Top / lowest
top_category = category_df.iloc[0]
top_product = product_df.iloc[0]
lowest_product = product_df.iloc[-1]

# Correlation supported by the dataset
price_sales_corr = df["Unit_Price"].corr(df["Total_Sales"])

date_start = df["Order_Date"].min().strftime("%b %Y")
date_end = df["Order_Date"].max().strftime("%b %Y")

# Age group sales if available
age_group_html = ""
if "Age_Group" in df.columns:
    age_df = (
        df.groupby("Age_Group")["Total_Sales"]
          .sum()
          .sort_values(ascending=False)
          .reset_index()
    )
    age_rows = ""
    for _, r in age_df.iterrows():
        age_rows += f"""
        <div class="insight-row">
          <span>{html.escape(str(r["Age_Group"]))}</span>
          <strong>{r["Total_Sales"]:,.2f}</strong>
        </div>
        """
    age_group_html = f"""
      <div class="panel">
        <div class="panel-title">Sales by Age Group</div>
        <div class="insight-list">{age_rows}</div>
      </div>
    """

# ------------------------------------------------------------
# JSON data for Plotly
# ------------------------------------------------------------
months_js = json.dumps(months)
monthly_sales_js = json.dumps(monthly_sales)
monthly_transactions_js = json.dumps(monthly_transactions)

category_names_js = json.dumps(category_names)
category_sales_js = json.dumps(category_sales)
category_share_js = json.dumps(category_share)

product_names_js = json.dumps(product_names)
product_sales_js = json.dumps(product_sales)
product_units_js = json.dumps(product_units)
product_prices_js = json.dumps(product_prices)
product_categories_js = json.dumps(product_categories)

# ------------------------------------------------------------
# Dashboard HTML
# ------------------------------------------------------------
page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ApexPlanet — Sales Performance Dashboard</title>

<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>

<style>
:root {{
  --navy: #0b1f3a;
  --navy2: #102b50;
  --blue: #2878e8;
  --blue2: #4b9cff;
  --cyan: #23b7c9;
  --green: #18a874;
  --purple: #7657df;
  --orange: #f28a36;
  --red: #e95f75;
  --yellow: #eab83f;
  --bg: #f4f7fb;
  --card: #ffffff;
  --text: #10213b;
  --muted: #718096;
  --border: #e4eaf2;
  --shadow: 0 8px 24px rgba(15, 35, 65, 0.07);
}}

* {{
  box-sizing: border-box;
}}

body {{
  margin: 0;
  font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  background: var(--bg);
  color: var(--text);
}}

.app {{
  display: flex;
  min-height: 100vh;
}}

.sidebar {{
  width: 245px;
  background: linear-gradient(180deg, var(--navy), #07162b);
  color: white;
  padding: 24px 16px;
  position: fixed;
  inset: 0 auto 0 0;
  display: flex;
  flex-direction: column;
  z-index: 10;
}}

.brand {{
  padding: 4px 10px 26px;
  border-bottom: 1px solid rgba(255,255,255,.12);
}}

.brand-name {{
  font-size: 24px;
  font-weight: 800;
  letter-spacing: -.5px;
}}

.brand-name span {{
  color: #8ebcff;
}}

.brand-sub {{
  color: #b9d3f7;
  font-size: 12px;
  margin-top: 3px;
}}

.nav {{
  margin-top: 22px;
}}

.nav-item {{
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 13px 12px;
  margin-bottom: 7px;
  border-radius: 10px;
  color: #c6d5eb;
  font-size: 14px;
}}

.nav-item.active {{
  background: linear-gradient(90deg, #2479ed, #3e8eff);
  color: white;
  box-shadow: 0 7px 18px rgba(36,121,237,.28);
}}

.nav-icon {{
  width: 22px;
  text-align: center;
}}

.data-source {{
  margin-top: auto;
  border: 1px solid rgba(255,255,255,.18);
  border-radius: 12px;
  padding: 14px;
  color: #d9e6f7;
  font-size: 12px;
  line-height: 1.5;
}}

.main {{
  margin-left: 245px;
  width: calc(100% - 245px);
}}

.header {{
  background:
    radial-gradient(circle at 75% 20%, rgba(55,132,244,.22), transparent 28%),
    linear-gradient(120deg, var(--navy), var(--navy2));
  color: white;
  padding: 28px 36px 25px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}}

.header-title {{
  font-size: 32px;
  font-weight: 800;
  letter-spacing: -.8px;
}}

.header-sub {{
  margin-top: 5px;
  color: #bad2ef;
  font-size: 16px;
}}

.period {{
  border: 1px solid rgba(255,255,255,.24);
  border-radius: 10px;
  padding: 12px 16px;
  font-size: 13px;
  color: #dce9fa;
}}

.content {{
  padding: 24px 28px 30px;
}}

.kpis {{
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 15px;
  margin-bottom: 18px;
}}

.kpi {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 18px;
  box-shadow: var(--shadow);
  position: relative;
  overflow: hidden;
}}

.kpi::after {{
  content: "";
  position: absolute;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  right: -20px;
  top: -20px;
  background: rgba(40,120,232,.08);
}}

.kpi-label {{
  color: var(--muted);
  font-size: 13px;
  font-weight: 600;
}}

.kpi-value {{
  font-size: clamp(18px, 1.55vw, 24px);
  font-weight: 800;
  margin-top: 8px;
  color: var(--text);
  white-space: nowrap;
  letter-spacing: -0.5px;
}}

.kpi-note {{
  margin-top: 8px;
  font-size: 11px;
  color: var(--green);
  font-weight: 600;
}}

.grid-main {{
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 18px;
  margin-bottom: 18px;
}}

.grid-bottom {{
  display: grid;
  grid-template-columns: 1.1fr 1.1fr 1fr;
  gap: 18px;
  margin-bottom: 18px;
}}

.panel {{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 18px;
  box-shadow: var(--shadow);
  min-width: 0;
}}

.panel-title {{
  font-size: 16px;
  font-weight: 750;
  margin-bottom: 12px;
}}

.chart {{
  width: 100%;
  height: 330px;
}}

.chart-small {{
  width: 100%;
  height: 310px;
}}

.insights {{
  background: linear-gradient(135deg, #f7fbff, #ffffff);
  border: 1px solid #dce8f6;
  border-radius: 14px;
  padding: 20px;
  margin-bottom: 18px;
  box-shadow: var(--shadow);
}}

.insight-grid {{
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 0;
}}

.insight {{
  padding: 8px 18px;
  border-right: 1px solid var(--border);
}}

.insight:last-child {{
  border-right: 0;
}}

.badge {{
  width: 29px;
  height: 29px;
  border-radius: 50%;
  background: var(--blue);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 12px;
  margin-bottom: 10px;
}}

.insight h4 {{
  margin: 0 0 7px;
  font-size: 13px;
}}

.insight p {{
  margin: 0;
  color: var(--muted);
  font-size: 11px;
  line-height: 1.5;
}}

.insight-list {{
  display: flex;
  flex-direction: column;
  gap: 9px;
}}

.insight-row {{
  display: flex;
  justify-content: space-between;
  padding: 9px 10px;
  border-radius: 8px;
  background: #f7f9fc;
  font-size: 12px;
}}

.footer {{
  background: var(--navy);
  color: #b9cce5;
  padding: 13px 28px;
  font-size: 11px;
  display: flex;
  justify-content: space-between;
}}

@media (max-width: 1150px) {{
  .sidebar {{ width: 210px; }}
  .main {{ margin-left: 210px; width: calc(100% - 210px); }}
  .kpis {{ grid-template-columns: repeat(3, 1fr); }}
  .insight-grid {{ grid-template-columns: repeat(3, 1fr); }}
  .insight:nth-child(3) {{ border-right: 0; }}
}}

@media (max-width: 850px) {{
  .sidebar {{
    position: relative;
    width: 100%;
    min-height: auto;
  }}
  .app {{ display: block; }}
  .main {{
    margin-left: 0;
    width: 100%;
  }}
  .nav {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 6px;
  }}
  .nav-item {{ margin: 0; }}
  .grid-main, .grid-bottom {{
    grid-template-columns: 1fr;
  }}
  .header {{
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }}
}}

@media (max-width: 600px) {{
  .content {{ padding: 15px; }}
  .header {{ padding: 22px 18px; }}
  .header-title {{ font-size: 24px; }}
  .kpis {{ grid-template-columns: 1fr 1fr; }}
  .insight-grid {{ grid-template-columns: 1fr; }}
  .insight {{ border-right: 0; border-bottom: 1px solid var(--border); padding: 12px 0; }}
  .insight:last-child {{ border-bottom: 0; }}
  .nav {{ grid-template-columns: 1fr 1fr; }}
  .footer {{ flex-direction: column; gap: 5px; }}
}}
</style>
</head>

<body>
<div class="app">

  <aside class="sidebar">
    <div class="brand">
      <div class="brand-name">Apex<span>Planet</span></div>
      <div class="brand-sub">Data Analytics Internship</div>
    </div>

    <nav class="nav">
      <div class="nav-item active"><span class="nav-icon">⌂</span> Overview</div>
      <div class="nav-item"><span class="nav-icon">↗</span> Sales Trend</div>
      <div class="nav-item"><span class="nav-icon">◆</span> Category Analysis</div>
      <div class="nav-item"><span class="nav-icon">▣</span> Product Analysis</div>
      <div class="nav-item"><span class="nav-icon">●</span> Customer Insights</div>
      <div class="nav-item"><span class="nav-icon">▤</span> Transaction Insights</div>
    </nav>

    <div class="data-source">
      <strong>Data Source</strong><br><br>
      ApexPlanet Internship Dataset<br>
      Sales Data 2025
    </div>
  </aside>

  <main class="main">

    <header class="header">
      <div>
        <div class="header-title">Sales Performance Dashboard</div>
        <div class="header-sub">Task 3 — Deep Dive Analysis &nbsp; | &nbsp; Uncovering Trends. Driving Insights.</div>
      </div>
      <div class="period">▣ &nbsp; {date_start} – {date_end}</div>
    </header>

    <section class="content">

      <div class="kpis">

        <div class="kpi">
          <div class="kpi-label">Total Sales</div>
          <div class="kpi-value">{total_sales:,.2f}</div>
          <div class="kpi-note">Overall revenue scale</div>
        </div>

        <div class="kpi">
          <div class="kpi-label">Transactions</div>
          <div class="kpi-value">{transactions:,}</div>
          <div class="kpi-note">Transaction volume</div>
        </div>

        <div class="kpi">
          <div class="kpi-label">Unique Customers</div>
          <div class="kpi-value">{unique_customers:,}</div>
          <div class="kpi-note">Customer reach</div>
        </div>

        <div class="kpi">
          <div class="kpi-label">Average Transaction</div>
          <div class="kpi-value">{aov:,.2f}</div>
          <div class="kpi-note">Average order value</div>
        </div>

        <div class="kpi">
          <div class="kpi-label">Units Sold</div>
          <div class="kpi-value">{units_sold:,}</div>
          <div class="kpi-note">Sales volume</div>
        </div>

      </div>

      <div class="grid-main">

        <div class="panel">
          <div class="panel-title">Monthly Sales Trend</div>
          <div id="monthlyChart" class="chart"></div>
        </div>

        <div class="panel">
          <div class="panel-title">Sales by Category</div>
          <div id="categoryChart" class="chart"></div>
        </div>

      </div>

      <div class="grid-bottom">

        <div class="panel">
          <div class="panel-title">Product Sales Performance</div>
          <div id="productChart" class="chart-small"></div>
        </div>

        <div class="panel">
          <div class="panel-title">Units Sold by Product</div>
          <div id="unitsChart" class="chart-small"></div>
        </div>

        <div class="panel">
          <div class="panel-title">Average Unit Price</div>
          <div id="priceChart" class="chart-small"></div>
        </div>

      </div>

      <div class="grid-bottom">

        <div class="panel">
          <div class="panel-title">Category Sales Share</div>
          <div id="shareChart" class="chart-small"></div>
        </div>

        <div class="panel">
          <div class="panel-title">Product Contribution</div>
          <div id="productContribution" class="chart-small"></div>
        </div>

        <div class="panel">
          <div class="panel-title">Key Metrics</div>
          <div class="insight-list">
            <div class="insight-row"><span>Top Category</span><strong>{html.escape(str(top_category["Category"]))}</strong></div>
            <div class="insight-row"><span>Top Product</span><strong>{html.escape(str(top_product["Product"]))}</strong></div>
            <div class="insight-row"><span>Top Product Sales</span><strong>{top_product["Sales"]:,.2f}</strong></div>
            <div class="insight-row"><span>Lowest Product Sales</span><strong>{lowest_product["Sales"]:,.2f}</strong></div>
            <div class="insight-row"><span>Price/Sales Correlation</span><strong>{price_sales_corr:.4f}</strong></div>
          </div>
        </div>

      </div>

      {age_group_html}

      <div class="insights">
        <div class="panel-title">Key Insights</div>

        <div class="insight-grid">

          <div class="insight">
            <div class="badge">1</div>
            <h4>Category Leadership</h4>
            <p>{html.escape(str(top_category["Category"]))} leads category sales with {top_category["Sales"]:,.2f}, representing {category_share[0]:.2f}% of total sales.</p>
          </div>

          <div class="insight">
            <div class="badge">2</div>
            <h4>Top Product</h4>
            <p>{html.escape(str(top_product["Product"]))} is the highest-selling product at {top_product["Sales"]:,.2f}.</p>
          </div>

          <div class="insight">
            <div class="badge">3</div>
            <h4>Customer Reach</h4>
            <p>{unique_customers:,} unique customers generated {transactions:,} transactions, providing broad customer coverage.</p>
          </div>

          <div class="insight">
            <div class="badge">4</div>
            <h4>Transaction Value</h4>
            <p>The average transaction value is {aov:,.2f} across the {transactions:,} recorded transactions.</p>
          </div>

          <div class="insight">
            <div class="badge">5</div>
            <h4>Price & Sales Association</h4>
            <p>The Pearson correlation between Unit Price and Total Sales is {price_sales_corr:.4f}; this indicates association, not causation.</p>
          </div>

        </div>
      </div>

    </section>

    <footer class="footer">
      <span>ApexPlanet Data Analytics Internship — Task 3</span>
      <span>Data source: ApexPlanet Internship Dataset &nbsp;|&nbsp; Built with Plotly.js</span>
    </footer>

  </main>
</div>

<script>
const months = {months_js};
const monthlySales = {monthly_sales_js};
const monthlyTransactions = {monthly_transactions_js};

const categoryNames = {category_names_js};
const categorySales = {category_sales_js};
const categoryShare = {category_share_js};

const productNames = {product_names_js};
const productSales = {product_sales_js};
const productUnits = {product_units_js};
const productPrices = {product_prices_js};
const productCategories = {product_categories_js};

const common = {{
  font: {{
    family: "Inter, Arial, sans-serif",
    color: "#10213b"
  }},
  paper_bgcolor: "rgba(0,0,0,0)",
  plot_bgcolor: "rgba(0,0,0,0)",
  margin: {{l: 50, r: 20, t: 10, b: 50}},
  hoverlabel: {{bgcolor: "#10213b", font: {{color: "white"}}}}
}};

Plotly.newPlot("monthlyChart", [
  {{
    x: months,
    y: monthlySales,
    type: "bar",
    name: "Sales",
    marker: {{color: "#2878e8"}},
    hovertemplate: "%{{x}}<br>Sales: %{{y:,.2f}}<extra></extra>"
  }},
  {{
    x: months,
    y: monthlyTransactions,
    type: "scatter",
    mode: "lines+markers",
    name: "Transactions",
    yaxis: "y2",
    line: {{color: "#18a874", width: 3}},
    marker: {{size: 7}},
    hovertemplate: "%{{x}}<br>Transactions: %{{y}}<extra></extra>"
  }}
], {{
  ...common,
  barmode: "group",
  legend: {{orientation: "h", y: 1.12}},
  yaxis: {{title: "Sales", tickformat: "~s"}},
  yaxis2: {{
    title: "Transactions",
    overlaying: "y",
    side: "right"
  }},
  xaxis: {{tickangle: -35, tickfont: {{size: 10}}}},
  hovermode: "x unified"
}}, {{responsive: true, displaylogo: false}});

Plotly.newPlot("categoryChart", [{{
  labels: categoryNames,
  values: categorySales,
  type: "pie",
  hole: 0.58,
  textinfo: "percent",
  hovertemplate: "%{{label}}<br>Sales: %{{value:,.2f}}<br>Share: %{{percent}}<extra></extra>"
}}], {{
  ...common,
  margin: {{l: 10, r: 10, t: 10, b: 10}},
  showlegend: true,
  legend: {{font: {{size: 11}}}}
}}, {{responsive: true, displaylogo: false}});

Plotly.newPlot("productChart", [{{
  x: productSales,
  y: productNames,
  type: "bar",
  orientation: "h",
  marker: {{color: "#4b8ff5"}},
  text: productSales.map(v => v.toLocaleString(undefined, {{maximumFractionDigits: 0}})),
  textposition: "outside",
  hovertemplate: "%{{y}}<br>Sales: %{{x:,.2f}}<extra></extra>"
}}], {{
  ...common,
  margin: {{l: 85, r: 70, t: 10, b: 40}},
  yaxis: {{autorange: "reversed"}}
}}, {{responsive: true, displaylogo: false}});

Plotly.newPlot("unitsChart", [{{
  x: productNames,
  y: productUnits,
  type: "bar",
  marker: {{color: "#23b7c9"}},
  hovertemplate: "%{{x}}<br>Units: %{{y:,}}<extra></extra>"
}}], {{
  ...common,
  margin: {{l: 50, r: 20, t: 10, b: 75}},
  xaxis: {{tickangle: -35}}
}}, {{responsive: true, displaylogo: false}});

Plotly.newPlot("priceChart", [{{
  x: productNames,
  y: productPrices,
  type: "bar",
  marker: {{color: "#f28a36"}},
  hovertemplate: "%{{x}}<br>Avg Unit Price: %{{y:,.2f}}<extra></extra>"
}}], {{
  ...common,
  margin: {{l: 55, r: 20, t: 10, b: 75}},
  xaxis: {{tickangle: -35}}
}}, {{responsive: true, displaylogo: false}});

Plotly.newPlot("shareChart", [{{
  x: categoryNames,
  y: categoryShare,
  type: "bar",
  marker: {{color: "#7657df"}},
  text: categoryShare.map(v => v.toFixed(2) + "%"),
  textposition: "outside",
  hovertemplate: "%{{x}}<br>Share: %{{y:.2f}}%<extra></extra>"
}}], {{
  ...common,
  margin: {{l: 45, r: 20, t: 10, b: 80}},
  yaxis: {{title: "Share %"}},
  xaxis: {{tickangle: -30}}
}}, {{responsive: true, displaylogo: false}});

Plotly.newPlot("productContribution", [{{
  x: productNames,
  y: productSales,
  type: "scatter",
  mode: "markers",
  marker: {{
    size: productSales.map(v => Math.max(18, Math.sqrt(v) / 130)),
    color: productSales,
    colorscale: "Blues",
    showscale: false,
    line: {{width: 1, color: "#ffffff"}}
  }},
  text: productCategories,
  hovertemplate: "<b>%{{x}}</b><br>Category: %{{text}}<br>Sales: %{{y:,.2f}}<extra></extra>"
}}], {{
  ...common,
  margin: {{l: 55, r: 20, t: 10, b: 65}},
  xaxis: {{tickangle: -35}},
  yaxis: {{title: "Sales"}}
}}, {{responsive: true, displaylogo: false}});
</script>

</body>
</html>
"""

output = base / "Task3_Interactive_Dashboard.html"
output.write_text(page, encoding="utf-8")

print("SUCCESS")
print(f"Dashboard rebuilt: {output}")
print(f"Rows: {transactions:,}")
print(f"Total Sales: {total_sales:,.2f}")
print(f"Unique Customers: {unique_customers:,}")
print(f"Units Sold: {units_sold:,}")
print(f"AOV: {aov:,.2f}")
print(f"Date range: {df['Order_Date'].min():%b %Y} - {df['Order_Date'].max():%b %Y}")
