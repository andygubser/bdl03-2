import pandas as pd


input_path = "data_raw"
output_path = "data_prep"
# file = "household_data_1min_singleindex.csv"
file = "household_data_15min_singleindex.csv"
# file = "household_data_60min_singleindex.csv"
path_file = f"{input_path}/{file}"

df60_raw = pd.read_csv(path_file)
ls_cols_string = ["utc_timestamp", "cet_cest_timestamp", "interpolated"]
ls_cols_numeric = list(set(df60_raw.columns) - set(ls_cols_string))

df60_raw_diff = df60_raw
df60_raw_diff[ls_cols_numeric] = df60_raw_diff[ls_cols_numeric].diff().copy()
df60_raw_diff.describe()


def get_df_prepared(df, num):
    df_tmp = df[ls_cols_string + [col for col in df.columns if f"_residential{num}" in col]].copy()
    df_tmp["unit"] = f"residential{num}"
    df_tmp.columns = df_tmp.columns.str.replace(f'DE\_KN\_residential{num}\_', '', regex=True)
    return df_tmp


def get_df_combined(df, max_num):
    df_appended = pd.DataFrame()
    for num in range(max_num):
        print(num)
        df_tmp = get_df_prepared(df, num=num)
        df_appended = pd.concat([df_appended, df_tmp], axis=0, ignore_index=True)
    return df_appended


df_prep = get_df_combined(df60_raw_diff, max_num=5)
df_prep.to_csv(f"{output_path}/prep_{file}")