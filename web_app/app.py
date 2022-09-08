from flask import Flask, request, render_template

from utils import get_movie_info, get_poster_links, get_stars
from recommender import get_recommandations, movies, get_titles_from_query, get_id_from_title, get_rec_stars
from scipy.sparse import csr_matrix
import os

port = int(os.environ.get('PORT', 5000))

app = Flask(__name__)

@app.route("/")
def landing_page():
    return render_template(
        "index.html"
        )

@app.route("/recommender/")
def make_recommendations():
    titles = request.args.getlist("input")
    ratings = []
    for i in range(5):
        string = "rating" + str(i+1)
        ratings.append(request.args.getlist(string)[0])
    poster_links = get_poster_links(titles)
    titels_from_query = get_titles_from_query(titles)
    title_ids = get_id_from_title(titels_from_query)
    print(title_ids)
    titles_and_ratings_dict = dict(zip(title_ids, ratings))
    recs = get_recommandations(titles_and_ratings_dict)
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
        titles=titels_from_query,
        movie_infos = movie_infos,
        rec_stars = rec_stars
        )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=True)
