"""
    In this file I will try to see the difference between scientific articles that contain a PRO questionnaire and
    articles that do not have any PRO instrument.
"""

# import packages
import glob
import os
import re
import shutil
import pandas as pd


# function to divide the articles depending on the class -- PRO vs NO_PRO
def preprocess_data(files_path, excel_path, path1, path0):
    # read and store excel file as dataframe
    excel_file = pd.read_excel(excel_path)
    # check that number of articles correspond to shape[0]
    titol_filenames = [file for file in glob.glob(files_path + "*.pdf")]
    # get id number from filename and store in list
    id_filename = {}
    for fn in titol_filenames:
        # modify filenames for splitting and get first element (id)
        fileid = re.sub(r"( |-)", "_", fn.split('\\')[-1]).split("_")[0].lstrip("0")
        # if filename does not contain any of the above characters, filename is the id
        try:
            id_filename[int(fileid)] = fn
        except Exception:
            id_filename[int(fileid.split(".")[0])] = fn
    # initialize counters
    c0 = 0
    c1 = 0
    for fileid, filename in list(id_filename.items()):
        # get row from excel file
        row = excel_file[excel_file["refid"] == fileid]
        # get class of document - 1 or 0
        try:
            y = row["filtro_instrumento"].values[0]
        except Exception:
            print(f"Missing value - Row: {row}\nArticle refid: {fileid}")
            continue
        # copy file to folder depending on class
        if y == 1:
            c1 += 1
            shutil.copy(filename, path1 + filename.split('\\')[-1])
        else:
            c0 += 1
            shutil.copy(filename, path0 + filename.split('\\')[-1])

    # make sure that all articles were moved to a new folder
    assert ((c1 + c0) == len(set(excel_file[excel_file["filtro_titol"] == 1]["refid"])))
    # print number of documents moved from each class
    print(f"Class 1 articles added to corresponding folder: {c1}\nClass 0 articles added to corresponding folder: {c0}")


#################### ---------- MAIN ---------- ####################


# define paths
data_path = "D:/GitHub/Data/"
files_path = data_path + "2016/"
excel_path = data_path + "bd_2016.xlsx"

# create new folders if they do not exist - PRO and NO_PRO
pro_path = data_path + "PRO/"
nopro_path = data_path + "noPRO/"
if not os.path.isdir(pro_path):
    os.mkdir(pro_path)
if not os.path.isdir(nopro_path):
    os.mkdir(nopro_path)

# call to function
preprocess_data(files_path, excel_path, pro_path, nopro_path)
