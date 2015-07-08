import os
ia = imdb.IMDb() # by default access the web.
rootdir = 'E:\\'
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        file_name, extension = os.path.splitext(file)
        if extension in ['.mp4', '.mkv', '.avi', '.mov']:
            digits = [int(s) for s in file.split() if s.isdigit()]
            for digit in digits:
                year = ''
                if len(str(digit))== 4:
                    year = str(digit)
            import re
            rx = re.compile('\W+')
            res = rx.sub(' ', file_name).strip()
            print res
        # Search for a movie (get a list of Movie objects).
            s_result = ia.search_movie(res+' '+year)
            for item in s_result:
                print item['long imdb canonical title'], item.movieIDitem
                print 'runtime',item['runtime']
                print 'rating',item['rating']
                print 'director',item['director']
                print '---------------------------'