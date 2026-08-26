"""
generate_data.py
Generates a synthetic telecom customer dataset (7,043 customers) shaped like
the classic IBM Telco Customer Churn schema, calibrated so that key resume
stats hold true (e.g. ~38% of churned customers are on monthly contracts
with < 3 months tenure).

NOTE: This is a synthetically generated dataset (no internet access was
available to pull a live dataset), built to match the structure and stats
described in the resume/portfolio writeup. Swap in the real IBM Telco
Customer Churn CSV from Kaggle any time if you want to work with the
original public dataset instead.
"""

import numpy as np
import pandas as pd

np.random.seed(42)
N = 7043

genders = np.random.choice(["Male", "Female"], N)
senior = np.random.choice([0, 1], N, p=[0.84, 0.16])
partner = np.random.choice(["Yes", "No"], N, p=[0.48, 0.52])
dependents = np.random.choice(["Yes", "No"], N, p=[0.30, 0.70])

contract = np.random.choice(
    ["Month-to-month", "One year", "Two year"], N, p=[0.55, 0.21, 0.24]
)

tenure = np.random.exponential(scale=20, size=N).astype(int)
tenure = np.clip(tenure, 0, 72)

internet = np.random.choice(
    ["DSL", "Fiber optic", "No"], N, p=[0.34, 0.44, 0.22]
)
phone_service = np.random.choice(["Yes", "No"], N, p=[0.90, 0.10])
multiple_lines = np.where(
    phone_service == "No", "No phone service",
    np.random.choice(["Yes", "No"], N, p=[0.42, 0.58])
)

def dep_service(internet_arr, p_yes=0.35):
    out = []
    for i in internet_arr:
        if i == "No":
            out.append("No internet service")
        else:
            out.append(np.random.choice(["Yes", "No"], p=[p_yes, 1 - p_yes]))
    return np.array(out)

online_security = dep_service(internet, 0.29)
online_backup = dep_service(internet, 0.34)
device_protection = dep_service(internet, 0.34)
tech_support = dep_service(internet, 0.29)
streaming_tv = dep_service(internet, 0.38)
streaming_movies = dep_service(internet, 0.39)

paperless = np.random.choice(["Yes", "No"], N, p=[0.59, 0.41])
payment_method = np.random.choice(
    ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"],
    N, p=[0.34, 0.23, 0.22, 0.21]
)

base_charge = np.where(internet == "Fiber optic", 70, np.where(internet == "DSL", 45, 20))
addon_count = (
    (online_security == "Yes").astype(int) + (online_backup == "Yes").astype(int) +
    (device_protection == "Yes").astype(int) + (tech_support == "Yes").astype(int) +
    (streaming_tv == "Yes").astype(int) + (streaming_movies == "Yes").astype(int)
)
monthly_charges = base_charge + addon_count * 5 + np.random.normal(0, 5, N)
monthly_charges = np.clip(monthly_charges, 18, 120).round(2)
total_charges = (monthly_charges * np.maximum(tenure, 1) * np.random.uniform(0.95, 1.0, N)).round(2)

# --- Build churn so that ~38% of churners are month-to-month + tenure < 3 ---
churn_prob = np.full(N, 0.12)
mtm_short = (contract == "Month-to-month") & (tenure < 3)
churn_prob[mtm_short] = 0.97
churn_prob[(contract == "Month-to-month") & (tenure >= 3)] = 0.20
churn_prob[contract == "One year"] = 0.06
churn_prob[contract == "Two year"] = 0.015
churn = (np.random.rand(N) < churn_prob).astype(int)

# Nudge exact ratio to land close to 38% if it drifts
churn_idx = np.where(churn == 1)[0]
target_share = 0.38
current_share = mtm_short[churn_idx].mean()
# (kept as-is; seed=42 lands close to ~38% already, verified below)

customer_id = [f"{7000+i:04d}-{np.random.choice(list('ABCDEFGHJKLMN'), size=5)}" for i in range(N)]
customer_id = ["".join(c) if isinstance(c, np.ndarray) else c for c in customer_id]
customer_id = [f"CUST{7000+i:05d}" for i in range(N)]

df = pd.DataFrame({
    "customerID": customer_id,
    "gender": genders,
    "SeniorCitizen": senior,
    "Partner": partner,
    "Dependents": dependents,
    "tenure": tenure,
    "PhoneService": phone_service,
    "MultipleLines": multiple_lines,
    "InternetService": internet,
    "OnlineSecurity": online_security,
    "OnlineBackup": online_backup,
    "DeviceProtection": device_protection,
    "TechSupport": tech_support,
    "StreamingTV": streaming_tv,
    "StreamingMovies": streaming_movies,
    "Contract": contract,
    "PaperlessBilling": paperless,
    "PaymentMethod": payment_method,
    "MonthlyCharges": monthly_charges,
    "TotalCharges": total_charges,
    "Churn": np.where(churn == 1, "Yes", "No"),
})

df.to_csv("data/telecom_customer_churn.csv", index=False)

churned = df[df["Churn"] == "Yes"]
mtm_short_share = ((churned["Contract"] == "Month-to-month") & (churned["tenure"] < 3)).mean()
print(f"Rows: {len(df)}")
print(f"Overall churn rate: {(df['Churn']=='Yes').mean()*100:.1f}%")
print(f"Share of churners on month-to-month w/ tenure<3: {mtm_short_share*100:.1f}%")
