import pandas as pd
import pickle
from scipy.sparse import csr_matrix
import numpy as np
from thefuzz import fuzz, process
import sklearn


movies = pd.read_csv("movies.csv")
ratings = pd.read_csv("ratings.csv")

titles = movies['title'].str.partition(' (', True)
movies['title'] = titles[0]

"""to be used if using NN model"""
with open('static/nn_new_recommender.pkl', 'rb') as file:
    model = pickle.load(file)

with open('static/nmf_recommender.pkl', 'rb') as file:
    NMF_model = pickle.load(file)

with open('static/r_matrix.pkl', 'rb') as file:
    R = pickle.load(file)

def get_titles_from_query(query):
    result = []
    for title in query:
        search_query = title
        match = process.extractBests(
        search_query, movies['title'], scorer=fuzz.token_set_ratio
        )
        result.append(match[0][0])
    print (result)
    return result

def get_id_from_title(query):
    result = []
    for title in query:
        movie = movies[movies['title'].str.fullmatch(str(title))]['movieId'].values[0]
        result.append(movie)
    return result


def get_recommandations(query):

    user_vec = np.repeat(0, 168253)
    user_vec[list(query.keys())] = list(query.values())

    distances, userIds = model.kneighbors([user_vec], n_neighbors=10, return_distance=True)

    distances = distances[0]
    userIds = userIds[0]

    neighborhood = ratings.set_index('userId').loc[userIds]

    factors = np.array(distances)[neighborhood.index.factorize()[0]]
    neighborhood['rating'] *= 1-factors
    
    scores = neighborhood.groupby('movieId')['rating'].sum()
    
    allready_seen = scores.index.isin(query.keys())
    scores.loc[allready_seen] = 0
    scores = scores.sort_values(ascending=False)

    recommendations = scores.head(5).index

    result = movies.set_index('movieId').loc[recommendations]

    result_titles = result['title'].values

    print ("result_titles: ", result_titles)

    return result_titles



def get_NMF_recommendations(query):
    #query = {1: 5, 2: 4, 79091: 5, 56367: 1, 180987: 5}
    print(query)
    data = list(query.values())  # the ratings of the new user
    row_ind = [0]*len(data)      # we use just a single row 0 for this user 
    col_ind = list(query.keys()) # the columns (=movieId) of the ratings

    # new user vector: needs to have the same format as the training data
    user_vec = csr_matrix((data, (row_ind, col_ind)), shape=(1, R.shape[1]))

    # user_vec -> encoding -> p_user_vec -> decoding -> user_vec_hat
    scores = NMF_model.inverse_transform(NMF_model.transform(user_vec))

    # convert to a pandas series
    scores = pd.Series(scores[0])

    # give a zero score to movies the user has allready seen
    scores[query.keys()] = 0

    # sort the scores from high to low 
    scores = scores.sort_values(ascending=False)

    # get the movieIds of the top 5 entries
    recommendations = scores.head(5).index

    result = movies.set_index('movieId').loc[recommendations]

    result_titles = result['title'].values

    print ("result_titles: ", result_titles)

    return result_titles



def get_rec_stars(movie_list):
    star_results = []
    for movieId in movie_list:
        rating = ratings.groupby('movieId')['rating'].mean()[movieId]
        rating_round = round(rating)
        positive = int(rating_round) * '<span class="fa fa-star checked"></span>'
        negative = (5-int(rating_round)) * '<span class="fa fa-star"></span>'
        result = positive + negative
        star_results.append(result)
        print ("rating: ", rating)
    return star_results
