import pandas as pd
df = pd.concat(pd.read_excel(
    r'Новое учебное меню.xlsx', sheet_name=None), ignore_index=True)

df.drop(columns=df.columns[0], axis=1, inplace=True)
df.drop(columns=df.columns[1], axis=1, inplace=True)
df = df.to_dict('dict')
name = input()
matches = [x for x in df['Unnamed: 1'].values()if isinstance(x, str) and name in  x]
if len(matches) > 1:
    print("Choose one type")
    print(matches)
    a = int(input())
    matches = matches[a-1]
print(matches)
matches = ''.join(matches)


def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k


key = get_key(df['Unnamed: 1'], matches)
print(df['Unnamed: 3'].get(key))
print(df['Unnamed: 4'].get(key))
