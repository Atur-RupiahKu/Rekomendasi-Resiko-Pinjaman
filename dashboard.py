import streamlit as st
import pandas as pd
import joblib
from sklearn.base import BaseEstimator, TransformerMixin

class MultiplyByFactor(BaseEstimator, TransformerMixin):
    def __init__(self, factor=755.33):
        self.factor = factor

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X * self.factor


pipeline = joblib.load('Credit Risk.pkl')

st.header("Credit Risk")
st.markdown("---")

LoanAmount = st.number_input("Jumlah Hutang (IDR)")
LoanDuration = st.number_input("Lama Hutang (Bulan)")
InterestRate = st.number_input("Bunga Hutang (%)")
MonthlyLoanPayment = st.number_input("Pembayaran Per Bulan (IDR)")
NumberOfDependents = st.number_input("Jumlah Tanggungan")
CreditScore = st.number_input("BI Checking (integrasi dengan SLIK)")
AnnualIncome = st.number_input("Pendapatan per bulan (integrasi dengan fitur 1)")
Age = st.number_input("Usia (tahun)")

EducationLevel = st.selectbox(
    "Pendidikan Terakhir",
    ("SMA/SLTA", "Diploma", "Sarjana", "Magister", "Doktor")
)

EmploymentStatus = st.selectbox(
    "Status Pekerjaan",
    ("Bekerja", "Bekerja Sendiri", "Tidak Bekerja")
)

MaritalStatus = st.selectbox(
    "Status Nikah",
    ("Menikah", "Lajang", "Cerai", "Janda")
)

def changeEducationLevel(EducationLevel):
    if EducationLevel=="SMA/SLTA":
        return "High School"
    elif EducationLevel=="Diploma":
        return "Associate"
    elif EducationLevel=="Sarjana":
        return "Bachelor"
    elif EducationLevel=="Magister":
        return "Master"
    else:
        return "Doctor"

def changeEmploymentStatus(EmploymentStatus):
    if EmploymentStatus=="Bekerja":
        return "Employed"
    elif EmploymentStatus=="Bekerja Sendiri":
        return "Self-Employed"
    else:
        return "Unemployed"

def changeMaritalStatus(MaritalStatus):
    if MaritalStatus=="Menikah":
        return "Married"
    elif MaritalStatus=="Lajang":
        return "Single"
    elif MaritalStatus=="Cerai":
        return "Divorced"
    else:
        return "Widowed"

if st.button('Check Data'):
    new_data = pd.DataFrame({
        "MonthlyIncome": AnnualIncome,
        "LoanAmount": LoanAmount,
        "InterestRate": InterestRate,
        "MonthlyLoanPayment": MonthlyLoanPayment,
        "CreditScore": CreditScore,
        "NumberOfDependents": NumberOfDependents,
        "LoanDuration": LoanDuration,
        'EducationLevel': changeEducationLevel(EducationLevel),
        "Age": Age,
        'EmploymentStatus': changeEmploymentStatus(EmploymentStatus),
        'MaritalStatus': changeMaritalStatus(MaritalStatus)
    }, index=[0])

    st.dataframe(new_data)

if st.button('Run Prediction'):
    new_data = pd.DataFrame({
        "MonthlyIncome": AnnualIncome,
        "LoanAmount": LoanAmount,
        "InterestRate": InterestRate,
        "MonthlyLoanPayment": MonthlyLoanPayment,
        "CreditScore": CreditScore,
        "NumberOfDependents": NumberOfDependents,
        "LoanDuration": LoanDuration,
        'EducationLevel': changeEducationLevel(EducationLevel),
        "Age": Age,
        'EmploymentStatus': changeEmploymentStatus(EmploymentStatus),
        'MaritalStatus': changeMaritalStatus(MaritalStatus)
    }, index=[0])
    prediction = pipeline.predict(new_data)
    proba = pipeline.predict_proba(new_data)
    print(proba)
    print(prediction)
    if prediction==[0]:
        st.header("Loan Not Approved!")
    elif prediction==[1]:
        st.header("Loan Approved")