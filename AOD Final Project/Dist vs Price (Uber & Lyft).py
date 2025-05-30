import pandas as pd
import plotly.express as px

input_file = "/Users/siddhantjain/PycharmProjects/AOD Final Project/cab_rides.csv"
df = pd.read_csv(input_file)

df = df.dropna(subset=['distance', 'price', 'cab_type'])

fig = px.scatter(
    df,
    x="distance",
    y="price",
    color="cab_type",
    title="Distance vs Price for Different Cab Types",
    labels={"distance": "Distance (miles)", "price": "Price (USD)"},
    hover_data=["cab_type"]
)

fig.update_layout(
    updatemenus=[
        {
            "buttons": [
                {
                    "label": cab,
                    "method": "update",
                    "args": [
                        {"visible": [cab == c for c in df["cab_type"].unique()]},
                        {"title": f"Distance vs Price for {cab}"}
                    ],
                }
                for cab in df["cab_type"].unique()
            ] + [
                {
                    "label": "All",
                    "method": "update",
                    "args": [
                        {"visible": [True] * len(df["cab_type"].unique())},
                        {"title": "Distance vs Price for All Cab Types"}
                    ],
                }
            ],
            "direction": "down",
            "showactive": True,
        }
    ]
)

fig.show()
