# smart-store-moses

## 🧠 1. Business Goal  
**Goal:** Identify total sales performance by *season* and *product category* across different *regions*.  
This insight helps Smart Store optimize inventory and marketing strategies based on seasonal demand and regional trends.

---

## 🗂 2. Data Source  
We used the prepared **SQLite data warehouse** located at: data/dw/smart_sales.db


### Tables Used:
- **sales** – `sale_id`, `customer_id`, `product_id`, `sale_amount`, `sale_date`
- **product** – `product_id`, `product_name`, `category`
- **customer** – `customer_id`, `name`, `region`, `join_date`

### Columns Used:
- From `sales`: `sale_date`, `sale_amount`
- From `product`: `category`
- From `customer`: `region`

---

## 🧰 3. Tools  
- **PySpark**: For OLAP-style joins, grouping, and aggregation  
- **Matplotlib + Seaborn**: For final visualizations  
- **Jupyter Notebook**: For documenting and presenting the full pipeline

---

## 🧮 4. Workflow & Logic  

### A. Join & Prep  
We joined the three tables on `product_id` and `customer_id`, and extracted the month from `sale_date`. Then, we assigned each month to a `season`.

```python
from pyspark.sql.functions import month, when

df_joined = df_sales \
    .join(df_product, "product_id") \
    .join(df_customer, "customer_id") \
    .withColumn("month", month("sale_date"))

df_joined = df_joined.withColumn(
    "season",
    when(df_joined.month.isin(12, 1, 2), "Winter")
    .when(df_joined.month.isin(3, 4, 5), "Spring")
    .when(df_joined.month.isin(6, 7, 8), "Summer")
    .when(df_joined.month.isin(9, 10, 11), "Fall")
)
```

### B. OLAP Aggregation
We grouped by region, season, and category and calculated the total sales:

from pyspark.sql.functions import sum as _sum

olap_result = df_joined.groupBy("region", "season", "category") \
    .agg(_sum("sale_amount").alias("total_sales"))

---

## 📈 5. Results & Visualization
Bar Chart:
Title: Total Sales by Season and Product Category
Axes:

X-axis: Season

Y-axis: Total Sales ($)

Color: Product Category

[Total Sales Chart](Screenshot 2025-04-21 at 1.28.14 AM.png)

### 7. Challenges
- Handling missing values in the `sale_date` column.
- Initial Spark JDBC connection failed until .jar path and org.sqlite.JDBC driver were configured.
- season was initially null due to format mismatch – fixed by casting date before extracting month.

