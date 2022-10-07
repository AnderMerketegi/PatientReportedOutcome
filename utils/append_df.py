"""
    In this file I will create a function to get all dataframe rows that belong to class 0 (noPRO) and create a single
    dataframe with all the articles for future operations.
"""

# import packages
import pandas as pd


# function to append df2 to df1
def append_df(df1, df2):
    # create lists of columns
    df1_cols = list(df1.columns)
    df2_cols = list(df2.columns)
    # check if columns are the same before appending
    if len(df1_cols) != len(df2_cols):
        df1, df2 = insert_columns(df1, df1_cols, df2)
    # check that all filtro_titol values are 0 in df
    df = df1.append(df2, ignore_index=True)
    return df


# function to insert column in corresponding position if columns of two dataframes are not the same
def insert_columns(df1, df1_cols, df2):
    # get columns that are missing in one of the datasets
    missing_cols = list(set(df1.columns).difference(set(df2.columns)).union(set(df2.columns).difference(set(df1.columns))))
    for col_name in missing_cols:
        # if the column is missing in df2, insert new column
        if col_name in df1_cols:
            index = df1.columns.get_loc(col_name)
            new_col = ["" for row in df2.iterrows()]
            df2.insert(index, col_name, new_col)
        else:
            index = df2.columns.get_loc(col_name)
            new_col = ["" for row in df1.iterrows()]
            df1.insert(index, col_name, new_col)
        return df1, df2


#################### ---------- MAIN ---------- ####################


data_path = "D:/GitHub/Data/"
# load the datasets that will be appended
df_2013_2014 = pd.read_excel(data_path + "bd_2013_2014.xlsx")
df_2015 = pd.read_excel(data_path + "bd_2015.xlsx")
df_2016 = pd.read_excel(data_path + "bd_2016.xlsx")
# create a dataframe corresponding to articles that we do not have in our corpus (filtro_titol == 0)
df_2013_2014 = df_2013_2014[df_2013_2014["filtro_titol"] == 0]
df_2015 = df_2015[df_2015["filtro_titol"] == 0]
df_2016 = df_2016[df_2016["filtro_titol"] == 0]
# create dataframe
no_titol_df = append_df(df_2013_2014, append_df(df_2015, df_2016))
# save dataframe for future operations
no_titol_df.to_csv(data_path + "no_titol_df.csv")