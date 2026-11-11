import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import pickle

file_name = "data/alice.txt"
pickle_name = "data/alice_tfidf.pkl"

# create the rag data
def create_rag_data():
    # load the data
    with open(file_name, "r") as f:
        document_text = f.read()

    # split the data on double newlines
    document_text = document_text.split("\n\n")
    
    # Initialize TF-IDF Vectorizer
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(document_text)
    
    return document_text, vectorizer, tfidf_matrix

def get_cached_rag_data():
    if os.path.exists(pickle_name):
        with open(pickle_name, "rb") as f:
            document_text, vectorizer, tfidf_matrix = pickle.load(f)
    else:
        document_text, vectorizer, tfidf_matrix = create_rag_data()
        with open(pickle_name, "wb") as f:
            pickle.dump((document_text, vectorizer, tfidf_matrix), f)

    return document_text, vectorizer, tfidf_matrix


document_text, vectorizer, tfidf_matrix = get_cached_rag_data()

def search_document(question):
    # convert the question to a TF-IDF vector
    question_tfidf = vectorizer.transform([question])

    # calculate the cosine similarity
    similarities = cosine_similarity(question_tfidf, tfidf_matrix)[0]

    # get the top 3 most similar documents
    top_indices = np.argsort(similarities)[-3:][::-1]

    indices = list(top_indices)
    for x in range(1, 4):
        indices.extend([i-x for i in top_indices if i-x >= 0])
        indices.extend([i+x for i in top_indices if i+x < len(document_text)])

    # sort and unique the indices
    top_indices = sorted(list(set(indices)))

    prior_indice = -2
    top_passages = []
    for i in top_indices:
        if prior_indice != i-1:
            top_passages.append(f"Passage {i}:\n{document_text[i]}")
        else:
            top_passages[-1] += "\n\n" + document_text[i]
        prior_indice = i

    return top_passages
