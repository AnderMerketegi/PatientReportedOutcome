"""
    In this file I will compare different similarity algorithms and will try to summarize
    the text in a scientific article getting the most relevant n sentences.

    Similarity: Jaccard similarity
    Ranking: Text Rank algorithm
"""

# import packages
import glob
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


# function to summarize text t and get n most important sentences
def summarize_text(t, n):
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
    summarized_text = " ".join([t[i] for i in selected_indexes])
    return summarized_text


# function to summarize (n sentences) all txt documents from path and store them in output path
def summarize(path, n, output_path):
    # check that paths exist
    if not os.path.exists(path):
        print(f"Unable to find path: {path}.")
        return
    if not os.path.exists(output_path):
        print(f"Unable to find output path.")
        os.mkdir(output_path)
        print(f"Output path created.\n")
    # count summarized documents
    n_sum = 0
    # get txt files from path
    files = glob.glob(path + "*.txt")
    n_total = len(files)
    for file in files:
        # read full document
        with open(file, 'r', encoding='utf-8') as f:
            t = f.read()
        # clean text
        t = clean_text(t)
        # get summarized text
        summarized_t = summarize_text(t, n)
        # print(output_path + file.split("\\")[-1][:-4] + "_sum.txt")
        with open(output_path + file.split("\\")[-1][:-4] + "_sum.txt", "w", encoding='utf-8') as f:
            f.write(summarized_t)
            n_sum += 1

    print(f"{n_total}/{n_sum} text files summarized.")


#################### ---------- MAIN ---------- ####################


# define data path
data_path = "D:/GitHub/PatientReportedOutcome/data_sample/pdf_txt/txt/en/"
# summarize all txt files located in data_path - 25 sentences
n = 25
summarize(data_path, n, data_path + "summaries/")