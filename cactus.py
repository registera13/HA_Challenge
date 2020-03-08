import pandas
from pathlib import Path
file = Path('hg2_min_3_min_4.bed')
p_num = 'hg2'
h_lower = -2
h_upper = 0.7
min_cont = 15

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="""Process bed files of variants""")
    parser.add_argument("filename", help="file name", type=str, )
    #                        # nargs='+')
    parser.add_argument("contiguous_count",
                        help="number of homozygous contiguous variants", type=int)
    parser.add_argument('-homz_lower', help='below this negative float is considered '
                                            'homozygous', type=float, default=-2)
    parser.add_argument('-homz_upper', help='above this positive float is considered '
                                            'homozygous', type=float, default=0.7)
    args = parser.parse_args()
    file = Path(args.filename)
    p_num = file.name.split('_')[0]
    h_lower = args.homz_lower
    h_upper = args.homz_upper
    min_cont = args.contiguous_count

# genes = pandas.read_csv('Data Files/Data Files/hg19_genes.tsv', '\t')
# exons = pandas.read_csv('Data Files/Data Files/hg19_exon_locations.tsv', '\t',
#                         header=None)
unique_df = pandas.read_csv(file, '\t', header=None)
unique_df.columns = ['chr', 'start', 'end', 'reference', 'alternate', 'ref reads',
                     'alt reads']
# Create a column for computing the homozygosity
v_df_p1 = pandas.concat([unique_df,
                         pandas.Series(1 - unique_df['ref reads'] /
                                       unique_df['alt reads'], name='homr')],
                        axis=1)
in_length = len(unique_df)
del unique_df
pandas.options.mode.use_inf_as_na = False
v_df_p1 = v_df_p1.dropna()  # Remove the nan values for where there are 0s
#                               # in both reads
# Create a column for Boolean value of homozygous (includes deletions)
v_df_p2 = pandas.concat([v_df_p1,
                         pandas.Series((v_df_p1['homr'] > h_upper) |
                                       (v_df_p1['homr'] < h_lower), name='homz')],
                        axis=1)
del v_df_p1


def get_contiguous_homozygous(df_w_homz, min_count) -> pandas.DataFrame:
    interval_len = 0
    interval_start = None
    interval_end = None
    under_min_count = min_count - 1
    interval_df = pandas.DataFrame(columns=['chr', 'start', 'end', 'variant count'])
    for ind, row in df_w_homz.iterrows():
        if row['homz']:
            if interval_len == 0:
                interval_start = row['chr':'end']
                interval_end = row['end']
                interval_len = 1
            elif row['chr'] == interval_start[0]:
                interval_end = row['end']
                interval_len += 1

        else:
            if interval_len > under_min_count:
                interval_df.loc[len(interval_df)] = [interval_start[0], interval_start[1],
                                                     interval_end, interval_len]
            interval_len = 0
    return interval_df


cont_bed = get_contiguous_homozygous(v_df_p2, min_cont)
cont_bed.to_csv('{}_homz_cont_{}.bed'.format(p_num, min_cont), '\t', index=False)
print('Input was {} lines, Output is only {} lines!'.format(in_length, len(cont_bed)))
