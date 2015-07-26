import sys
from os import walk

def extract_extensions(path):
    extensions = set()
    for dirpath, dirs, files in walk(path):
        extensions.update([fn[fn.strip().rfind("."):] for fn in files])
    print extensions

if __name__ == '__main__':
    if len(sys.argv) == 2:
        extract_extensions(sys.argv[1])
    else:
        print "USAGE: python extesion_collecror.py [abs path to the movie folder]"
        