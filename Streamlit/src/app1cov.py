import time
import streamlit as st
import pandas as pd
import numpy as np
from streamlit import cache
import pydeck as pdk
import altair as alt
from sqlalchemy import create_engine


def app():
    st.title('Covid-19 Analysis')
    st.markdown("""
    ### Coronavirus disease is an infectious desease that has afected everyone around the globe. It has changed that way we do things in a short amount of time. You will be able to see a short analysis of the data that we've been able to gather for our final project of DATA PRODUCT. We will share information about cases around the world in a determined time period, we hope it serves you. You can see the source and replicate in the following github [here](https://github.com/AlexanderPalencia/Data-Product/blob/master/streamlit/first_app.py)

    ### In order for you to navigate in an easier and more comfortable manner we've implemented a navigation panel for you where you will be able to search for the information that it's most important to you being this information about confirmed cases, deaths due to Coronavirus or Recovered cases as well. You will be able to find this navigation panel on your left of this page, We hope you enjoy and make use of this information.
    """)
