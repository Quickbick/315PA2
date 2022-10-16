import pandas as pd

movies = pd.read_csv('./movie-lens-data/movies.csv')
links = pd.read_csv('./movie-lens-data/links.csv')
ratings = pd.read_csv('./movie-lens-data/ratings.csv')
tags = pd.read_csv('./movie-lens-data/tags.csv')

#create profile of movies and various recieved ratings  
mainDataFrame = pd.merge(ratings, movies, on="movieId")
movieMatrix = mainDataFrame.pivot_table(index='userId', columns='title', values='rating')
movieSeacher = mainDataFrame.pivot_table(index='title', values='movieId')

#computes similarity for move-movie pairs using centered cosine similarity method
corrMatrix = movieMatrix.corr(method='pearson', min_periods= 50)

#iterates users
for i in range(1,2): #len(movieMatrix) for final
    #gets user's ratings
    userRatings = movieMatrix.iloc[i].dropna()
    reccomend = pd.Series()

    #iterates movies
    for j in range(0, len(userRatings)):
        #adds similar movies to reccomend table
        similar = corrMatrix[userRatings.index[j]].dropna()
        similar = similar.map(lambda x: x * userRatings[j])
        reccomend = reccomend.append(similar)
    
    #sorts movies in order of best reccomendation
    reccomend.sort_values(inplace= True, ascending= False)

    #prints top 5 reccomended to file
    
    x = pd.DataFrame(reccomend)
    reccomendFilter = x[~x.index.isin(userRatings.index)]
    holdItems = reccomendFilter.head(5)
    print("User Id " + str(i))
    for j in range (0, 5):
        print(holdItems.iloc[j].name)
    #print(reccomendFilter.head(5))