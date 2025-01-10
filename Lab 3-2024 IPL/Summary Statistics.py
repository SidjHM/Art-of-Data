import pandas as pd
import os
import matplotlib.pyplot as plt

# File paths
batters_file_path = '/Users/siddhantjain/PycharmProjects/2024 IPL/Files/Batters.csv'
bowlers_file_path = '/Users/siddhantjain/PycharmProjects/2024 IPL/Files/Bowlers.csv'

# Load the datasets
batters_data = pd.read_csv(batters_file_path)
bowlers_data = pd.read_csv(bowlers_file_path)


# Function to calculate summary statistics
def calculate_summary_statistics(data, column_name):
    mode = data[column_name].mode()
    stats = {
        'Mean': data[column_name].mean(),
        'Median': data[column_name].median(),
        'Mode': mode.tolist() if not mode.empty else None,  # Handle multiple modes or empty mode
        'STD': data[column_name].std()
    }
    return stats


# Columns to analyze and their datasets
columns_to_analyze = {
    'Runs': batters_data,
    'Avg': batters_data,
    'Wkts': bowlers_data,
    'SR': bowlers_data
}

# Create a summary table
summary_rows = []

# Calculate statistics for each column and add to the summary table
for column, dataset in columns_to_analyze.items():
    stats = calculate_summary_statistics(dataset, column)
    summary_rows.append({'Statistic': 'Mean', column: stats['Mean']})
    summary_rows.append({'Statistic': 'Median', column: stats['Median']})
    summary_rows.append({'Statistic': 'Mode', column: stats['Mode']})
    summary_rows.append({'Statistic': 'STD', column: stats['STD']})

# Convert the list of rows into a DataFrame
summary_table = pd.DataFrame(summary_rows)

# Reorganize columns to ensure proper formatting
summary_table = summary_table.fillna("").set_index("Statistic").T.reset_index().rename(columns={'index': 'Statistic'})

# Display the summary table
print(summary_table)

# Save summary table as a CSV file
summary_csv_path = os.path.join(os.path.dirname(batters_file_path), 'Summary_Statistics.csv')
summary_table.to_csv(summary_csv_path, index=False)
print(f"Summary statistics saved to: {summary_csv_path}")

# Generate box plots for each column
output_directory = os.path.dirname(batters_file_path)  # Save plots in the same directory as the files

for column, dataset in columns_to_analyze.items():
    plt.figure(figsize=(8, 6))
    plt.boxplot(dataset[column].dropna(), patch_artist=True, boxprops=dict(facecolor='lightblue', color='blue'))
    plt.title(f'Box Plot for {column}', fontsize=16)
    plt.ylabel(column, fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Save each box plot as a separate image
    plot_file_path = os.path.join(output_directory, f'BoxPlot_{column}.png')
    plt.savefig(plot_file_path)
    print(f"Box plot saved to: {plot_file_path}")
    plt.close()
