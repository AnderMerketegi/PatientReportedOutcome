"""
    In this script I will create the required function in order to download pdf articles from pubmed given pubmed identifiers.
    This way, I will be able to expand the dataset and thus, obtain more training articles

    In order to downlaod pubmed articles, the following package will be employed: https://pypi.org/project/pubmed2pdf/
"""

# import packages
import glob
import os
import pandas as pd
import shutil

# define function to get pubmed identifiers from dataframe[colname]
def get_ids_from_df(df, colname):
    print(len(df))
    return [str(id[3:]) for id in list(df[colname])]


# function to download articles from pubmed given a list of identifiers and move pdf files from default path to destination path
def pubmed_download(ids, default_path, dest_path):
    # a total of 6620 pubmed identifiers
    for index, id in enumerate(ids):
        try:
            # call terminal command to download article
            os.system('''pubmed2pdf pdf --pmids="''' + id + '''"''')
        except Exception:
            print(f"Unable to download the article with pmid = {id}")
            continue
        if index % 20 == 0 and index > 0:
            print(f"\n{index} articles downloaded\n")
            # move files every 20 downloaded articles
            move_files(default_path, dest_path)


# function to move files from default download path to output path
def move_files(orig_path, dest_path):
    # check that both directories exist
    if not os.path.exists(orig_path):
        print("Default path not found.")
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)
        print("Destination path not found. Created.")
    # get pdf files from specified folder
    pdf_files = glob.glob(orig_path + "*.pdf")
    print(f"{len(pdf_files)} articles found.")
    for file in pdf_files:
        filename = file.split("\\")[-1]
        # move articles to destination path
        shutil.move(file, dest_path + filename)
    print("\nArticles moved succesfully.")


#################### ---------- MAIN ---------- ####################


# define data path
data_path = "D:/GitHub/Data/"
no_titol = pd.read_csv(data_path + "no_titol_df.csv").drop(columns = ["Unnamed: 0"])
# get pubmed identifiers from dataframe
pubmed_ids = get_ids_from_df(no_titol, "pmid")
# by default, all files are downloaded to path: "C:/Users/Ander Merketegi/pubmed2pdf"
default_path = "C:/Users/Ander Merketegi/pubmed2pdf/"
# download articles
pubmed_download(pubmed_ids, default_path, data_path + "noTITOL/")


