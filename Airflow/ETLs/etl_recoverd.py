import pandas as pd
import numpy as np

recovered = pd.read_csv("../data/time_series_covid19_recovered_global.csv")
recovered['Lat'] = recovered.Lat.astype(str)
recovered['Long'] = recovered.Long.astype(str)

variables = [
    "Province/State",
    "Country/Region",
    "Lat",
    "Long"
]

new_recovered = pd.melt(frame=recovered, id_vars= variables, var_name="fecha",value_name="recovered")
new_recovered["recovered"] = new_recovered["recovered"].astype(int)
new_recovered = new_recovered.rename(columns={'Lat':'lat','Long':'lon'})