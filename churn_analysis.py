"""
churn_analysis.py
Customer Churn Analysis — Telecom (7,043 customers)

Analyzes churn patterns based on tenure, contract type, and monthly charges.
Engineers contract-type buckets and tenure bands, then produces 11 charts
saved to /images.

Key insight: 38% of churned customers were on month-to-month contracts with
less than 3 months of tenure -> early-engagement / onboarding strategies
recommended for new month-to-month subscribers.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
plt.rcParams["figure.dpi"] = 110

df = pd.read_csv("data/telecom_customer_churn.csv")

# ---------------------------------------------------------------
# Feature engineering
# ---------------------------------------------------------------
def tenure_band(t):
    if t < 3:
        return "0-2 mo"
    elif t < 12:
        return "3-11 mo"
    elif t < 24:
        return "12-23 mo"
    elif t < 48:
        return "24-47 mo"
    else:
        return "48+ mo"

df["TenureBand"] = df["tenure"].apply(tenure_band)
df["TenureBand"] = pd.Categorical(
    df["TenureBand"], categories=["0-2 mo", "3-11 mo", "12-23 mo", "24-47 mo", "48+ mo"], ordered=True
)

df["ContractBucket"] = df["Contract"].map({
    "Month-to-month": "Monthly",
    "One year": "1-Year",
    "Two year": "2-Year",
})

df["ChurnFlag"] = (df["Churn"] == "Yes").astype(int)

out = "images/"

# 1. Overall churn distribution (pie)
plt.figure(figsize=(5, 5))
df["Churn"].value_counts().plot.pie(autopct="%1.1f%%", colors=["#4C72B0", "#DD8452"], ylabel="")
plt.title("1. Overall Customer Churn Distribution")
plt.tight_layout(); plt.savefig(out + "01_overall_churn_pie.png"); plt.close()

# 2. Tenure histogram
plt.figure(figsize=(7, 5))
sns.histplot(data=df, x="tenure", hue="Churn", bins=30, multiple="stack", palette=["#4C72B0", "#DD8452"])
plt.title("2. Tenure Distribution by Churn")
plt.xlabel("Tenure (months)")
plt.tight_layout(); plt.savefig(out + "02_tenure_histogram.png"); plt.close()

# 3. Monthly charges histogram
plt.figure(figsize=(7, 5))
sns.histplot(data=df, x="MonthlyCharges", hue="Churn", bins=30, multiple="stack", palette=["#4C72B0", "#DD8452"])
plt.title("3. Monthly Charges Distribution by Churn")
plt.xlabel("Monthly Charges ($)")
plt.tight_layout(); plt.savefig(out + "03_monthly_charges_histogram.png"); plt.close()

# 4. Churn rate by contract type (bar)
plt.figure(figsize=(6, 5))
rate = df.groupby("ContractBucket")["ChurnFlag"].mean().reindex(["Monthly", "1-Year", "2-Year"]) * 100
rate.plot.bar(color="#C44E52")
plt.ylabel("Churn Rate (%)"); plt.title("4. Churn Rate by Contract Type")
plt.xticks(rotation=0)
plt.tight_layout(); plt.savefig(out + "04_churn_rate_by_contract.png"); plt.close()

# 5. Box plot: monthly charges by churn
plt.figure(figsize=(6, 5))
sns.boxplot(data=df, x="Churn", y="MonthlyCharges", palette=["#4C72B0", "#DD8452"])
plt.title("5. Monthly Charges by Churn Status")
plt.tight_layout(); plt.savefig(out + "05_boxplot_charges_by_churn.png"); plt.close()

# 6. Correlation heatmap
plt.figure(figsize=(6, 5))
num_df = df[["tenure", "MonthlyCharges", "TotalCharges", "SeniorCitizen", "ChurnFlag"]]
sns.heatmap(num_df.corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("6. Correlation Heatmap")
plt.tight_layout(); plt.savefig(out + "06_correlation_heatmap.png"); plt.close()

# 7. Churn rate by tenure band
plt.figure(figsize=(7, 5))
rate2 = df.groupby("TenureBand")["ChurnFlag"].mean() * 100
rate2.plot.bar(color="#55A868")
plt.ylabel("Churn Rate (%)"); plt.title("7. Churn Rate by Tenure Band")
plt.xticks(rotation=20)
plt.tight_layout(); plt.savefig(out + "07_churn_rate_by_tenure_band.png"); plt.close()

# 8. Churn count by contract bucket AND tenure band (highlighting the 38% insight)
plt.figure(figsize=(8, 5))
sub = df[df["Churn"] == "Yes"]
ct = pd.crosstab(sub["TenureBand"], sub["ContractBucket"])
ct.plot.bar(stacked=True, ax=plt.gca(), colormap="Set2")
plt.title("8. Churned Customers: Tenure Band x Contract Type")
plt.ylabel("Number of Churned Customers")
plt.xticks(rotation=20)
plt.tight_layout(); plt.savefig(out + "08_churn_tenureband_contract_stacked.png"); plt.close()

# 9. Churn rate by payment method
plt.figure(figsize=(7, 5))
rate3 = df.groupby("PaymentMethod")["ChurnFlag"].mean().sort_values() * 100
rate3.plot.barh(color="#8172B2")
plt.xlabel("Churn Rate (%)"); plt.title("9. Churn Rate by Payment Method")
plt.tight_layout(); plt.savefig(out + "09_churn_rate_by_payment_method.png"); plt.close()

# 10. Churn rate by internet service
plt.figure(figsize=(6, 5))
rate4 = df.groupby("InternetService")["ChurnFlag"].mean() * 100
rate4.plot.bar(color="#CCB974")
plt.ylabel("Churn Rate (%)"); plt.title("10. Churn Rate by Internet Service")
plt.xticks(rotation=0)
plt.tight_layout(); plt.savefig(out + "10_churn_rate_by_internet_service.png"); plt.close()

# 11. Senior citizen churn comparison
plt.figure(figsize=(6, 5))
rate5 = df.groupby("SeniorCitizen")["ChurnFlag"].mean() * 100
rate5.index = ["Non-Senior", "Senior"]
rate5.plot.bar(color="#64B5CD")
plt.ylabel("Churn Rate (%)"); plt.title("11. Churn Rate: Senior vs Non-Senior Citizens")
plt.xticks(rotation=0)
plt.tight_layout(); plt.savefig(out + "11_churn_rate_senior_citizen.png"); plt.close()

# ---------------------------------------------------------------
# Key insight printout
# ---------------------------------------------------------------
churned = df[df["Churn"] == "Yes"]
insight_share = ((churned["Contract"] == "Month-to-month") & (churned["tenure"] < 3)).mean()
print(f"Total customers analyzed: {len(df)}")
print(f"Overall churn rate: {df['ChurnFlag'].mean()*100:.1f}%")
print(f"Share of churned users on monthly contracts with <3mo tenure: {insight_share*100:.1f}%")
print("11 visualizations saved to /images")
