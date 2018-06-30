# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 10:44:00 2018

@author: Bruno
"""
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn import metrics
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction import DictVectorizer
import matplotlib.pyplot as plt
vec = DictVectorizer()
#data = pd.read_json('resultOscarsUserAna2.json')
'''Substituir por arquivo desejado, gerado por userAnalysisInstagram.py'''
data = pd.read_json('userInfFoodInstagram2.json') #com nivel popularidade
print(data)
UsersId = data["username"].values
TotalLikes = data["total_likes"].values
AverageLikes = data["average_likes"].values
CommentsCountTotal =  data["comments_count_total"].values
AverageRetweet = data["average_comments_count"].values
ImportantDataForInfluencer = data[["average_comments_count","average_likes"]].values
#Popular user make calculation
InfluenceLevel = data["influence_level"].values
InfluenceLevelWiCom = data[["influence_level","average_comments_count"]].values
InfluenceLevelWiLikes = data[["influence_level","average_likes"]].values
#FollowersIdUser = data[["idUser","followers_count"]].values
#vec.fit_transform(data).toarray()

#Clustering influencer level with rettweets average
clusInfCom = KMeans(n_clusters=3).fit(InfluenceLevelWiCom)
#Clustering influencer level with followers
clusInfLike = KMeans(n_clusters=3).fit(InfluenceLevelWiLikes)
reshapedInfluencers = InfluenceLevel.reshape(-3,1)
#clusInfluencers = KMeans(n_clusters=2).fit(reshapedInfluencers)
print("Clustering")
print(clusInfCom)
centers = clusInfCom.cluster_centers_;
print("Centerss:")
print(centers)
labels = clusInfCom.labels_;
print("Labels:")
print(labels)
#siho = metrics.silhouette_samples(InfluenceLevelWiCom,clusInfCom.labels_)

#print(siho<-0.5)

#print("Silhouette Coefficient: %0.3f"% metrics.silhouette_score(InfluenceLevelWiCom, clusInfCom.labels_))

def plot_results():
    unique_labels = set(clusInfCom.labels_)
    colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
    for k, col in zip(unique_labels, colors):
        if k == -1:
             
            col = 'k'

        class_member_mask = (clusInfCom.labels_ == k)

        xy = InfluenceLevelWiCom[class_member_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markeredgecolor='k', 
                 markersize=25)

    plt.show()
    return
def plot_results2():
    unique_labels = set(clusInfLike.labels_)
    colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
    for k, col in zip(unique_labels, colors):
        if k == -1:
             
            col = 'k'

        class_member_mask = (clusInfLike.labels_ == k)

        xy = InfluenceLevelWiLikes[class_member_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markeredgecolor='k', 
                 markersize=25)

    plt.show()
    return
plot_results()
plot_results2()

#print(UsersId)
#UsersId.astype(float)
#print(preprocessing.scale(UsersId))
#Predicting
print("MultinomialNB")
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import MultinomialNB
#clf = BernoulliNB()
clf = MultinomialNB()
clf.fit(ImportantDataForInfluencer, InfluenceLevel)
BernoulliNB(alpha=1.0, binarize=0.0, class_prior=None, fit_prior=True)
MultinomialNB(alpha=1.0, class_prior=None, fit_prior=True)
print("Predict popularity according to average likes and average retweets using MultinomialNB")
pred = clf.predict(ImportantDataForInfluencer)
print(pred)

#file = open("C:/Users/Bruno/Desktop/PUC/TCC 2/python-twitter-master/examples/influenciaPredictFoodInstagram.txt", "a+")
#for preds in pred:
#    file.write(str(preds) +"\n")
#file.close()

#for s in pred:
 #   print(s)
print("Predict Probabilidade")
print(clf.predict_proba(ImportantDataForInfluencer))
print("Popular pos...")
print(InfluenceLevel)
resultAcc = accuracy_score(InfluenceLevel, pred)
print("Accuracy")
print(resultAcc)
from sklearn.feature_extraction import DictVectorizer
vec = DictVectorizer()
#dataNum = vec.fit_transform(SomeData).toarray()
#print(dataNum)

#Nearest Neighbors of average retweets and likes
#print("NN")
#from sklearn.neighbors import NearestNeighbors
#import numpy as np
#X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
#nbrs = NearestNeighbors(n_neighbors=2, algorithm='auto').fit(InfluenceLevelWiCom)
#reshaped = ImportantDataForInfluencer.reshape(4760,-4760)
#reshaped = ImportantDataForInfluencer.reshape(-3,3)
#distances, indices = nbrs.kneighbors(InfluenceLevelWiCom)
#print(indices)
#print(distances)
#print(nbrs.kneighbors_graph(InfluenceLevelWiCom).toarray())