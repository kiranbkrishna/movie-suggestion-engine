video_extesions = [ '.flv', '.dat', '.vob', '.mkv', '.mpg', '.dat', '.avi', '.mp4']

noise_words = 
keywords.update(filter( lambda(x): not p.match(x), [j for j in re.split('\s+|\.', fn) for fn in files]))