#This code graphs these statistics versus all Bowlers present in the Bowlers.csv file.


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import numpy as np
import os

# File path
file_path = '/Users/siddhantjain/PycharmProjects/2024 IPL/Files/Bowlers.csv'

# Folder path for saving plots
folder_path = os.path.join(os.path.dirname(file_path), 'Bowler Graphs')

# Create the folder if it doesn't exist
os.makedirs(folder_path, exist_ok=True)

# Load the dataset
data = pd.read_csv(file_path)

# Function to plot graph, perform regression, and save the plot
def plot_graph_and_regression(x_col, y_col, xlabel, ylabel, file_suffix):
    # Extract variables
    X = data[x_col].values.reshape(-1, 1)
    y = data[y_col].values

    # Perform linear regression
    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)

    # Calculate R^2 value
    r2 = r2_score(y, y_pred)

    # Plot the data and regression line
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=x_col, y=y_col, data=data, color='blue', label='Data Points')
    plt.plot(data[x_col], y_pred, color='red', label=f'Best-Fit Line ($R^2={r2:.2f}$)')
    plt.title(f'{ylabel} vs {xlabel}')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)

    # Save the plot in the 'Bowler Graphs' folder
    plot_path = os.path.join(folder_path, f'{file_suffix}.png')
    plt.savefig(plot_path)
    plt.show()

    print(f"Plot saved to: {plot_path}")

# Plot for Winning Bid (cr) vs Wkts
plot_graph_and_regression(y_col='Wkts', x_col='Winning Bid (cr)', ylabel='Wkts', xlabel='Winning Bid (cr)', file_suffix='Bowler: Winning_Bid_vs_Wkts')

# Plot for Winning Bid (cr) vs SR
plot_graph_and_regression(y_col='SR', x_col='Winning Bid (cr)', ylabel='SR', xlabel='Winning Bid (cr)', file_suffix='Bowler: Winning_Bid_vs_SR')

# Plot for Winning Bid (cr) vs Avg
plot_graph_and_regression(y_col='Avg', x_col='Winning Bid (cr)', ylabel='Avg', xlabel='Winning Bid (cr)', file_suffix='Bowler: Winning_Bid_vs_Avg')

# Plot for Winning Bid (cr) vs Econ
plot_graph_and_regression(y_col='Econ', x_col='Winning Bid (cr)', ylabel='Econ', xlabel='Winning Bid (cr)', file_suffix='Bowler: Winning_Bid_vs_Econ')
