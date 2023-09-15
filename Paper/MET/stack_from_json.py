import json
import matplotlib.pyplot as plt
import numpy as np

# Load the JSON data from file
with open('my_file.json', 'r') as f:
    data = json.load(f)

label = data['selection']

# Create a list of values for the histogram
hist_values = [v for k, v in data.items() if k != 'selection' and isinstance(v, float)]

total_sum = sum(hist_values)

y_limit = 2 * total_sum
colors = ['blue', 'green', 'red', 'purple', 'orange', 'orange']

bin_edges = np.linspace(min(hist_values), max(hist_values), 10)

# Create a histogram with the computed bin edges
for i, (key, value) in enumerate(data.items()):
    if key != 'selection' and isinstance(value, float):
        plt.hist(value, bins=bin_edges, stacked=True, label=key, color=colors[i])

# Set the x-axis tick labels to the selection label
plt.xticks([0.5], [label])
plt.ylim([0, y_limit])

# Add legend and axis labels
plt.legend()
plt.xlabel(label)
plt.ylabel('count')


# Save the plot to file
plt.savefig('plot.png')


