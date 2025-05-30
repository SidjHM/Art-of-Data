import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import numpy as np

input_file = "/Users/siddhantjain/PycharmProjects/AOD Final Project/cab_rides.csv"
df = pd.read_csv(input_file)

df = df.dropna(subset=["distance", "price", "name"])

r2_values = {}

cab_types = df["name"].unique()

for cab in cab_types:
    subset = df[df["name"] == cab]

    X = subset[["distance"]].values
    y = subset["price"].values

    if len(X) > 1:
        model = LinearRegression()
        model.fit(X, y)
        y_pred = model.predict(X)
        r2 = r2_score(y, y_pred)
        r2_values[cab] = r2

print("R² values for each Cab Type:")
for cab, r2 in r2_values.items():
    print(f"{cab}: {r2:.4f}")

fig = px.scatter(
    df,
    x="distance",
    y="price",
    color="name",
    title="Distance vs Price by Cab Type",
    labels={"distance": "Distance (miles)", "price": "Price (USD)", "name": "Cab Type"},
    hover_data=["cab_type", "name"]
)

fig.update_layout(
    legend_title_text="Cab Type",
    hovermode="closest"
)

fig.show()
