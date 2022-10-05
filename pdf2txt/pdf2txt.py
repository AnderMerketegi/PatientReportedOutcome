"""
    This file will be used to try different libraries to extract text from pdf files
"""

# import packages
import os
from PyPDF2 import PdfReader
from pdfminer.high_level import extract_text

data_path = "D:/GitHub/PatientReportedOutcome/data/pdf_img/"

# get n pdf file
file = [data_path + f for f in [f for f in os.listdir(data_path) if f.endswith("pdf")]][0]

# we will try several options and compare the txt file obtained from all of them
options = { 1: "PyPDF2",
            2: "pdfminer"
          }

sel = options[1]

# create text file with the method selected above
with open(file[:-4] + f"_{sel}.txt", "w", encoding="utf-8") as f:

    if sel == "PyPDF2":
        # create pdf object
        pdf = PdfReader(file)

        # extract text from all pdf pages
        text = ""
        for page in pdf.pages:
            text += page.extractText()
        f.write(text)

    elif sel == "pdfminer":
        text = extract_text(file, 'rb')
        f.write(text)
