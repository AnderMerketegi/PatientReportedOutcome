"""
    In this file I will compare different similarity algorithms and will try to summarize
    the text in a scientific article getting the most relevant n sentences.

    Similarity: Jaccard similarity
    Ranking: Text Rank algorithm
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


# calculate sentence probabilities for ordering using page rank algorithm
def page_rank(similarity_matrix):
    # dumping factor - around 0.85
    damping = 0.85
    # number of iterations
    iter = 100
    # minimum difference from one iteration to other
    min_difference = 1e-6
    # initialize probability list
    probability_list = [1] * similarity_matrix.shape[0]
    # initialize previous probability value
    previous_probability = 0
    for _ in range(iter):
        # compute new probability list
        probability_list = (1 - damping) + damping * np.matmul(similarity_matrix, probability_list)
        # if the difference of probabilities is lower than minimum
        if abs(previous_probability - sum(probability_list)) < min_difference:
            break
        else:
            previous_probability = sum(probability_list)
    return probability_list


# function to summarize text
def summarize(t, n):
    t = t.split('.')
    t = [sentence.lstrip() for sentence in t]
    # create initial similarity matrix
    similarity_matrix = np.zeros((len(t), len(t)))
    for i in range(similarity_matrix.shape[0]):
        for j in range(i+1, similarity_matrix.shape[1]):
            # compute similarity between sentences i and j
            similarity_matrix[i][j] = jaccard_similarity(t[i].split(), t[j].split())

    probability_list = list(enumerate(page_rank(similarity_matrix)))
    # sort probability list in descending order keeping the indexes
    probability_list = list(sorted(probability_list, key = lambda tup: tup[1], reverse = True))
    # get indexes for first n sentences
    selected_indexes = [tup[0] for tup in probability_list][:n]
    # get selected sentences and return
    selected_sentences = [t[i] for i in selected_indexes]
    return selected_sentences


####################### --------- MAIN ------- #######################


# define data path
data_path = "D:/GitHub/PatientReportedOutcome/data/pdf_txt/"

# get and store txt file
file = [data_path + f for f in [f for f in os.listdir(data_path) if f.endswith("txt")]][0]
with open(file, 'r', encoding='utf-8') as f:
    text = f.read()

# clean text
text = clean_text(text)
# get summarized text - n sentences
n = 25
selected_sentences = summarize(text, n)
[print(s) for s in selected_sentences]

