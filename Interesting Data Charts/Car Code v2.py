import pandas as pd
import altair as alt
import json

df = pd.read_csv("/Users/siddhantjain/PycharmProjects/Interesting Data Charts/Sedans and Hatchbacks.csv")

top_cars = df.nlargest(5, "Potential Lifespan").reset_index(drop=True)

min_radius = 50
max_radius = 250
top_cars["Radius"] = min_radius + (top_cars["Potential Lifespan"] - top_cars["Potential Lifespan"].min()) / \
                     (top_cars["Potential Lifespan"].max() - top_cars["Potential Lifespan"].min()) * (max_radius - min_radius)

def create_arc(car, index, start_theta, end_theta, color):
    base = pd.DataFrame({"theta": [start_theta, end_theta]})
    return alt.Chart(base).mark_arc(innerRadius=top_cars.iloc[index]["Radius"] - 10,
                                    outerRadius=top_cars.iloc[index]["Radius"]
                                   ).encode(
        theta="theta:Q",
        color=alt.value(color)
    )

def create_label(car, index):
    return alt.Chart(pd.DataFrame({"x": [top_cars.iloc[index]["Radius"] + 20],
                                    "y": [0],
                                    "text": [f"{car['Car']}\n{car['Potential Lifespan']} miles"]})).mark_text(
        align='left', baseline='middle', dx=5
    ).encode(x='x:Q', y='y:Q', text='text:N')

donut_charts = []
for i, row in top_cars.iterrows():
    donut_charts.append(create_arc(row, i, 0, 90, "white"))
    donut_charts.append(create_arc(row, i, 90, 270, "green"))
    donut_charts.append(create_arc(row, i, 270, 360, "black"))
    donut_charts.append(create_label(row, i))  # Add label

chart = alt.layer(*donut_charts).properties(width=400, height=400)
chart_json = chart.to_json()


with open("donut_chart.json", "w") as f:
    json.dump(chart_json, f)
