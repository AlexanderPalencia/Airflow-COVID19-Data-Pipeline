import pandas as pd
import numpy as np

deaths = pd.read_csv("../data/time_series_covid19_deaths_global.csv")
deaths['Lat'] = deaths.Lat.astype(str)
deaths['Long'] = deaths.Long.astype(str)

variables = [
    "Province/State",
    "Country/Region",
    "Lat",
    "Long"
]

new_deaths = pd.melt(frame=deaths, id_vars= variables, var_name="fecha",value_name="deaths")
new_deaths["deaths"] = new_deaths["deaths"].astype(int)
new_deaths = new_deaths.rename(columns={'Lat':'lat','Long':'lon'})
print(new_deaths.head())