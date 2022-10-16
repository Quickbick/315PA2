import pandas as pd

movies = pd.read_csv('./movie-lens-data/movies.csv')
links = pd.read_csv('./movie-lens-data/links.csv')
ratings = pd.read_csv('./movie-lens-data/ratings.csv')
tags = pd.read_csv('./movie-lens-data/tags.csv')

mainDataFrame = pd.merge(ratings, movies, on="movieId")
movieMatrix = mainDataFrame.pivot_table(index='userId', columns='title', values='rating')
corrMatrix = movieMatrix.corr(method='pearson', min_periods= 50)

for i in range(1,2):
    userRatings = movieMatrix.iloc[i].dropna()
    print("Ratings for user " + str(i))
    print(userRatings)
    reccomend = pd.Series()
    for j in range(0, len(userRatings)):
        print("***** Adding similar movies to " + userRatings.index[j] + "*****")
        similar = corrMatrix[userRatings.index[j]].dropna()
        similar = similar.map(lambda x: x * userRatings[j])
        reccomend = reccomend.append(similar)
    print("Sorting Reccommendations")
    reccomend.sort_values(inplace= True, ascending= False)
    print("User Id " + str(i))
    print(reccomend.head(10))
    x = pd.DataFrame(reccomend)
    reccomendFilter = x[~x.index.isin(userRatings.index)]
    reccomendFilter.head(5)