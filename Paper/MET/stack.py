import matplotlib.pyplot as plt

# Define the dictionary with the data
my_dict = {'apples': [3, 2, 1], 'bananas': [2, 3, 4], 'oranges': [1, 2, 3]}

# Create a list of the labels for the x-axis
labels = ['Group 1', 'Group 2', 'Group 3']

# Create a list of the colors for the bars
colors = ['r', 'g', 'b']

# Create a list of the bottom values for the bars (initialized to 0)
bottom_values = [0] * len(labels)

# Loop over the keys in the dictionary and create a bar for each key
for key in my_dict.keys():
    values = my_dict[key]
    plt.bar(labels, values, bottom=bottom_values, color=colors.pop(0))
    bottom_values = [sum(x) for x in zip(bottom_values, values)]

# Add a legend
plt.legend(my_dict.keys())

# Add labels for the x-axis and y-axis
plt.xlabel('Groups')
plt.ylabel('Values')

# Display the plot
#plt.show()
plt.savefig('my_plot.png')
