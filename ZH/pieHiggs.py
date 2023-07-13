import matplotlib.pyplot as plt

# Pie chart
labels = ['bb', 'cc',  '$\tau \tau$', '$\mu$\mu$', 'WW*', 'ZZ*', 'gg', 'gammagamma', 'Zgamma']
sizes = [58.2, 2.9, 6.3, 0.02, 21.4, 2.6, 8.2, 0.23, 0.15]
# only "explode" the 2nd slice (i.e. 'Hogs')
explode = (0, 0.1, 0, 0, 0,0,0,0,0)
fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
# Equal aspect ratio ensures that pie is drawn as a circle
ax1.axis('equal')
plt.tight_layout()
plt.show()

