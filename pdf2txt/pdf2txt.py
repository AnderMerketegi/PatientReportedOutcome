"""
    This file will be used to try different libraries to extract text from pdf files
"""

# import packages
import os
import glob
from PyPDF2 import PdfReader
from pdfminer.high_level import extract_text
import fitz


# function to convert pdf files to txt files making use of the specified tool
def pdf2txt(file, tool):
    # create text file with the method specified in "tool"
    with open(file[:-4] + f"_{tool}.txt", "w", encoding="utf-8") as f:
        if tool == "PyPDF2":
            # create pdf object
            pdf = PdfReader(file)
            # extract text from all pdf pages
            text = ""
            for page in pdf.pages:
                text += page.extractText()


        # working best for now
        elif tool == "pdfminer":
            text = extract_text(file, 'rb')

        elif tool == "fitz":
            text = ""
            doc = fitz.open(file)
            for page in doc:
                text += page.get_text()

    print(f"File created -> {file[:-4] + f'_{tool}.txt'}")
    return text, len(text.split())


# define function to convert all documents in file, making use of specified tool and saving the text file in output file
def convert_documents(tool, path, output_path):
    # check if output_path exists - if not, create path
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    # get all pdf files from path
    documents = glob.glob(path + "*.pdf")
    print(f"{len(documents)} documents will be converted")
    for document in documents:
        try:
            with open(output_path + document.split('\\')[-1][:-3] + "txt", "w", encoding="utf-8") as f:
                text, n_words = pdf2txt(document, tool)
                f.write(text)
        except Exception:
            print(f"Unable to process document {document}")
            continue


#################### ---------- MAIN ---------- ####################


# define data_path
data_path = "D:/GitHub/PatientReportedOutcome/data_sample/pdf_txt/"
# get one pdf file - n=0
file = [data_path + f for f in [f for f in os.listdir(data_path) if f.endswith("pdf")]][0]
# available tools for text extraction from pdf files
options = {1: "PyPDF2", 2: "pdfminer", 3: "fitz"}

# text, n_words = pdf2txt(file, options[1])
convert_documents(options[2], data_path, data_path + "txt/")