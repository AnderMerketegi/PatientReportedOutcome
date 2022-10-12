"""
    In this file I will create a function to get all dataframe rows that belong to class 0 (noPRO) and create a single
    dataframe with all the articles for future operations.
"""

# import packages
import os.path

import pandas as pd
import glob
import shutil


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


# define function to separate text files depending on the year - taking splitted pdf files as reference
def separate_documents(pdf_path, txt_path):
    # get pdf filenames from corresponding pdf_path (year)
    pdf_filenames = [file.split("\\")[-1][:-4] for file in glob.glob(pdf_path + "/*.pdf")]
    txt_filenames = [file.split("\\")[-1][:-4] for file in glob.glob(txt_path + "/*.txt")]
    # define summaries path to replicate exercise
    sum_path = txt_path + "summaries/"
    # get year
    year = pdf_path.split("/")[-2]
    # create new folder if it does not exist
    if not os.path.exists(txt_path + year + "/"):
        new_path = txt_path + year + "/"
        os.mkdir(new_path)
    if not os.path.exists(sum_path + year + "/"):
        new_sum_path = sum_path + year + "/"
        os.mkdir(new_sum_path)
    for txt_file in txt_filenames:
        if txt_file in pdf_filenames:
            shutil.move(txt_path + txt_file + ".txt", new_path + txt_file + ".txt")
            shutil.move(sum_path + txt_file + "_sum.txt", new_sum_path + txt_file + "_sum.txt")


#################### ---------- MAIN ---------- ####################


data_path = "D:/GitHub/Data/2013-14/"
txt_path = "D:/GitHub/Data/noTITOL/txt/en/"
separate_documents(data_path, txt_path)