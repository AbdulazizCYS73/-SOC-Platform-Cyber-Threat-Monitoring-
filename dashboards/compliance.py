import streamlit as st

def show_compliance():

    st.subheader("NIST Security Controls")

    c1, c2 = st.columns(2)

    with c1:
        st.checkbox("Identify Assets")
        st.checkbox("Protect Systems")
        st.checkbox("Detect Threats")

    with c2:
        st.checkbox("Respond to Incidents")
        st.checkbox("Recover Operations")