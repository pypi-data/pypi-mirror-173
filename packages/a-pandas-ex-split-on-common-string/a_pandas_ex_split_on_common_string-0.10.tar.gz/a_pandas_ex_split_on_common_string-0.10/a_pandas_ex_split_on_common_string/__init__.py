import re
from typing import Union
from pandas.core.frame import Series
import regex
from a_pandas_ex_df_to_string import ds_to_string
from a_pandas_ex_plode_tool import explode_lists_and_tuples_in_column
import pandas as pd


def series_to_dataframe(
    df: Union[pd.Series, pd.DataFrame]
) -> (Union[pd.Series, pd.DataFrame], bool):
    dataf = df.copy()
    isseries = False
    if isinstance(dataf, pd.Series):
        columnname = dataf.name
        dataf = dataf.to_frame()

        try:
            dataf.columns = [columnname]
        except Exception:
            dataf.index = [columnname]
            dataf = dataf.T
        isseries = True

    return dataf, isseries


def split_series_on_common_string(df: pd.Series, is_path: bool = False) -> pd.DataFrame:
    r"""
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


    """
    originalindexalle = df.index.__array__().copy()
    df_orig = df.copy()
    df_orig = df_orig.reset_index(drop=True)
    df2 = ds_to_string(df_orig.dropna()).to_frame()
    df2, isseries = series_to_dataframe(df2)
    df2.columns = ["aa_original"]
    df2["aa_original"] = df2["aa_original"].astype("string")
    fpath = explode_lists_and_tuples_in_column(df2["aa_original"].str.split(""))
    com_string = ""
    for col in fpath.columns:
        if len(fpath[col].unique()) == 1:
            com_string += str(fpath[col].unique()[0])
        else:
            break
    if is_path:
        com_string = regex.sub(r"[\\/]+[^\\/]+$", "", com_string)
    comstringregex = re.compile(fr"(^{re.escape(com_string)})(.*)$")
    resu = df2["aa_original"].str.extract(comstringregex)
    resu.columns = ["aa_common", "aa_different"]
    resunew = pd.concat([df2, resu], axis=1, ignore_index=True)
    missing = list(set(df_orig.index.to_list()) - set(resunew.index.to_list()))
    if any(missing):
        for mi in missing:
            resunew.loc[mi] = [pd.NA, pd.NA, pd.NA]
    resunew = resunew.sort_index()
    resunew.index = originalindexalle.copy()
    resunew.columns = ["aa_original", "aa_common", "aa_different"]
    return resunew


def pd_add_split_on_common_string():
    Series.s_split_on_common_string = split_series_on_common_string
