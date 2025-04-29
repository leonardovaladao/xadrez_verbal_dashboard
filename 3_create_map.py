import pandas as pd
import plotly.express as px
import plotly.colors as pc
import numpy as np

from map_country_pt_en import countries_map_pt_en

df_citacoes = pd.read_csv('Data/Numero_Citacoes.csv')
df_programas = pd.read_csv('Data/Numero_Programas.csv')
df = df_citacoes.merge(df_programas, on='Pais', how='outer')
df['Country'] = df['Pais'].map(countries_map_pt_en)
df = df.rename(columns={'NumCit': 'Citações', 'NumProgramas': 'Programas'})
df["Citações_Log"] = np.log1p(df["Citações"])  

_, list_values = pd.qcut(df['Citações'], 10, duplicates='drop', retbins=True)
list_values = [round(i) for i in list_values]
# list_values = np.arange(1, max(df['Citações'])+1, round(max(df['Citações'])/10))

tick_vals = np.log1p(list_values)
tick_text = [str(v) for v in list_values]

greys = pc.sequential.Greys
custom_greys = greys[1:-1]  

fig = px.choropleth(
    df,
    locations = 'Country',
    locationmode="country names",
    color='Citações_Log',
    hover_data=["Citações", "Programas"],
    color_continuous_scale=custom_greys,
    # range_color=(2, 1_000)
)

fig.update_traces(
    hovertemplate=(
        "<b>País: %{customdata[0]}</b><br>" +
        "Número de citações: %{customdata[1]}<br>" +
        "Número de programas: %{customdata[2]}<br>" 
    ),
    customdata=df.values
)



fig.update_coloraxes(
    colorbar=dict(
        
        tickvals=tick_vals,
        ticktext=tick_text
    )
)

fig.update_layout(
    coloraxis_colorbar=dict(
        title="Citações",
        thickness=15,       # Make colorbar thinner
        len=0.75,           # Shorten it a bit
        xpad=10             # Add space from right edge
    ),
    margin=dict(l=0, r=0, t=0, b=0)  # Remove extra margin
)

fig.write_html('my_map.html', include_plotlyjs="cdn", full_html=True)