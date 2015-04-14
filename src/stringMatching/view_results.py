import pandas as pd

df = pd.DataFrame.from_csv('predictions.csv')
groups = df.groupby(['layout', 'mode'])
print 'Found:'
print groups['found'].sum()

print
print 'Index:'
print groups['found_idx'].mean()
