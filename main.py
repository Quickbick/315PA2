from turtle import title
import pandas as pd

movies = pd.read_csv('./movie-lens-data/movies.csv')
links = pd.read_csv('./movie-lens-data/links.csv')
ratings = pd.read_csv('./movie-lens-data/ratings.csv')
tags = pd.read_csv('./movie-lens-data/tags.csv')

#create profile of movies and various recieved ratings  
mainDataFrame = pd.merge(ratings, movies, on="movieId")
movieMatrix = mainDataFrame.pivot_table(index='userId', columns='title', values='rating')

#computes similarity for move-movie pairs using centered cosine similarity method
corrMatrix = movieMatrix.corr(method='pearson', min_periods= 50)

outfile = open("./output.txt", "w")

#iterates users
for i in range(1,len(movieMatrix)):
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
    outfile.write(str(i))
    outfile.write(' ')
    holdmax = min(5, len(holdItems))
    for j in range (0, holdmax):
        for k in range (0, len(movies)):
            if(movies.iloc[k, 1] == holdItems.iloc[j].name):
                outfile.write(str(movies.iloc[k, 0]))
                outfile.write(' ')
    outfile.write('\n')
outfile.close()