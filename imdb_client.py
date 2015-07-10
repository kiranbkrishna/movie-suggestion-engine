"""
Module used to get ratings, director, plot and genere of a movie
using imdbpy
"""

import imdb
i = imdb.IMDb()

def search_movie(movie_name, movie_year=None):
    movies = i.search_movie(movie_name)
    selected_movie = None
    if movies:
        if movie_year:
            for movie in movies:
                if movie_year == movie.data.get('year'):
                    selected_movie = movie
                    break
        else:
            selected_movie = movies[0]
    return selected_movie

def get_movie_details(movie):
    if movie:
        movie = i.get_movie(movie.movieID)
        d = None
        if movie:
            data = movie.__dict__['data']
            director_name = ''
            if data.get('director'):
                director_name=data.get('director')[0].get('name')
            d = {'title': data.get('title'),
                 'ratings': data.get('rating'), 
                 'plot': data.get('plot'),
                  'director':director_name}
        return d

def imdb_details(movie_name, movie_year=None):
    movie = search_movie(movie_name, movie_year)
    return get_movie_details(movie)