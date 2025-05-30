import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime

df = pd.read_csv("cab_rides_with_time.csv")

df = df.dropna(subset=['price', 'surge_multiplier'])

df['hour'] = df['time'].apply(lambda x: int(x.split(':')[0]))
df['minute'] = df['time'].apply(lambda x: int(x.split(':')[1]))


X_price = df[['cab_type', 'name', 'distance', 'hour', 'minute', 'surge_multiplier']]
y_price = df['price']

categorical_features = ['cab_type', 'name']
numerical_features = ['distance', 'hour', 'minute', 'surge_multiplier']

preprocessor_price = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(drop='first'), categorical_features)
    ],
    remainder='passthrough'
)

price_model = Pipeline(steps=[
    ('preprocessor', preprocessor_price),
    ('regressor', RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42))
])

X_price_train, X_price_test, y_price_train, y_price_test = train_test_split(X_price, y_price, test_size=0.2, random_state=42)
price_model.fit(X_price_train, y_price_train)


def predict_price(cab_type, cab_name, distance, surge_multiplier, time_str):
    try:
        dt = datetime.strptime(time_str, "%H:%M:%S:%f")
    except ValueError:
        raise ValueError("Time must be in HH:MM:SS:MS format (e.g., 14:30:12:123)")

    hour = dt.hour
    minute = dt.minute

    price_input = pd.DataFrame([{
        'cab_type': cab_type,
        'name': cab_name,
        'distance': distance,
        'hour': hour,
        'minute': minute,
        'surge_multiplier': surge_multiplier
    }])
    predicted_price = price_model.predict(price_input)[0]

    return round(predicted_price, 2)
Ub
if __name__ == "__main__":
    cab_type = input("Enter cab company (Uber or Lyft): ")
    cab_name = input("Enter ride type (e.g., Shared, Black, Lux, etc.): ")
    distance = float(input("Enter distance in miles: "))
    surge_multiplier = float(input("Enter surge multiplier (e.g., 1.0, 1.25, 2.0): "))
    time_str = input("Enter time in format HH:MM:SS:MS (e.g., 14:25:35:120): ")

    price = predict_price(cab_type, cab_name, distance, surge_multiplier, time_str)
    print(f"Predicted Price: ${price}")
