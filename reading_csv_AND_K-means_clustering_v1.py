#!/usr/bin/python
# -*- coding: utf-8 -*-
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_20newsgroups

import csv

with open('file.tsv') as tsvfile: #opens a file named tab_delim.tsv and name it tsvfile for internal usage

    reader=csv.DictReader(tsvfile, delimiter='\t') #csv.reader is a function defined in the csv module

    for row in reader:
        #rows iteration - we navigate through all of the rows of the csv file
        tweets.append(row['Tweet'])

# *** Bag-of-Words implementation ***

vectorizer = TfidfVectorizer(stop_words='english') # Convert a collection of raw documents to a matrix of TF-IDF features.
                                                   # Equivalent to CountVectorizer followed by TfidfTransformer.
X = vectorizer.fit_transform(reader(tsvfile['Tweet']).todense())

# *** End of Bag-of-Words implementation ***



# *** K-means implementation ***

true_k=3
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=300, n_init=10)
# n_clusters := (int, optional, default: 8) The number of clusters to form as well as the number of centroids to generate.
# init := {‘k-means++’, ‘random’ or an ndarray} Method for initialization, defines initial cluster centers. ‘k-means++’ : selects initial cluster centers for k-mean clustering in a smart way to speed up convergence
# max_iter := (int, default: 300) Maximum number of iterations of the k-means algorithm for a single run.
# n_init := (int, default: 10) Number of time the k-means algorithm will be run with different centroid seeds. The final results will be the best output of n_init consecutive runs in terms of inertia(= αδράνεια).

model.fit(X) # Compute k-means clustering.

# *** End of K-means implementation ***




print("Top terms per cluster:")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
for i in range(true_k):
    print ("Cluster %d:" % i)
    for ind in order_centroids[i, :6]:
        print (' %s' % terms[ind])
    print ()

pca = PCA(n_components = 2).fit(X)
data2D = pca.transform(X)
# From StackOverflow : "When you use Bag of Words, each of your sentences gets represented in a high dimensional space
# of length equal to the vocabulary. If you want to represent this in 2D you need to reduce the dimension,
# for example using PCA with two components.

plt.scatter(data2D[:,0], data2D[:,1], c = model.labels_)
# scatter method of matplotlib.pyplot makes a scatter plot of x vs y lists
# the term ':' in data2D[:,0] is used to include every live of data2D list

centers2D = pca.transform(model.cluster_centers_)

plt.scatter(centers2D[:,0], centers2D[:,1],
            marker='x', s=200, linewidths=3, c='r')
plt.show()