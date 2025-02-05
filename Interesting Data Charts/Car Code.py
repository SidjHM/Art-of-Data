import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib.patches import Polygon, Circle
import matplotlib.colors as mcolors
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon as ShapelyPolygon

# Load the population data
df = pd.read_csv('/Users/siddhantjain/PycharmProjects/Interesting Data Charts/Population.csv')

# Clean the population column
df['Population (2024)'] = df['Population (2024)'].replace({',': ''}, regex=True).astype(int)

# Normalize population for proportional sizing
df['Normalized Population'] = df['Population (2024)'] / df['Population (2024)'].sum()

# Set up the figure and axis for plotting (making the circle bigger)
fig, ax = plt.subplots(figsize=(10, 10))  # Increased size of the figure
ax.set_aspect('equal')

# Define the number of countries to be plotted
num_countries = len(df)

# Set the radius of the circle
radius = 50.0

# Remove the background color
fig.patch.set_facecolor('none')  # Remove the background of the figure
ax.set_facecolor('none')  # Remove the background of the axes

# Create a list of distinct colors
colors = list(mcolors.TABLEAU_COLORS.values()) * 5  # Ensure we have enough colors

# Function to generate random shapes (polygons) inside the circle
def generate_random_shape(population_fraction, radius, min_size=0.05, max_size=0.2):
    # Determine the size of the polygon based on the population fraction
    size = population_fraction * (max_size - min_size) + min_size

    num_sides = random.randint(4, 10)  # Random number of sides for the polygon
    angle_step = 2 * np.pi / num_sides
    points = []

    # Generate random points for the polygon
    for i in range(num_sides):
        angle = i * angle_step
        r = random.uniform(0, size * radius)  # Random radius scaled by population fraction
        x = r * np.cos(angle)
        y = r * np.sin(angle)
        points.append((x, y))

    # Create the polygon
    polygon = ShapelyPolygon(points)

    # Make sure the polygon fits within the circle boundary
    if polygon.is_valid and polygon.area <= np.pi * (radius ** 2):
        return points
    else:
        # If invalid or out of bounds, retry
        return generate_random_shape(population_fraction, radius, min_size, max_size)

# List to hold the positions of the polygons (shapes)
occupied_positions = []

# Add the outer circle to the plot (making the circle boundary visible)
circle = Circle((0, 0), radius, edgecolor='black', facecolor='none', linewidth=2)
ax.add_patch(circle)

# Function to check if a new shape overlaps with any existing shapes
def check_overlap(new_shape, occupied_positions):
    new_polygon = ShapelyPolygon(new_shape)
    for existing_shape in occupied_positions:
        existing_polygon = ShapelyPolygon(existing_shape)
        if new_polygon.intersects(existing_polygon):
            return True  # If there's an intersection, the shapes overlap
    return False  # No overlap

# Create the shapes for each country
for i, row in df.iterrows():
    # Generate a random shape based on the population fraction
    while True:
        points = generate_random_shape(row['Normalized Population'], radius)

        # Check if the new shape overlaps with any existing shapes
        if not check_overlap(points, occupied_positions):
            occupied_positions.append(points)
            # Create the polygon (random shape) and add it to the plot
            polygon = Polygon(points, closed=True, edgecolor='black', facecolor=colors[i % len(colors)], linewidth=1.5)
            ax.add_patch(polygon)
            break

# Remove axes and labels for a clean circle
ax.set_xlim(-1.2, 1.2)  # Adjusted to give more space around the circle
ax.set_ylim(-1.2, 1.2)  # Adjusted to give more space around the circle
ax.axis('off')

# Display the plot
plt.show()
