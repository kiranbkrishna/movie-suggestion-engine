"""
Used to grab meaning from the names of movie files.
We try to get the name, year, language of the movie.
This details can then be used as parameters to search.
"""
import re
from os import walk
from cfg import video_extesions
path = '/home/kiran/nn'

# for dirpath, dirs, files in walk(path):

def extract_details_from_string(filename):
    assert filename
    current_extension = get_filename_extension(filename)
    if current_extension in video_extesions:
        possible_years = set(get_possible_years)
    else:
        print 'Invalid file type. Abort details extraction.'

def get_filename_extension(filename):
    assert type(filename) == type("")
    return filename[filename.strip().rfind('.'):]

def get_possible_years(filename):
    "Gets all possible values for years"
    assert type(filename) == type("")
    p = re.compile('\d{4}')
    return p.findall(filename)

if __name__ == '__main__':
    extract_details_from_string("Homely Meals (2014) Malayalam DVDRip x264 AAC 5.1-MBRHDRG.mkv")