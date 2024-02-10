import csv
import pandas as pd

file_path = '/Users/cksash/Downloads/allegheny/250969492_AHN-Wexford-Hospital_standardcharges.csv'
# lines = open(file_path, 'r').readlines()

# def clean_data():
#     by_size = {}
#
#     for l in csv.reader(lines, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True):
#         cols = len(l)
#         if cols not in by_size:
#             by_size[cols] = []
#
#         by_size[cols].append(l)
#
#     print (f"Rows of {len(by_size)} different sizes found")
#
#     dfs = []
#
#     for size, rows in by_size.items():
#         df = pd.DataFrame(data=rows)
#         dfs.append(df)
#
#         if df.shape[0] < 100:
#             continue
#
#         print(df.shape)
#         print(df.loc[:5])

if __name__ == '__main__':
    data = pd.read_csv(file_path, encoding='unicode_escape', skiprows=[0, 1])
    cpt_data = data[data['code|1|type'] == 'CPT']
    cpt_data = cpt_data[['description', 'code|1', 'code|1|type', 'standard_charge|min', 'standard_charge|max']]
    cpt_data = cpt_data.dropna()
    print(f"Dataset size: {cpt_data.shape}")
    cpt_data.to_csv('wexford_clean.csv')

