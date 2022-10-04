# import packages
import random
import os

from PyPDF2 import PdfReader
import slate3k as slate
from pdfminer.high_level import extract_text

data_path = "D:/GitHub/PatientReportedOutcome/data/pdf_txt/"

# get n pdf file
file = [data_path + f for f in [f for f in os.listdir(data_path) if f.endswith("pdf")]][0]

# we will try several options and compare the txt file obtained from all of them
options = { 1: "PyPDF2",
            2: "slate3k",
            3: "pdfminer"
          }

sel = options[3]

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

    elif sel == "slate3k":
        text = slate.PDF(open(file, 'rb')).text()
        f.write(text)

    elif sel == "pdfminer":
        text = extract_text(file, 'rb')
        f.write(text)
