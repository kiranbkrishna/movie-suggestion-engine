"""
Used to grab meaning from the names of movie files.
We try to get the name, year, language of the movie.
This details can then be used as parameters to search.
"""
import re
import sys
from os import walk
from optparse import OptionParser
from utils.imdb_client import imdb_details
from conf.cfg import video_extesions, languages, noise_words

# for dirpath, dirs, files in walk(path):

def extract_details_from_string(filename):
    assert filename
    current_extension = get_filename_extension(filename)
    if current_extension in video_extesions:
        possible_years = set(get_possible_years(filename))
        print possible_years
        possible_languages = set(get_possible_languages(filename))
        print possible_languages
        possible_movie_name = get_possible_names(filename, 
                                possible_languages,
                                possible_years,
                                current_extension)
        print possible_movie_name
        return {'filename': filename,
            'movie_name': possible_movie_name,
            'year': str(possible_years),
            'language': str(possible_languages)}

    else:
        print 'Invalid file type. Abort details extraction.'
        possible_movie_name = 'NA'

def get_filename_extension(filename):
    assert type(filename) == type("")
    return filename[filename.strip().rfind('.'):]

def get_possible_languages(filename):
    "Get all possible language values"
    assert type(filename) == type("")
    ret = set()
    for lang in languages:
        p = re.compile(lang, re.IGNORECASE)
        values = p.findall(filename) or []
        if values:
            values = map(lambda(x):x.lower(), values)
        ret.update(values)
    return ret

def get_possible_names(filename, possible_languages, possible_years, current_extension):
    "Get the possible movie name"
    assert isinstance(filename, str)
    movie_name = filename
    #1 remove filename extension
    p = re.compile(current_extension.strip('.'))
    movie_name = p.sub('', movie_name)

    #2 remove any websites in the name
    p = re.compile('[w]{3}.[\w\d]+.[\d\w]{3}')
    movie_name = p.sub('', movie_name)

    #3 remove year
    for year in possible_years:
        p = re.compile(year, re.IGNORECASE)
        movie_name = p.sub('', movie_name)
    
    #4 remove languages
    for lang in possible_languages:
        p = re.compile(lang, re.IGNORECASE)
        movie_name = p.sub('', movie_name)
    
    #5 remove noise words
    name_list = re.split('\s+|\.|\-|\_', movie_name)
    name = ""
    for n in name_list:
        to_add = True
        for w in noise_words:
            p = re.compile(w, re.IGNORECASE)
            if p.match(n):
                to_add = False
                break
        if to_add:
            name += (n + " ")
    
    #6 chop off the substring from special character occuring index.
    p = re.compile('[^\{\(\[@#$%^&*()_!+~]+')
    m = p.match(name)
    if m:
        name = m.group()
    else:
        print 'returning movie name without removal'
    return name

def get_possible_years(filename):
    "Gets all possible values for years"
    assert type(filename) == type("")
    p = re.compile('\d{4}')
    return p.findall(filename)


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-p', '--path', dest='path', help='Path to movies')
    parser.add_option('-m', '--movie', dest='movie', help='name of the movie')
    parser.add_option('-o', '--outpath', dest='outpath', help='directory where output file should be generated')
    (options, args) = parser.parse_args()
    movie = options.movie
    path = options.path
    out = options.outpath
    
    if path:
        if not path.endswith(sep):
            f = open(path + "/out.csv", 'w')
        else:
            f = open(path + "out.csv", 'w')

        s = "movie_name,title,ratings,director,runtime,genres,plot \n"
        f.write(s)
        for diname, dirs, files in walk(path):
            for fn in files:
                d = extract_details_from_string(fn)
                if d:
                    try:
                        details = imdb_details(d['movie_name'])
                        if details:
                            s = "%s,%s,%s,%s,%s,%s,%s\n" %(d['movie_name'], details['title'], details['ratings'], details['director'],details['runtimes'],details['genres'],details['plot'])
                        else:
                            s = "unable to find result for " + d['movie_name'] + "\n"
                        print s
                        f.write(s)
                    except UnicodeEncodeError:
                        print "codec can't encode character"
        f.close()
    elif movie:
        d = extract_details_from_string(movie)
        print d
    else:
        parser.print_help()
