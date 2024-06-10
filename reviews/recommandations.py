# # recommendations.py
# import pandas as pd
# import numpy as np
# from scipy.sparse import csr_matrix
# from sklearn.neighbors import NearestNeighbors
# from moviereview.settings import BASE_DIR

# # Load the movie dataset
# print(BASE_DIR)
# file_path = str(BASE_DIR) +'\\reviews\\tmdb_movies3.csv'
# movies_df = pd.read_csv(file_path)

# # Add a random user ID to simulate user ratings (for demonstration purposes)
# movies_df['userid'] = np.random.randint(1, 6, movies_df.shape[0])

# # Keep relevant columns
# movies_df = movies_df[['id', 'userid', 'vote_count', 'runtime', 'title']]

# def create_matrix(df):
#     N = len(df['userid'].unique())
#     M = len(df['id'].unique())

#     user_mapper = {userid: idx for idx, userid in enumerate(np.unique(df["userid"]))}
#     movie_mapper = {movieid: idx for idx, movieid in enumerate(np.unique(df["id"]))}

#     user_inv_mapper = {idx: userid for userid, idx in user_mapper.items()}
#     movie_inv_mapper = {idx: movieid for movieid, idx in movie_mapper.items()}

#     user_index = [user_mapper[userid] for userid in df['userid']]
#     movie_index = [movie_mapper[movieid] for movieid in df['id']]

#     X = csr_matrix((df["vote_count"], (movie_index, user_index)), shape=(M, N))

#     return X, user_mapper, movie_mapper, user_inv_mapper, movie_inv_mapper

# X, user_mapper, movie_mapper, user_inv_mapper, movie_inv_mapper = create_matrix(movies_df)

# def find_similar_movies(movie_id, X, k=10, metric='cosine', show_distance=False):
#     neighbour_ids = []

#     movie_ind = movie_mapper[movie_id]
#     movie_vec = X[movie_ind]
#     k += 1

#     kNN = NearestNeighbors(n_neighbors=k, algorithm="brute", metric=metric)
#     kNN.fit(X)

#     movie_vec = movie_vec.reshape(1, -1)
#     neighbour = kNN.kneighbors(movie_vec, return_distance=show_distance)

#     for i in range(1, k):
#         n = neighbour[1].item(i) if show_distance else neighbour[0].item(i)
#         neighbour_ids.append(movie_inv_mapper[n])

#     return neighbour_ids
# recommendation.py
# import numpy as np
# from scipy.sparse import csr_matrix
# from sklearn.neighbors import NearestNeighbors
# from .models import Movie, Review

# def create_matrix():
#     reviews = Review.objects.all().values('user_id', 'movie_id', 'rating')
#     user_ids = list(set(review['user_id'] for review in reviews))
#     movie_ids = list(set(review['movie_id'] for review in reviews))
    
#     user_mapper = {user_id: i for i, user_id in enumerate(user_ids)}
#     movie_mapper = {movie_id: i for i, movie_id in enumerate(movie_ids)}
    
#     user_inv_mapper = {i: user_id for user_id, i in user_mapper.items()}
#     movie_inv_mapper = {i: movie_id for movie_id, i in movie_mapper.items()}
    
#     user_index = [user_mapper[review['user_id']] for review in reviews]
#     movie_index = [movie_mapper[review['movie_id']] for review in reviews]
#     ratings = [review['rating'] for review in reviews]
    
#     X = csr_matrix((ratings, (movie_index, user_index)), shape=(len(movie_ids), len(user_ids)))
#     return X, user_mapper, movie_mapper, user_inv_mapper, movie_inv_mapper

# def find_similar_movies(movie_id, k=10):
#     X, user_mapper, movie_mapper, user_inv_mapper, movie_inv_mapper = create_matrix()
    
#     movie_ind = movie_mapper.get(movie_id)
#     if movie_ind is None:
#         return []

#     movie_vec = X[movie_ind].reshape(1, -1)
#     kNN = NearestNeighbors(n_neighbors=k+1, algorithm="brute", metric="cosine")
#     kNN.fit(X)
#     neighbour = kNN.kneighbors(movie_vec, return_distance=False)
    
#     similar_movie_ids = [movie_inv_mapper[i] for i in neighbour[0] if i != movie_ind]
#     print(similar_movie_ids)
#     return Movie.objects.filter(id__in=similar_movie_ids)

# def recommend_movies_for_user(user_id, k=10):
    # user_reviews = Review.objects.filter(user_id=user_id)
    # if not user_reviews.exists():
    #     return Movie.objects.none()

    # highest_rated_review = user_reviews.order_by('-rating').first()
    # return find_similar_movies(highest_rated_review.movie_id, k)
    
import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from .models import Movie, Review

# Global variables to store matrix and mappings
X = None
user_mapper = {}
movie_mapper = {}
user_inv_mapper = {}
movie_inv_mapper = {}

def load_data():
    reviews = Review.objects.all().values('user_id', 'movie_id', 'rating')
    df = pd.DataFrame(reviews)
    return df

def create_matrix(df):
    global X, user_mapper, movie_mapper, user_inv_mapper, movie_inv_mapper

    N = len(df['user_id'].unique())
    M = len(df['movie_id'].unique())

    user_mapper = {user_id: idx for idx, user_id in enumerate(np.unique(df["user_id"]))}
    movie_mapper = {movie_id: idx for idx, movie_id in enumerate(np.unique(df["movie_id"]))}

    user_inv_mapper = {idx: user_id for user_id, idx in user_mapper.items()}
    movie_inv_mapper = {idx: movie_id for movie_id, idx in movie_mapper.items()}

    user_index = [user_mapper[user_id] for user_id in df['user_id']]
    movie_index = [movie_mapper[movie_id] for movie_id in df['movie_id']]

    X = csr_matrix((df["rating"], (movie_index, user_index)), shape=(M, N))

def update_matrix():
    df = load_data()
    create_matrix(df)

def find_similar_movies(movie_id, k=10, metric='cosine', show_distance=False):
    global X, user_mapper, movie_mapper, user_inv_mapper, movie_inv_mapper

    neighbour_ids = []

    movie_ind = movie_mapper[movie_id]
    movie_vec = X[movie_ind]
    k += 1

    kNN = NearestNeighbors(n_neighbors=k, algorithm="brute", metric=metric)
    kNN.fit(X)

    movie_vec = movie_vec.reshape(1, -1)
    neighbour = kNN.kneighbors(movie_vec, return_distance=show_distance)

    for i in range(1, k):
        n = neighbour[1].item(i) if show_distance else neighbour[0].item(i)
        neighbour_ids.append(movie_inv_mapper[n])

    return neighbour_ids

# Initial matrix creation
update_matrix()
