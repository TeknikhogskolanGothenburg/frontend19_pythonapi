def make_movie(items):
    keys = ["id", "budget", "original_language", "original_title", "overview", "popularity", "poster_path", "release_date", "revenue", "runtime"]
    movie = {}
    for i, key in enumerate(keys):
        movie[key] = items[i]
    return movie