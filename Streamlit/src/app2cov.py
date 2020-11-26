import time
import streamlit as st
import pandas as pd
import numpy as np
from streamlit import cache
import pydeck as pdk
import altair as alt
from sqlalchemy import create_engine
from datetime import datetime


## Confirmed Covid Data

def app():
        
    engine = create_engine("mysql+pymysql://alex:test123@db:3306/airflowcovid")

    confirm = pd.read_sql_table('confirmed', engine) 
    dfconfirm = confirm.copy()
    dfconfirm['Date'] =  pd.to_datetime(dfconfirm['Date'])
    max_date = max(dfconfirm['Date'])
    min_date = min(dfconfirm['Date'])
    description = "The following page will provide you with information about the confirmed cases around the world. This data has been gathered and display from " + str(min_date) + " to  " + str(max_date) + " to give you a better knowledge of the information you're presented with."

    group_by_country_and_date = dfconfirm.groupby(['Country', 'Date'])['Cases'].sum().reset_index()
    group_by_super = dfconfirm.groupby(['Country', 'Date', 'Lat', 'Lon'])['Cases'].sum().reset_index()
    group_by_super["Lon"] = pd.to_numeric(group_by_super["Lon"], downcast="float")
    group_by_super["Lat"] = pd.to_numeric(group_by_super["Lat"], downcast="float")

    total_cases = dfconfirm[dfconfirm['Date'] == max_date]
    total_cases.rename(columns = {'Cases': 'Total_Cases'}, inplace = True)
    group_by_country_total = total_cases.groupby(['Country'])['Total_Cases'].sum()
    

    # FRONT-END
    st.title('Confirmed cases')
    
    st.write(description)
    
    st.subheader('Raw Data')
    st.write(dfconfirm)  
    
    st.subheader('Total Cases by ' + str(max_date))
    st.dataframe(group_by_country_total)
    
    st.subheader('Top 10 countries with more cases by date')
    hour_selected = st.date_input(label="Select a Date", value=dfconfirm['Date'].min(),  min_value=dfconfirm['Date'].min(),  max_value=dfconfirm['Date'].max())
    df_filter_date = dfconfirm[dfconfirm['Date'] == hour_selected.isoformat()]
    df_filter_date.rename(columns = {'Cases': 'Total_Cases'}, inplace = True)
    group_by_country_date = df_filter_date.groupby(['Country'])['Total_Cases'].sum().reset_index()
    group_by_country_date.sort_values(by=['Total_Cases'], ascending=False, inplace = True)
    a = group_by_country_date.head(10)
    
    s = alt.Chart(a).mark_bar().encode(
        alt.X('Country'),
        alt.Y('Total_Cases')
    )

    st.altair_chart(s, use_container_width=True)
    
    st.subheader('Historical data by country')
    countries_sel = st.multiselect(
     'Select a Contry',
     dfconfirm['Country'].unique())

    if len(countries_sel) > 0:
        filter_his_by_country = group_by_country_and_date[group_by_country_and_date.Country.isin(countries_sel)]
        q = alt.Chart(filter_his_by_country).mark_line().encode(
            x='Date',
            y='Cases',
            color='Country',
            strokeDash='Country',
        )
        st.altair_chart(q, use_container_width=True)

    
    
    st.subheader('Historical Map')

    # 2020-11-04 00:00:00


    a = pd.date_range(start=min_date,end=max_date)
    fin = pd.DataFrame(a, columns=['fecha'])
    fin.insert(0, 'ID', range(0, len(fin)))

    x = st.slider('Drag Date', min_value=0, max_value=len(fin), value=1)
    
    filterd = fin[fin['ID'] == x]['fecha']
    
    st.write(filterd.iloc[0]) 

    
    group_by_super_date = group_by_super[group_by_super['Date'] == filterd.iloc[0]]
    # Set viewport for the deckgl map
    view = pdk.ViewState(latitude=0, longitude=0, zoom=0.2,)

    
    # Create the scatter plot layer
    covidLayer = pdk.Layer(
            "ScatterplotLayer",
            group_by_super_date[['Cases','Lat','Lon']],
            get_position=['Lon', 'Lat'],
            get_radius='Cases',          # Radius is given in meters
            get_fill_color=[252, 136, 3],
            get_line_color=[255,0,0],
            pickable=False,
            opacity=0.3,
            stroked=True,
            filled=True,
            radius_scale=10,
            radius_min_pixels=2,
            radius_max_pixels=25,
            line_width_min_pixels=1
        )

    # Create the deck.gl map
    r = pdk.Deck(
        layers=[covidLayer],
        initial_view_state=view,
        map_style="mapbox://styles/mapbox/light-v10"
    )
    map = st.pydeck_chart(r)




