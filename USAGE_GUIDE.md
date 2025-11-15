# Data Lens - Usage Guide

Comprehensive examples and workflows for analyzing spreadsheets with natural language.

---

## Table of Contents

- [Quick Start](#quick-start)
- [Common Workflows](#common-workflows)
- [Query Patterns](#query-patterns)
- [Example Questions](#example-questions)
- [Tips & Best Practices](#tips--best-practices)

---

## Quick Start

### Load Your First Spreadsheet

```
You: Load sales_data.xlsx

Claude: I've loaded your file. It contains 1 sheet named "sales" with 250 rows.

Columns found:
- date (DATE)
- region (VARCHAR)
- product (VARCHAR)
- quantity (BIGINT)
- unit_price (DOUBLE)
- total_amount (DOUBLE)

What would you like to know about this data?
```

### Ask Your First Question

```
You: What's the total revenue?

Claude: I'll calculate that for you.

Total revenue: $1,847,293.50

This represents 250 transactions across all regions and products.
```

---

## Common Workflows

### Workflow 1: Business Analysis

**Scenario:** Analyzing sales data to understand business performance.

```
You: Load Q4_sales_2024.xlsx

Claude: Loaded! Found 3 sheets: sales, customers, products
I've created 3 tables: q4_sales_2024, customers, products

---

You: Show me revenue by region

Claude: Here's the revenue breakdown by region:

| Region         | Revenue      | Orders | Avg Order Value |
|----------------|--------------|--------|-----------------|
| North America  | $2,456,789   | 1,234  | $1,991         |
| Europe         | $1,892,345   | 987    | $1,917         |
| Asia Pacific   | $3,124,567   | 1,456  | $2,146         |
| Latin America  | $876,234     | 432    | $2,028         |

**Key Insights:**
- Asia Pacific is your top-performing region (43% of revenue)
- Highest average order value: Asia Pacific ($2,146)
- Total orders: 4,109 across all regions

---

You: Which products are best sellers in Asia Pacific?

Claude: Top 5 products in Asia Pacific by revenue:

1. **Premium Widget Pro** - $487,234 (312 units)
2. **Enterprise Dashboard** - $398,765 (89 units)
3. **Professional Suite** - $287,456 (145 units)
4. **Standard Widget** - $245,123 (567 units)
5. **Analytics Module** - $198,432 (234 units)

Premium Widget Pro is your clear winner, generating 15.6% of Asia Pacific revenue.

---

You: What's the month-over-month growth trend?

Claude: Monthly revenue trend for Q4:

| Month    | Revenue    | vs Previous | Growth % |
|----------|------------|-------------|----------|
| October  | $2,234,567 | -           | -        |
| November | $2,567,890 | +$333,323   | +14.9%   |
| December | $2,847,478 | +$279,588   | +10.9%   |

You're seeing consistent growth throughout Q4:
- October to November: +14.9%
- November to December: +10.9%
- Q4 total growth: +27.4%

Strong finish to the year!
```

### Workflow 2: Data Exploration

**Scenario:** Exploring a new dataset to understand its structure and contents.

```
You: I've just received customer_data.csv. Help me understand what's in it.

Claude: I've loaded customer_data.csv. Let me analyze it for you.

**Dataset Overview:**
- Total customers: 2,847
- Columns: 8
- Date range: 2022-01-15 to 2024-11-14

**Column breakdown:**
1. customer_id (TEXT) - Unique identifiers
2. signup_date (DATE) - When they joined
3. email (TEXT) - Contact information
4. age (BIGINT) - Customer age
5. country (TEXT) - Location
6. plan_type (TEXT) - Subscription tier
7. monthly_value (DOUBLE) - Revenue per month
8. status (TEXT) - Active, Churned, etc.

**Sample data (first 3 rows):**
| customer_id | signup_date | age | country | plan_type  | monthly_value | status |
|-------------|-------------|-----|---------|------------|---------------|--------|
| CUST-001    | 2022-03-15  | 34  | USA     | Premium    | $49.99        | Active |
| CUST-002    | 2022-03-16  | 28  | Canada  | Standard   | $19.99        | Active |
| CUST-003    | 2022-03-16  | 45  | UK      | Enterprise | $199.99       | Active |

What aspect would you like to explore?

---

You: What are the key demographics?

Claude: **Customer Demographics Analysis:**

**Age Distribution:**
- 18-24: 423 customers (14.9%)
- 25-34: 1,189 customers (41.8%) ⭐ Largest group
- 35-44: 734 customers (25.8%)
- 45-54: 389 customers (13.7%)
- 55+: 112 customers (3.9%)

Average customer age: 33.4 years

**Geographic Distribution:**
- USA: 1,245 customers (43.7%)
- Canada: 334 customers (11.7%)
- UK: 298 customers (10.5%)
- Germany: 245 customers (8.6%)
- Other: 725 customers (25.5%)

**Plan Type Distribution:**
- Standard: 1,523 customers (53.5%)
- Premium: 987 customers (34.7%)
- Enterprise: 337 customers (11.8%)

---

You: How much revenue comes from each plan type?

Claude: **Revenue by Plan Type:**

| Plan       | Customers | Monthly Revenue | Avg per Customer | Total % |
|------------|-----------|-----------------|------------------|---------|
| Enterprise | 337       | $67,396         | $199.99          | 52.8%   |
| Premium    | 987       | $49,350         | $49.99           | 38.7%   |
| Standard   | 1,523     | $30,435         | $19.99           | 23.9%   |

**Key Insight:** Enterprise customers are only 11.8% of your base but generate 52.8% of monthly revenue. This is your highest-value segment!

---

You: Show me signup trends over time

Claude: **Monthly Signups Trend:**

Recent months:
- Sep 2024: 234 signups
- Oct 2024: 267 signups (+14.1%)
- Nov 2024: 198 signups (-25.8%) [partial month]

**Quarterly Growth:**
- Q1 2024: 567 signups
- Q2 2024: 634 signups (+11.8%)
- Q3 2024: 723 signups (+14.0%)
- Q4 2024: 699 signups (projected: ~800)

You're on track for your best year yet! Q3 was your strongest quarter.
```

### Workflow 3: Report Generation

**Scenario:** Creating a weekly executive summary from multiple data sources.

```
You: Load this week's metrics: sales.csv, traffic.csv, conversions.csv

Claude: Loaded 3 files:
- sales: 1,234 rows (weekly sales data)
- traffic: 5,678 rows (website visits)
- conversions: 234 rows (purchases)

All ready for analysis.

---

You: Give me the executive summary for this week

Claude: **Weekly Executive Summary**
*Week of November 11-17, 2024*

**Sales Performance:**
- Total Revenue: $234,567 (↑ 12.3% vs last week)
- Average Order Value: $98.50 (↑ 3.2%)
- Total Orders: 2,382 (↑ 8.9%)
- Top Product: Premium Widget ($45,678)

**Traffic & Engagement:**
- Unique Visitors: 45,678 (↑ 15.2%)
- Page Views: 187,234 (↑ 18.7%)
- Avg Session Duration: 3m 42s (↑ 8.3%)
- Bounce Rate: 42.3% (↓ 2.1%)

**Conversion Metrics:**
- Conversion Rate: 5.2% (↑ 0.3pp)
- Cart Abandonment: 67.8% (↓ 1.2pp)
- Email Signups: 1,234 (↑ 23.4%)

**Key Highlights:**
✅ Revenue growth accelerating (12.3%)
✅ Traffic quality improving (lower bounce rate)
✅ Conversion rate at yearly high (5.2%)
⚠️ Cart abandonment still high - needs attention

---

You: Which traffic sources drove the most conversions?

Claude: **Conversion by Traffic Source:**

| Source        | Visitors | Conversions | Conv Rate | Revenue   |
|---------------|----------|-------------|-----------|-----------|
| Google Ads    | 12,345   | 987         | 8.0%      | $97,234   |
| Email         | 8,765    | 654         | 7.5%      | $64,321   |
| Organic       | 15,234   | 523         | 3.4%      | $51,467   |
| Social Media  | 6,789    | 198         | 2.9%      | $19,478   |
| Direct        | 2,545    | 20          | 0.8%      | $2,067    |

**Insights:**
- Google Ads has highest conversion rate (8.0%) and ROI
- Email performing well (7.5% conversion)
- Organic has most volume but lower conversion (3.4%)
- Consider increasing Google Ads and Email budget

---

You: Create a comparison table: this week vs last week

Claude: **Week-over-Week Comparison:**

| Metric                | Last Week  | This Week  | Change    | % Change |
|-----------------------|------------|------------|-----------|----------|
| Revenue               | $208,934   | $234,567   | +$25,633  | +12.3%   |
| Orders                | 2,187      | 2,382      | +195      | +8.9%    |
| AOV                   | $95.51     | $98.50     | +$2.99    | +3.1%    |
| Unique Visitors       | 39,678     | 45,678     | +6,000    | +15.1%   |
| Conversion Rate       | 4.9%       | 5.2%       | +0.3pp    | +6.1%    |
| Email Signups         | 998        | 1,234      | +236      | +23.7%   |
| Cart Abandonment Rate | 69.0%      | 67.8%      | -1.2pp    | -1.7%    |

**Summary:** All key metrics trending positive. Strong week!
```

### Workflow 4: Ad-Hoc Analysis

**Scenario:** Quick questions about your data throughout the day.

```
9:00 AM
You: Load today's orders.csv. How many orders so far?

Claude: 47 orders as of 9:00 AM, totaling $4,523.67
Average order value: $96.25

---

11:30 AM
You: Update - how many now?

Claude: [Reloads file] 89 orders, totaling $8,234.50
+42 orders in the last 2.5 hours

---

2:15 PM
You: Which product is selling best today?

Claude: Top seller today: "Premium Widget Pro"
- 23 units sold
- $2,156 revenue
- 25.8% of total sales

---

4:45 PM
You: Final numbers for today?

Claude: **Daily Summary** (as of 4:45 PM)

Total Orders: 127
Total Revenue: $12,456.78
Average Order Value: $98.08

Top 3 Products:
1. Premium Widget Pro - $2,876 (23.1%)
2. Standard Widget - $1,987 (15.9%)
3. Widget Plus - $1,654 (13.3%)

Compared to yesterday: +15.2% revenue, +8.7% orders
```

---

## Query Patterns

### Aggregation Queries

```
Basic totals:
- "What's the total revenue?"
- "How many orders do we have?"
- "What's the sum of all quantities?"

Averages:
- "What's the average order value?"
- "Average price per product?"
- "Mean customer age?"

Min/Max:
- "What's the highest sale amount?"
- "Lowest price in the catalog?"
- "Most recent order date?"

Counts:
- "How many unique customers?"
- "Count of products by category?"
- "Number of orders per day?"
```

### Grouping & Breakdown

```
By category:
- "Revenue by region"
- "Sales by product category"
- "Orders by customer segment"

By time:
- "Monthly revenue trend"
- "Daily order counts"
- "Year-over-year comparison"

Multiple dimensions:
- "Revenue by region and product"
- "Average order value by month and customer type"
- "Top products by region"
```

### Filtering & Conditions

```
Simple filters:
- "Show only premium customers"
- "Orders above $1000"
- "Products in Electronics category"

Date filters:
- "Sales from last month"
- "Orders this year"
- "Transactions between Jan and Mar"

Multiple conditions:
- "Premium customers in USA with orders > $500"
- "Products in Electronics with price < $100"
- "Orders from Q4 with status 'Completed'"
```

### Sorting & Ranking

```
Top N:
- "Top 5 customers by revenue"
- "Best-selling products"
- "Highest revenue regions"

Bottom N:
- "Lowest performing products"
- "Smallest orders"
- "Least active customers"

With percentages:
- "Top 10 products with their revenue share"
- "Top regions by percentage of total sales"
```

### Comparisons

```
Period comparisons:
- "This month vs last month revenue"
- "Year-over-year growth"
- "Q3 vs Q4 performance"

Segment comparisons:
- "Premium vs Standard plan revenue"
- "North America vs Europe sales"
- "Product category comparison"

Percentage changes:
- "Month-over-month growth rate"
- "Percentage change in orders"
- "Growth rate by region"
```

---

## Example Questions

### Sales & Revenue

```
"What's our total revenue?"
"Show me revenue by month"
"Which product generates the most revenue?"
"What's the average order value?"
"Revenue breakdown by region"
"Top 10 customers by total spend"
"Monthly recurring revenue (MRR)"
"Year-over-year revenue growth"
```

### Products & Inventory

```
"Which products are best sellers?"
"Show me product performance by category"
"What's the average price per product?"
"Which items have the highest margins?"
"Product sales ranking"
"Inventory turnover rate"
"Products below reorder level"
"Slow-moving inventory"
```

### Customers

```
"How many active customers?"
"Customer acquisition by month"
"Average customer lifetime value"
"Customer segmentation by spend"
"Retention rate this quarter"
"Churn rate calculation"
"Top 20% of customers by revenue"
"New vs returning customer split"
```

### Time-Based Analysis

```
"Daily sales trend"
"Monthly growth rate"
"Seasonal patterns"
"Week-over-week comparison"
"Best performing day of week"
"Hourly sales distribution"
"Quarter-over-quarter growth"
"Year-to-date performance"
```

### Geographic Analysis

```
"Sales by country"
"Revenue by region"
"Top performing cities"
"Geographic distribution of customers"
"Regional growth comparison"
"Market penetration by state"
"International vs domestic sales"
```

---

## Tips & Best Practices

### Loading Files

**Best Practices:**
```
✅ Use descriptive file names: sales_q4_2024.xlsx
✅ Keep column names simple: "revenue" not "Total Revenue (USD)"
✅ Ensure consistent data types in columns
✅ Remove empty rows/columns before loading

❌ Avoid special characters in file names
❌ Don't use merged cells in Excel
❌ Avoid multiple header rows
❌ Don't mix data types in same column
```

### Asking Questions

**Be Specific:**
```
❌ "Show me the data"
✅ "Show me revenue by month for 2024"

❌ "What about customers?"
✅ "How many customers signed up this quarter?"

❌ "Any trends?"
✅ "What's the month-over-month growth trend in sales?"
```

**Start Simple, Then Drill Down:**
```
1. "What's the total revenue?" → $2.4M
2. "Break that down by region" → NA: $1.2M, EU: $800K, APAC: $400K
3. "Which products sell best in North America?" → Widget Pro leads
4. "Show me Widget Pro sales trend over time" → Growing 15% monthly
```

**Use Natural Language:**
```
✅ "What are my top 5 products?"
✅ "Show me customers who spent more than $1000"
✅ "Compare this month to last month"
✅ "Which region has the highest growth?"
```

### Working with Multiple Sheets

**Excel files with multiple sheets:**
```
When you load: sales_report.xlsx

Data Lens creates separate tables:
- sales_report (from "Sales" sheet)
- products (from "Products" sheet)
- customers (from "Customers" sheet)

Then you can query each:
"What's in the sales_report table?"
"Show me all products from the products table"
```

### Performance Tips

**For Large Files:**
```
✅ Use filters to narrow results: "Top 10" instead of "All"
✅ Ask for summaries instead of raw data
✅ Use date ranges to limit scope
✅ Request specific columns, not "SELECT *"

Example:
❌ "Show me all transactions" (slow on 100K rows)
✅ "What's the total transaction value?" (fast aggregation)
✅ "Show me top 20 transactions" (limited result set)
```

### Common Mistakes to Avoid

**SQL Limitations:**
```
❌ "Delete all orders from 2023" - Not allowed (read-only)
❌ "Drop the sales table" - Not allowed (destructive)
❌ "Update prices by 10%" - Not allowed (modification)

✅ All SELECT queries are allowed
✅ Aggregations, joins, filtering all work
✅ Complex analytical queries supported
```

**File Loading:**
```
❌ Loading file while another is active - Replaces previous data
✅ One file active at a time
✅ To switch files, just load the new one
```

**Column Name Issues:**
```
❌ "Show revenue from 'Total Revenue (USD)'" - Complex name
✅ Use exact column name from schema
✅ Or simplify: Ask Claude to "show me revenue" (it figures it out)
```

---

## Advanced Patterns

### Complex Calculations

```
You: Calculate the 80/20 rule - what percentage of customers generate 80% of revenue?

Claude: I'll analyze your customer revenue distribution.

**Pareto Analysis (80/20 Rule):**
- Total customers: 2,847
- Top 20% customers (569): Generate 76.8% of revenue ($1.84M)
- Top 10% customers (285): Generate 58.3% of revenue ($1.40M)
- Top 5% customers (142): Generate 41.2% of revenue ($988K)

Your top 142 customers (5%) drive over 40% of revenue. Key accounts to protect!
```

### Cohort Analysis

```
You: Show me customer retention by signup month

Claude: **Monthly Cohort Retention:**

| Signup Month | Customers | Still Active | Retention % |
|--------------|-----------|--------------|-------------|
| Jan 2024     | 234       | 189          | 80.8%       |
| Feb 2024     | 267       | 223          | 83.5%       |
| Mar 2024     | 298       | 256          | 85.9%       |
| Apr 2024     | 245       | 218          | 89.0%       |

Retention is improving! April cohort has best retention at 89%.
```

### Statistical Analysis

```
You: What's the distribution of order values? Any outliers?

Claude: **Order Value Distribution:**

Statistical Summary:
- Mean: $98.50
- Median: $67.30
- Std Dev: $145.23
- Min: $5.00
- Max: $2,450.00

Distribution:
- $0-$50: 1,234 orders (34.2%)
- $51-$100: 1,567 orders (43.4%)
- $101-$200: 654 orders (18.1%)
- $201-$500: 123 orders (3.4%)
- $500+: 32 orders (0.9%)

**Outliers detected:**
12 orders above $1,000 (3x std dev from mean)
These might be bulk/enterprise orders - worth investigating.
```

---

## Troubleshooting Queries

**"No results found"**
```
Check:
- Is the file loaded? Ask: "What tables are available?"
- Are column names correct? Ask: "What columns are in the table?"
- Is the filter too restrictive? Try broader query first
```

**"Column not found"**
```
Solution:
- Ask: "Show me the schema" to see exact column names
- Column names are case-sensitive
- Use exact name from schema
```

**"Query too complex"**
```
Break it down:
Instead of: "Show revenue by product by region by month with growth rates"
Try:
1. "Show revenue by product and region"
2. Then: "Now add month"
3. Then: "Calculate month-over-month growth"
```

---

## Getting Help

- **README:** Quick start and setup
- **TECHNICAL.md:** How DuckDB works, SQL safety
- **TROUBLESHOOTING.md:** Common issues and solutions
- **GitHub Issues:** Report bugs or request features

---

**Pro Tip:** The more specific your questions, the better the answers. Data Lens excels at turning natural language into precise SQL queries!
