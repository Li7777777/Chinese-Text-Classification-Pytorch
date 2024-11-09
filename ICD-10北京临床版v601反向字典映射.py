import pandas as pd
import json


df = pd.read_excel('./CHIP-CDN/国际疾病分类 ICD-10北京临床版v601.xlsx',header=None)
df.columns = ['ICD10', 'cName']
print("Loading data...")
print(df.head())
# 以cName为key，ICD10为value的字典，如果有重复的cName，value存为list
cName_dict = {}
for index, row in df.iterrows():
    if row['cName'] in cName_dict:
        cName_dict[row['cName']].append(row['ICD10'])
    else:
        cName_dict[row['cName']] = [row['ICD10']]
print("Dictionary created.")
# print(cName_dict)
# 保存字典为json文件

with open('./CHIP-CDN/cName_idc10.json', 'w', encoding='utf-8') as f:
    json.dump(cName_dict, f, ensure_ascii=False, indent=4)
print("Dictionary saved.")
