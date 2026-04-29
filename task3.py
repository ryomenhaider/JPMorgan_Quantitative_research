import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

df = pd.read_csv('/mnt/D06A89C26A89A5B6/projects/Forage/JPMorgan_Quantitative_research/data/Loan_Data.csv')

X = df.drop(columns=['default'])
y = df['default']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

lr_model = Pipeline(
    [
        ('scaler', StandardScaler()),
        ('model' , LogisticRegression())
    ]
)
lr_model.fit(X_train, y_train)

rf_model = Pipeline(
    [
        ('scaler', StandardScaler()),
        ('model' , RandomForestClassifier())
    ]
)
rf_model.fit(X_train, y_train)

for name, model in [('Logistic Regression', lr_model), ('RandomForestClassifier', rf_model)]:
    probs = model.predict_proba(X_test)[:,1]
    print(f'{name} AUC: {roc_auc_score(y_test, probs):.4f}')

def expected_loss(
        borrower_detail,
        model,
        loan_amount,
        recovery_rate=0.10
):
    borrower_df = pd.DataFrame([borrower_detail])
    PD = model.predict_proba(borrower_df)[:,1][0]
    LGD = 1 - recovery_rate
    EL  = PD * LGD * loan_amount
    print(f"Probability of Default : {PD:.2%}")
    print(f"Expected Loss          : ${EL:,.2f}")
    return round(EL, 2)

borrower = {
    "credit_lines_outstanding": 3,
    "loan_amt_outstanding": 5000,
    "total_debt_outstanding": 15000,
    "income": 60000,
    "years_employed": 5,
    "fico_score": 650
}

expected_loss(borrower_detail=borrower, loan_amount=10000, model=rf_model)
