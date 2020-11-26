import pandas as pd
import numpy as np

confirmed = pd.read_csv("../data/time_series_covid19_confirmed_global.csv")
confirmed['Lat'] = confirmed.Lat.astype(str)
confirmed['Long'] = confirmed.Long.astype(str)
confirmed.insert(0, 'New_ID', range(0, len(confirmed)))

length_colm = len(confirmed.columns)
for i in range(5, length_colm):
    if i == length_colm-1:
        new_colname = 'diff' + confirmed.columns[i]
        confirmed[new_colname] = 0
    elif i == 5:
        new_colname = 'diff' + confirmed.columns[i]
        confirmed[new_colname] = 0
    else:
            new_colname = ''
            new_colname = 'diff' + confirmed.columns[i]
            confirmed[new_colname] = confirmed[confirmed.columns[i+1]] - confirmed[confirmed.columns[i]]

            
first_df = confirmed.iloc[:, 0: length_colm]
cols = list(range(5,length_colm))
df = confirmed
df.drop(df.columns[cols],axis=1,inplace=True)
second_df = df

variables = [
    "Province/State",
    "Country/Region",
    "Lat",
    "Long"
]

new_confirmed = pd.melt(frame=first_df, id_vars= variables, var_name="fecha",value_name="confirmed")
new_confirmed["confirmed"] = new_confirmed["confirmed"].astype(int)
new_confirmed = new_confirmed.rename(columns={'Lat':'lat','Long':'lon'})

new_diff = pd.melt(frame=df, id_vars= variables, var_name="fecha",value_name="Aumento")
new_diff["Aumento"] = new_diff["Aumento"].astype(int)
new_diff = new_diff.rename(columns={'Lat':'lat','Long':'lon'})

df_final = new_confirmed
df_final['diff'] = new_diff['Aumento']