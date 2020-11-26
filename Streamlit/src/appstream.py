import app1cov
import app2cov
import app3cov
import app4cov
import streamlit as st
PAGES = {
    "Introduction": app1cov,
    "Confirmed": app2cov,
    "Deaths": app3cov,
    "Recovered": app4cov
}

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()




