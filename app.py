import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="CodeAlpha Task 2 EDA", page_icon="📊", layout="wide")
st.title("📊 CodeAlpha Task 2 — Exploratory Data Analysis")
st.write("Explore structure, quality, trends, patterns and relationships in your dataset.")

uploaded=st.file_uploader("Upload a CSV dataset",type=["csv"])
if uploaded: df=pd.read_csv(uploaded)
else:
    df=pd.read_csv("data/sales_data.csv")
    st.info("Using the included sample sales dataset. Upload your own CSV to analyze it.")

c1,c2,c3,c4=st.columns(4)
c1.metric("Rows",df.shape[0]); c2.metric("Columns",df.shape[1])
c3.metric("Missing Values",int(df.isna().sum().sum())); c4.metric("Duplicates",int(df.duplicated().sum()))

st.subheader("🔍 Data Preview")
st.dataframe(df.head(20),use_container_width=True)
st.subheader("🧹 Data Quality")
st.dataframe(df.isna().sum().to_frame("Missing Values"),use_container_width=True)
st.subheader("📈 Descriptive Statistics")
num=df.select_dtypes(include="number")
if not num.empty: st.dataframe(num.describe().T,use_container_width=True)

st.subheader("📊 Visualization")
cols=list(num.columns)
cats=list(df.select_dtypes(include=["object","category"]).columns)
if cols:
    metric=st.selectbox("Numeric variable",cols)
    st.bar_chart(df[metric].dropna().head(50))
if cats and cols:
    cat=st.selectbox("Group by",cats)
    metric=st.selectbox("Measure",cols,key="measure")
    st.bar_chart(df.groupby(cat)[metric].mean().sort_values(ascending=False).head(20))

st.subheader("🔗 Correlation")
if len(cols)>=2: st.dataframe(num.corr(),use_container_width=True)
else: st.info("At least two numeric columns are required.")

st.download_button("⬇️ Download cleaned CSV",df.drop_duplicates().to_csv(index=False).encode(), "cleaned_dataset.csv","text/csv")
