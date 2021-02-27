#!/usr/bin/env python3

# dependencies
import seaborn as sns
import scipy.stats as stats
import matplotlib.pyplot as plt

# settings for seaborn plotting style
sns.set(color_codes=True)

# settings for seaborn plot sizes
sns.set(rc={'figure.figsize':(5,5)})

# we need to plot a distribution that we can mimick server activity with
dist = stats.poisson.rvs(mu=10, size=100, random_state=64)
print(dist)

# plot the distribution
ax = sns.distplot(dist, kde=False, bins=30, color="steelblue")
ax.set(xlabel='Poisson Distribution', ylabel='Frequency')
plt.show()