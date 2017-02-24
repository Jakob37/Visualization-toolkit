#!/usr/bin/env python3

"""
Visualize a pair of samples for particular feature as categorical scatter representing
intensity values for each replicate.
"""


import argparse
import pandas as pd
import seaborn as sns


def main():

    args = parse_arguments()
    df = pd.read_csv(args.csv, index_col=0)
    df.index = df.index.to_series().astype(str)

    row = args.target_row_label

    sample1_cols = [int(s) for s in args.sample1_cols.split(',')]
    sample2_cols = [int(s) for s in args.sample2_cols.split(',')]

    y_name = 'sample intensities'

    s1_series = df.ix[row, sample1_cols]
    s1_df = setup_sample_df(s1_series, 's1', y_name)

    s2_series = df.ix[row, sample2_cols]
    s2_df = setup_sample_df(s2_series, 's2', y_name)

    merged_s = pd.concat([s1_df, s2_df])
    
    sns.stripplot(data=merged_s, x='sample', y=y_name)
    sns.plt.title('Sample replicate comparison')
    sns.plt.show()
    

def setup_sample_df(sample_series, sample_name, y_name):

    sample_series.name = y_name
    s_df = sample_series.to_frame()
    s_df['sample'] = sample_name
    return s_df


def parse_arguments():

    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', required=True)
    parser.add_argument('--sample1_cols', required=True)
    parser.add_argument('--sample2_cols', required=True)
    parser.add_argument('--target_row_label', required=True)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main()
