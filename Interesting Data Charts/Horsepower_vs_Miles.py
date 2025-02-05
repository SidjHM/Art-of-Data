import altair as alt
from vega_datasets import data

# Load the cars dataset
cars = data.cars()

# Create a bubble chart
bubble_chart = alt.Chart(cars).mark_circle().encode(
    x='Horsepower',
    y='Miles_per_Gallon',
    size='Weight_in_lbs',
    color='Origin',
    tooltip=['Name', 'Horsepower', 'Miles_per_Gallon', 'Weight_in_lbs']
).properties(
    title='Horsepower vs Miles per Gallon (Bubble Size by Weight)'
).interactive()

# Save as an HTML file
bubble_chart.save('bubble_chart.html')
