```python
$pip install a-pandas-ex-split-on-common-string
from a_pandas_ex_split_on_common_string import pd_add_split_on_common_string
pd_add_split_on_common_string()
df = pd.read_csv("https://raw.githubusercontent.com/pandas-dev/pandas/main/doc/data/titanic.csv")
df['text'] = 'myway_/bo' + df.Embarked.astype('string') + '.txt'
print(df.text.s_split_on_common_string(is_path=False))
print(df.text.s_split_on_common_string(is_path=True))

		aa_original  aa_common aa_different
0    myway_/boS.txt  myway_/bo        S.txt
1    myway_/boC.txt  myway_/bo        C.txt
2    myway_/boS.txt  myway_/bo        S.txt
3    myway_/boS.txt  myway_/bo        S.txt
4    myway_/boS.txt  myway_/bo        S.txt
..              ...        ...          ...
886  myway_/boS.txt  myway_/bo        S.txt
887  myway_/boS.txt  myway_/bo        S.txt
888  myway_/boS.txt  myway_/bo        S.txt
889  myway_/boC.txt  myway_/bo        C.txt
890  myway_/boQ.txt  myway_/bo        Q.txt
[891 rows x 3 columns]
		aa_original aa_common aa_different
0    myway_/boS.txt    myway_     /boS.txt
1    myway_/boC.txt    myway_     /boC.txt
2    myway_/boS.txt    myway_     /boS.txt
3    myway_/boS.txt    myway_     /boS.txt
4    myway_/boS.txt    myway_     /boS.txt
..              ...       ...          ...
886  myway_/boS.txt    myway_     /boS.txt
887  myway_/boS.txt    myway_     /boS.txt
888  myway_/boS.txt    myway_     /boS.txt
889  myway_/boC.txt    myway_     /boC.txt
890  myway_/boQ.txt    myway_     /boQ.txt
[891 rows x 3 columns]
```
