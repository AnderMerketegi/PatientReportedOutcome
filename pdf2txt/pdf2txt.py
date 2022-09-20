# import packages
import random
import os

from PyPDF2 import PdfFileReader
import slate3k as slate
from pdfminer.high_level import extract_text


data_path = "C:/Users/Ander Merketegi/Desktop/GitHub/Data/PatientReportedOutcome/Files/2013_14/"

# get n pdf file
n = random.randint(0, len(os.listdir(data_path)))
file = data_path + os.listdir(data_path)[n]

# we will try several options and compare the txt file obtained from all of them
options = { 1: "PyPDF2",
            2: "slate3k",
            3: "pdfminer"
          }

sel = options[3]

# create text file with the method selected above
with open(file[:-4] + "_pypdf.txt", "w", encoding="utf-8") as f:

    if sel == "PyPDF2":
        # create pdf object
        pdf = PdfFileReader(file)

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
