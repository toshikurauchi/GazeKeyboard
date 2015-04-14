import pandas as pd
import sys

filename = 'predictions.csv'
if len(sys.argv) > 1:
    filename = sys.argv[1]

def print_statistics(df, group_by):
    groups = df.groupby(group_by)
    totals = groups['trial'].count()

    print 'FOUND:'
    print groups['found'].sum()/totals

    print
    print 'INDEX MEAN:'
    print groups['found_idx'].mean()

    print
    print 'INDEX MAX:'
    print groups['found_idx'].max()

    print
    print 'TOP 1:'
    print df[df['found_idx'] == 0].groupby(group_by)['found'].count()/totals

    print
    print 'AMONG TOP 5:'
    print df[df['found_idx'] < 5].groupby(group_by)['found'].count()/totals

df = pd.read_csv(filename)

print_statistics(df, ['layout', 'mode'])
print_statistics(df, ['sbj', 'layout', 'mode'])
