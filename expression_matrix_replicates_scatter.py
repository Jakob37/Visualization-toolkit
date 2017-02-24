#!/usr/bin/env python3

"""
Visualize a pair of samples for particular feature as categorical scatter representing
intensity values for each replicate.
"""


import argparse
import pandas as pd
import seaborn as sns
import sys
import re


def main():

    args = parse_arguments()

    if args.target_row_label is None and args.row_label_file is None:
        print('You must provide either target_row_label or row_label_file')
        sys.exit(1)

    df = pd.read_csv(args.csv, index_col=0, delimiter=args.delim, engine='python')
    df.index = df.index.to_series().astype(str)

    #row = args.target_row_label
    target_rows = get_rows(args)

    s1_cols = [c for c in list(df) if re.match(args.s1_pattern, c)]
    s2_cols = [c for c in list(df) if re.match(args.s2_pattern, c)]

    if len(s1_cols) + len(s2_cols) == 0:
        print('No columns matching provided col patterns')
        sys.exit(1)

    y_name = 'sample intensities'

    raw_s1_df = df.ix[target_rows, s1_cols]
    long_s1_df = setup_long_df(raw_s1_df, target_rows, 's1', y_name)

    raw_s2_df = df.ix[target_rows, s2_cols]
    long_s2_df = setup_long_df(raw_s2_df, target_rows, 's2', y_name)

    merged_s = pd.concat([long_s1_df, long_s2_df])
    
    sns.stripplot(data=merged_s, x='feature', y='log2_intensity', hue='sample')
    sns.plt.title('Sample replicate comparison')
    sns.plt.show()


def get_rows(args):

    row_labels = list()

    if args.row_label_file:
        with open(args.row_label_file) as in_fh:
            for line in in_fh:
                line = line.rstrip()
                row_labels.append(line)
    elif args.target_row_label:
        row_labels.append(args.target_row_label)
    else:
        raise Exception("Neither row_label_file or target_row_label option found")
    return row_labels


def setup_long_df(raw_sample_df, target_rows, sample_name, y_name):

    s_df = pd.DataFrame({
        'log2_intensity': [],
        'feature': [],
        'sample': []})
    for col in raw_sample_df:
        col_data = raw_sample_df[col]
        sub_df = pd.DataFrame({
            'log2_intensity': col_data,
            'feature': target_rows,
            'sample': sample_name
            })
        s_df = pd.concat([s_df, sub_df])
    return s_df


def parse_arguments():

    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', required=True)
    parser.add_argument('--s1_pattern', required=True)
    parser.add_argument('--s2_pattern', required=True)

    parser.add_argument('--target_row_label')
    parser.add_argument('--row_label_file')

    parser.add_argument('--delim', default='\t')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main()
