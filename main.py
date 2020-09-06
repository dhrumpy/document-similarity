import re
import time

import spacy
nlp = spacy.load('en_core_web_lg')

from sklearn.feature_extraction.text import CountVectorizer
from scipy import spatial
from sklearn.cluster import SpectralClustering

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.filterwarnings('ignore')

nAbstract = 100

# ### Solution 1
print('Solution 1: ')
with open('corpus.txt', 'r') as file_object:
    corpus = file_object.readlines()
file_object.close()

# printing the first 10 abstracts
print('Printing first 10 abstracts')
for abstract in corpus[0:10]:
    print(abstract)


# ### Solution 2
print('\n\nSolution 2: ')
# # reading the corpus from the text file
# with open('corpus.txt', 'r') as file_object:
#     corpus = file_object.readlines()
# file_object.close()

print('Computing the frequency of words in the entire corpus')
freq = {}
for paragraph in corpus:
    for token in paragraph.split():
        if token in freq.keys():
            freq[token]+=1
        else:
            freq[token]=1            
print('Done')
            
print('Identifying top 10 frequent words in the entire corpus')
top10_word_freq = sorted(freq.values(), reverse=True)[0:10]
frequent_words = []
for key, value in freq.items():
    if value in top10_word_freq:
        frequent_words.append(key)        
print('Done')
print('Frequent word list/ Removed words: {}\n'.format(frequent_words))


print('Removing the top 10 frequent words from all the abstracts and witing the cleaned data into a text file')
file = open('cleaned_corpus.txt','w')
file.close()

with open('cleaned_corpus.txt', 'a+') as file_object:
    for paragraph in corpus: 
        paragraph = paragraph.split()
        paragraph = [token for token in paragraph if token not in frequent_words]
        paragraph = ' '.join(paragraph)
        file_object.write(paragraph)
        file_object.write('\n')
print('Done')

# ### Solution 3
print('\n\nSolution 3: ')

with open('cleaned_corpus.txt') as file_object:
    cleaned_corpus = file_object.readlines()
file_object.close()


print('Removing the stop words')
cleaned_corpus_without_stopWords = []
for paragraph in cleaned_corpus:
    paragraph = paragraph.split()
    paragraph = [token for token in paragraph if token not in nlp.Defaults.stop_words]
    paragraph = ' '.join(paragraph)
    cleaned_corpus_without_stopWords.append(paragraph)    
print('Done')
    
print('Lemmatizing; getting the root words of all tokens/ words')
lemmatized_data = []
for paragraph in cleaned_corpus_without_stopWords:
    lemmas = []
    doc = nlp(paragraph)
    for token in doc:
        lemmas.append(token.lemma_)
    lemmas = ' '.join(lemmas)
    lemmatized_data.append(lemmas)
print('Done') 
   
    
print('Removing puncuations')
punc = '''!()-[]{};:'"\, <>./?@#$%^&*_~'s'''
refined = []
for paragraph in lemmatized_data:
    tokens = paragraph.split()
    tokens = [token for token in tokens if token not in punc]
    paragraph = ' '.join(tokens)
    refined.append(paragraph)
print('Done')


count_vect = CountVectorizer()
doc_vectors = count_vect.fit_transform(refined)
print('Printing the first two rows of the vector:')
print('Vector 1:')
print(*doc_vectors.toarray()[0, :])
print('Vector 2:')
print(*doc_vectors.toarray()[1, :])

# plt.figure(figsize=(10, 8))
# sns.heatmap(data=doc_vectors.toarray()[0:2, :]);

cosine_similarity = lambda x, y: 1 - spatial.distance.cosine(x, y)

cosine_similarity_mat = np.zeros((nAbstract, nAbstract), dtype=float)
for i in range(nAbstract):
    for j in range(nAbstract):
        cosine_similarity_mat[i, j] = cosine_similarity(doc_vectors.toarray()[i,:], doc_vectors.toarray()[j,:])
        
# plt.figure(figsize=(10, 8))
# sns.heatmap(data=cosine_similarity_mat)


# ### Solution 4

print('Clustering')

doc_labels = list(SpectralClustering(n_clusters=6).fit_predict(cosine_similarity_mat))
print(doc_labels)


# ### Solution 5

nCluster = 6
docs_cluster_wise = []
print('Folloing are the document/ abstract clusters, the document numbers are grouped into corresponding clusters:')
for cluster_id in range(nCluster):
    docs_cluster_wise.append([i for i in range(nAbstract) if doc_labels[i]==cluster_id])
    print('cluster {}: {}'.format(cluster_id, docs_cluster_wise[cluster_id]))

    
# 3 most unique words within a cluster:
unique_words_within_clusters = []
print('\n\nThree unique words within each clusters:')
for idx, docs in enumerate(docs_cluster_wise):
    freq = {}
    for num in docs:
        for token in refined[num].split():
            if token in freq.keys():
                freq[token]+=1
            else:
                freq[token]=1
    top3_word_freq_in_a_cluster = sorted(freq.values(), reverse=True)[0:3]
    frequent_words = {}
    for key, value in freq.items():
        if value in top3_word_freq_in_a_cluster:
            frequent_words[key] = value
            
    unique_words_within_clusters.append(frequent_words)
    print('cluster {}: {}'.format(idx, unique_words_within_clusters[idx]))

