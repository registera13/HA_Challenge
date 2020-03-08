# python3
# Nick Weiner

import pandas
from pathlib import Path
file = Path('hg2_3_4_intersect.tsv')
p_num = 'hg2'
h_upper = 0.7

if __name__ == "__main__":
    import argparse
    from pathlib import Path
    parser = argparse.ArgumentParser(description="""Process bed files of variants""")
    parser.add_argument("filename", help="file name", type=str, )
    parser.add_argument('-homz_upper', help='above this positive float is considered '
                                            'homozygous', type=float, default=0.7)
    args = parser.parse_args()
    file = Path(args.filename)
    p_num = file.name.split('_')[0]
    h_upper = args.homz_upper

intersect_input: pandas.DataFrame = pandas.read_csv(file, '\t', header=None)
intersect_input.columns = ['ex_chr', 'ex_start', 'ex_end', 'src', 'chr', 'start', 'end',
                           'reference', 'alternate', 'ref reads', 'alt reads']
intersect_input = intersect_input.drop(columns=['ex_chr', 'ex_start', 'ex_end'])
intersect_input.sort_values(by=['chr', 'start', 'end', 'src'])
# Format, Chd, Fth, Mth
# GT    0|1     0|0 0|0
# GT    0|0     0|1 0|0
# GT    0|0     0|0 0|1
intersect_input = pandas.concat([intersect_input,
                                 pandas.Series(1 - intersect_input['ref reads'] /
                                               intersect_input['alt reads'],
                                               name='homr')],
                                axis=1)
vcf_df = pandas.DataFrame(columns=['chr', 'start', 'reference', 'alternate',
                                   'FORMAT', 'chd', 'fth', 'mth'])

last_pos = ''
h_dict_blank: dict = {'chd': '0|0', 'fth': '0|0', 'mth': '0|0'}
h_dict = h_dict_blank
for i in range(len(intersect_input)):
    this_pos = intersect_input.iloc[i]['chr':'alternate'].to_list()
    if last_pos == '':
        last_pos = this_pos
    if this_pos != last_pos:
        vcf_df.loc[len(vcf_df)] = [last_pos[0], last_pos[1],
                                   last_pos[2], last_pos[3],
                                   'GT', h_dict['chd'], h_dict['fth'], h_dict['mth']]
        h_dict: dict = h_dict_blank
    if intersect_input.loc[i]['homr'] > h_upper:
        h_dict[intersect_input.iloc[i]['src']] = '1|1'
    else:
        h_dict[intersect_input.iloc[i]['src']] = '0|1'
    last_pos = this_pos
vcf_df.loc[len(vcf_df)] = [last_pos[0], last_pos[1],  last_pos[2], last_pos[3],
                           'GT', h_dict['chd'], h_dict['fth'], h_dict['mth']]
vcf_df.to_csv('{}.vcf'.format(p_num), '\t', index=False)
