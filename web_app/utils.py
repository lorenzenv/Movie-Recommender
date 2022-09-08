import tmdbsimple as tmdb

tmdb.API_KEY = '0bf69a28ee0108f01839a18c66bf4d73'


def get_movie_info(movie_list):
    movie_infos = []
    for movie in movie_list:
        search = tmdb.Search()
        response = search.movie(query=movie)
        if search.results:
            movie_id = search.results[0]['id']
            movie = tmdb.Movies(movie_id)
            movie_info = movie.info()
            info = movie_info['overview']
            info = info[:120]
            info += "..."
            movie_infos.append(info)
        else:
            movie_infos.append("no information available")
    return movie_infos


def get_poster_links(movie_list):
    poster_list = []
    for movie in movie_list:
        movie = movie[:10]
        search2 = tmdb.Search()
        response = search2.movie(query=movie)
        if search2.results:
            movie_id = search2.results[0]['id']
            movie = tmdb.Movies(movie_id)
            response = movie.info()
            poster = movie.images()
            poster = poster.get('posters')
            if poster:
                poster = poster[0]
                file_path = poster['file_path']
                file_path = "https://image.tmdb.org/t/p/w500" + file_path
                poster_list.append(file_path)          
        else:
            poster_list.append("https://i.ibb.co/HG65553/hl-PLsovz-Je6j-GKp-QSp31f2-Mx-AMM.png")
    return poster_list

def get_stars(ratings_list):
    star_results = []
    print (ratings_list)
    for rating in ratings_list:
        print ("rating: ", rating)
        positive = int(rating) * '<span class="fa fa-star checked"></span>'
        negative = (5-int(rating)) * '<span class="fa fa-star"></span>'
        result = positive + negative
        star_results.append(result)
    return star_results

