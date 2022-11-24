from flask import Flask, request, render_template

from utils import get_movie_info, get_poster_links, get_stars
from recommender import get_NMF_recommendations, movies, get_titles_from_query, get_id_from_title, get_rec_stars
#from recommender import get_recommandations, movies, get_titles_from_query, get_id_from_title, get_rec_stars
from scipy.sparse import csr_matrix
import os

#if changing to NN model remove # from above and move to line above

port = int(os.environ.get('PORT', 5000))

app = Flask(__name__)

@app.route("/")
def landing_page():
    return render_template(
        "index.html"
        )

@app.route("/recommender/")
def make_recommendations():
    #takes input query from html, creates query to input into csr 
    #matrix and fit to nmf model to output recommendations. 
    #to switch to nearest neighbor model remove # from rec and replace in line below 
    titles = request.args.getlist("input")
    ratings = []
    for i in range(5):
        string = "rating" + str(i+1)
        ratings.append(request.args.getlist(string)[0])
    poster_links = get_poster_links(titles)
    titles_from_query = get_titles_from_query(titles)
    title_ids = get_id_from_title(titles_from_query)
    titles_and_ratings_dict = dict(zip(title_ids, [int(r) for r in ratings]))
    print(titles_and_ratings_dict)
    #recs = get_recommandations(titles_and_ratings_dict)
    recs = get_NMF_recommendations(titles_and_ratings_dict)
    recs_ids = get_id_from_title(recs)
    rec_stars = get_rec_stars(recs_ids)
    recomm_links = get_poster_links(recs)
    stars = get_stars(ratings)
    movie_infos = get_movie_info(recs)
    return render_template(
        'recommendation.html',
        recs=recs,
        poster_links=poster_links,
        recomm_links=recomm_links,
        ratings=ratings,
        stars=stars,
        titles=titles_from_query,
        movie_infos = movie_infos,
        rec_stars = rec_stars
        )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=True)

#need to add open web browser here