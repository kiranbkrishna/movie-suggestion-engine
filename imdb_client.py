"""
Module used to get ratings, director, plot and genere of a movie
using imdbpy
"""
import difflib

import imdb
i = imdb.IMDb()

def search_movie(movie_name, movie_year=None):
    movie_name.strip()
    movies = i.search_movie(movie_name)
    selected_movie = None
    if movies:
        # if movie_year:
        #     # for movie in movies:
        #     #     if movie_year == movie.data.get('year'):
        #     #         selected_movie = movie
        #     #         break
        #     if movie_year:
        #         movie_name = movie_name.trim() + ''+movie_year
        #     selected_movie = find_apt_match(movie_name, movies )
        # else:
        #     selected_movie = movies[0]
        if movie_year:
            movie_name = movie_name+ ''+movie_year
        selected_movie = find_apt_match(movie_name, movies )

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

def find_apt_match(movie_name, list_movies):
    movie_name.strip(' ')
    final_result = get_close_matches(movie_name, list_movies, 1)
    if final_result:
        return final_result[0]
    return None

def get_close_matches(word, movies, n=3, cutoff=0.6):
    if not n >  0:
        raise ValueError("n must be > 0: %r" % (n,))
    if not 0.0 <= cutoff <= 1.0:
        raise ValueError("cutoff must be in [0.0, 1.0]: %r" % (cutoff,))
    result = []
    s = difflib.SequenceMatcher()
    s.set_seq2(word)
    for x in movies:
        s.set_seq1(x.data.get('title')+' '+str(x.data.get('year')))
        # s.set_seq2(str(x.data.get('year')))
        if s.real_quick_ratio() >= cutoff and \
           s.quick_ratio() >= cutoff and \
           s.ratio() >= cutoff:
            result.append((s.ratio(), x))

    # Move the best scorers to head of list
    import heapq

    result = heapq.nlargest(n, result)
    # Strip scores for the best n matches
    return [x for score, x in result]




def imdb_details(movie_name, movie_year=None):
    movie = search_movie(movie_name, movie_year)
    return get_movie_details(movie)

if __name__ == '__main__':
    movies = i.search_movie('wolves')
    print get_close_matches('wolves 2014', movies,1)
