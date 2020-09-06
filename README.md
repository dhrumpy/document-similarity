# document-similarity
The project involves two-phase, namely, first retrieving the raw data from the PubMed database and second, language processing to determine similarity among the documents.


A python code 'scrapper.py' gathers all the required data, basically scrapping the website and parsing using the 'request' and 'beautiful soup' module. 
One needs to employ a 'sleep' method so that the site is not flooded with numerous requests in a short amount of time. 
We store the 'PMIDs' in a list and use this as an endpoint to access the document abstracts. 
This program's output is 'corpus.txt,' which is the raw form of the data that needs further processing. 
The typical running time is 450 seconds; run only when you want new data.


Following that, we run the 'main.py' for document analysis. 
First, we compute frequently occurring words in the entire corpus and remove them from each of the raw abstracts (corpus). 
Further, we refine the document by removing the stop words, lemmatizing them to their root forms. 
Each (refined) abstract is then represented as a vector using 'CountVectorizer()'. The components of the vectors represent the frequency of occurrence of a given word. 
Then similarity among every vector pair is computed and stored in a matrix 'cosine_similarity_mat.' 
Further, we group all the documents into six clusters using the similarity-matrix. 
Lastly, we print three unique words within each cluster.
