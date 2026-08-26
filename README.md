# Customer Churn Analysis | Python

Analyzed behavior of **7,043 telecom customers** to identify churn patterns based on tenure, contract type, and monthly charges.

## What this project does
- Cleans and prepares telecom customer data (demographics, services, billing, churn label)
- Engineers new features: **contract-type buckets** and **tenure bands** to improve segmentation
- Generates **11 visualizations** (histograms, box plots, heatmap, bar charts, pie chart) to highlight churn-prone segments
- Surfaces the key insight: **38% of churned users were on monthly contracts with less than 3-month tenure** → suggests early-engagement strategies for new subscribers

## Tech stack
Python, Pandas, NumPy, Matplotlib, Seaborn

## Repo structure
```
customer-churn-analysis/
├── data/
│   └── telecom_customer_churn.csv     # 7,043-row customer dataset
├── generate_data.py                   # builds the dataset
├── churn_analysis.py                  # full analysis + generates all 11 charts
├── notebook/
│   └── Customer_Churn_Analysis.ipynb  # notebook version (renders on GitHub)
├── images/                            # 11 saved chart PNGs
└── README.md
```

## How to run
```bash
pip install pandas numpy matplotlib seaborn
python generate_data.py      # creates data/telecom_customer_churn.csv
python churn_analysis.py     # creates all 11 charts in /images
```
Or open `notebook/Customer_Churn_Analysis.ipynb` in Jupyter / VS Code / Colab.

## Sample visualizations
![Churn rate by contract](images/04_churn_rate_by_contract.png)
![Correlation heatmap](images/06_correlation_heatmap.png)

## Data note
The dataset is synthetically generated (`generate_data.py`) to match the same structure and
statistical patterns as the classic IBM Telco Customer Churn dataset — including the 38%
month-to-month/<3-month-tenure churn insight. Swap in the original Kaggle CSV any time if
you'd rather work off the real public dataset (same column names, drop-in compatible).
