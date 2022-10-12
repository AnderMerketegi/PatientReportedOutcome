"""
    This file will be used to try different libraries to extract text from pdf files
"""

# import packages
import os
import glob
import shutil

from PyPDF2 import PdfReader
from pdfminer.high_level import extract_text
import fitz
from langdetect import detect


# function to convert pdf files to txt files making use of the specified tool
def pdf2txt(file, tool):
    # extract text file with the method specified in "tool"
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

    else:
        print("Selected tool is not available.")
        return None, None

    return text, len(text.split())


# define function to get the percentage of text area in respect of the whole page areas
def get_text_percentage(file):
    # initialize total page area and text area
    total_page_area = 0.0
    total_text_area = 0.0
    # read file using fitz library
    document = fitz.open(file)
    # iterate over the pages and compute the text area
    for page_n, page in enumerate(document):
        # add the total area of the page
        total_page_area += abs(page.rect)
        # get blocks that contain text within the page
        text_blocks = page.get_textpage().extractBLOCKS()
        current_text_area = 0.0
        if text_blocks:
            # calculate the text area for each block within the page
            for block in text_blocks:
                current_text_area += abs(fitz.Rect(block[:4]))
            total_text_area += current_text_area
        else:
            continue
    # close document
    document.close()
    return int((total_text_area / total_page_area) * 100)


# define function that detects the language of the article
def detect_language(text):
    return detect(text)


# define function to convert all documents in file, making use of specified tool and saving the text file in output file
def convert_documents(tool, path, output_path):
    # check if output_path exists - if not, create path
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    # get all pdf files from path
    documents = glob.glob(path + "*.pdf")
    print(f"\n{len(documents)} documents ready to be converted.")
    # initialize document counters
    scanned_documents = 0
    text_documents = 0
    for document in documents:
        # do not convert if document has already been converted
        if not os.path.exists(output_path + document.split('\\')[-1][:-3] + "txt"):
            # compute text ratio in document - if text percentage is lower than 10%: skip document
            text_ratio = get_text_percentage(document)
            # if text_ratio < 10% consider it as a scanned pdf
            if text_ratio > 10:
                try:
                    # get text and number of words
                    text, n_words = pdf2txt(document, tool)
                    # detect language of document and create folder to store if necessary
                    language = detect_language(text)
                    if not os.path.exists(f"{output_path}{language}/"):
                        os.mkdir(f"{output_path}{language}/")
                    with open(f"{output_path}{language}/" + document.split('\\')[-1][:-3] + "txt", "w", encoding="utf-8") as f:
                        f.write(text)
                    text_documents += 1
                except Exception:
                    print(f"Unable to process document {document}")
                    if not os.path.exists(path + "error/"):
                        os.mkdir(path + "error/")
                    shutil.move(document, path + "error/" + document.split('\\')[-1][:-3] + "pdf")
                    continue
            else:
                scanned_documents += 1
                # sent to error folder if the document was not converted to text
                if not os.path.exists(path + "img/"):
                    os.mkdir(path + "img/")
                shutil.move(document, path + "img/" + document.split('\\')[-1][:-3] + "pdf")
    print(f"{text_documents} documents converted ---- {scanned_documents} scanned documents.")


#################### ---------- MAIN ---------- ####################


# define data_path
data_path = "D:/GitHub/Data/PRO/"
# available tools for text extraction from pdf files
options = {1: "PyPDF2", 2: "pdfminer", 3: "fitz"}
# convert documents located in data_path and store them in output_path
convert_documents(options[2], data_path, data_path + "txt/")
