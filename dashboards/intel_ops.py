import streamlit as st

def show_intel(df):

    st.subheader("Intel Operations")

    c1, c2, c3 = st.columns(3)

    c1.metric("Live Events", len(df))

    c2.metric("IPs", df["ip"].nunique())

    c3.metric("Critical", len(df[df["risk"] == "Critical"]))