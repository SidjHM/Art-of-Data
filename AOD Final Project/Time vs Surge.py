import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import r2_score
import datetime

df = pd.read_csv("cab_rides.csv")
df = df.dropna(subset=['price', 'surge_multiplier'])
df['timestamp'] = pd.to_datetime(df['time_stamp'], unit='ms')
df['seconds_since_midnight'] = df['timestamp'].dt.hour * 3600 + df['timestamp'].dt.minute * 60 + df['timestamp'].dt.second

cab_names = df['name'].unique()
r2_values = {}
for name in cab_names:
    sub_df = df[df['name'] == name]
    if len(sub_df) > 1:
        x = sub_df['seconds_since_midnight']
        y = sub_df['surge_multiplier']
        r2_values[name] = round(r2_score(y, x), 3)

fig = px.scatter(
    df,
    x='seconds_since_midnight',
    y='surge_multiplier',
    color='name',
    title='Surge Multiplier vs Time of Day by Cab Name',
    labels={'seconds_since_midnight': 'Time of Day (HH:MM)', 'surge_multiplier': 'Surge Multiplier'},
    hover_data=['cab_type', 'distance']
)

tick_vals = list(range(0, 86401, 3600))
tick_texts = [str(datetime.timedelta(seconds=s))[:-3] for s in tick_vals]
fig.update_xaxes(tickmode='array', tickvals=tick_vals, ticktext=tick_texts)

buttons = [
    dict(label="All",
         method="update",
         args=[{"visible": [True]*len(fig.data)},
               {"title": "Surge Multiplier vs Time of Day for All Cab Names"}])
]

for i, name in enumerate(cab_names):
    mask = [trace.name == name for trace in fig.data]
    buttons.append(
        dict(label=name,
             method="update",
             args=[{"visible": mask},
                   {"title": f"Surge Multiplier vs Time of Day for {name} (R² = {r2_values.get(name, 'N/A')})"}])
    )

fig.update_layout(
    updatemenus=[
        dict(
            active=0,
            buttons=buttons
        )
    ]
)

fig.update_traces(marker=dict(size=5))
fig.update_layout(height=600)
fig.show()

print("\nR² values for each cab name (surge_multiplier vs time of day):")
for name, r2 in r2_values.items():
    print(f"{name}: R² = {r2}")
