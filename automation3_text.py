import matplotlib.pyplot as plt
import json
import os
import nltk 
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity, cosine_distances, pairwise_distances

def preprocess(text):
    tokens = word_tokenize(text)

    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word.lower() not in stop_words]

    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    processed_text = ' '.join(tokens)
    return processed_text

def similarities(text1,text2):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text1, text2])

    cosine_sim = cosine_similarity(tfidf_matrix)[0, 1]

    intersect = len(set(text1.split()) & set(text2.split()))
    union = len(set(text1.split()) | set(text2.split()))
    jaccard_sim = intersect / union

    intersect_dice = 2 * len(set(text1.split()) & set(text2.split()))
    dice_sim = intersect_dice / (len(set(text1.split())) + len(set(text2.split())))

    cosine_dist = cosine_distances(tfidf_matrix)[0, 1]

    dice_dist = 1- dice_sim
    jaccard_dist = 1 - jaccard_sim

    return {
        "Cosine Similarity": cosine_sim,
        "Jaccard Similarity": jaccard_sim,
        "Sorensen Similarity": dice_sim,
        "Cosine Distance": cosine_dist,
        "Jaccard Distance": jaccard_dist,
        "Sorensen Distance" : dice_dist
    }
    
text1 = input("Enter Texts for similarity analysis")
text2 = input("Enter Texts for similarity analysis")
processed_text1 = preprocess(text1)
processed_text2 = preprocess(text2)

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform([processed_text1, processed_text2])

svd = TruncatedSVD(n_components=2)
vectors_2d = svd.fit_transform(tfidf_matrix)

plt.scatter(vectors_2d[:, 0], vectors_2d[:, 1], c='blue', label='Text 1')
plt.scatter(vectors_2d[:, 0], vectors_2d[:, 1], c='yellow', label='Text 2')

plt.text(vectors_2d[0, 0], vectors_2d[0, 1], 'Text 1', fontsize=12, ha='right')
plt.text(vectors_2d[1, 0], vectors_2d[1, 1], 'Text 2', fontsize=12, ha='right')

plt.xlabel('Dimension 1')
plt.ylabel('Dimension 2')
plt.title('TF-IDF Vector Representation')

plt.legend()

metrics = similarities(processed_text1,processed_text2)
for x,y in metrics.items():
    print(f"{x}: {y}")

plt.show()

