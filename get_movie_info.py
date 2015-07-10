"""
Used to grab meaning from the names of movie files.
We try to get the name, year, language of the movie.
This details can then be used as parameters to search.
"""
import re
import sys
import json
from os import walk
from cfg import video_extesions, languages, noise_words
path = '/home/kiran/nn'

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
    extract_details_from_string("Homely Meals (2014) Malayalam DVDRip x264 AAC 5.1-MBRHDRG.mkv")

if __name__ == '__main__':
    path = sys.argv[1]
    f = open(path + "/out.csv", 'w')
    for diname, dirs, files in walk(path):
        for fn in files:
            d = extract_details_from_string(fn)
            if d:
                s = "%s,%s,%s,%s\n" %(d['movie_name'], d['filename'], d['language'], d['year'])
                # print s
                f.write(s)
    f.close()