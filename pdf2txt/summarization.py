"""
    In this file I will compare different similarity algorithms and will try to summarize
    the text in a scientific article getting the most relevant n sentences.
"""

# import packages
import os
import re
import numpy as np


# function to clean text
def clean_text(t):
    # remove non-ascii characters
    t = t.encode("ascii", "ignore").decode()
    # replace line breaks with single spaces
    t = re.sub("\n+", " ", t)
    return t


# function to compute jaccard similarity between two sentences
def jaccard_similarity(sentence1, sentence2):
    try:
        s1 = set(sentence1)
        s2 = set(sentence2)
        return round(float(len(s1.intersection(s2)) / len(s1.union(s2))), 3)
    except Exception:
        return 0.0


# function to summarize text
def summarize(t, n):
    t = t.split('.')
    t = [sentence.lstrip() for sentence in t]
    # create initial similarity matrix
    similarity_matrix = np.zeros((len(t), len(t)))
    for i in range(similarity_matrix.shape[0]):
        for j in range(i+1, similarity_matrix.shape[1]):
            similarity_matrix[i][j] = jaccard_similarity(t[i].split(), t[j].split())
    print(similarity_matrix)
    return t


# define data path
data_path = "D:/GitHub/PatientReportedOutcome/data/pdf_txt/"

# get and store txt file
file = [data_path + f for f in [f for f in os.listdir(data_path) if f.endswith("txt")]][0]
with open(file, 'r', encoding='utf-8') as f:
    text = f.read()

# clean text
text = clean_text(text)
text = summarize(text, 0)

print(text[:10])
# print(text[:550] + '\n\n' + clean_text(text)[:550])
