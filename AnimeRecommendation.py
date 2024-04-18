import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.utils import shuffle
from keras.layers import Input, Embedding, Dot, Flatten, Dense
from keras.models import Model
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint, LearningRateScheduler, EarlyStopping

# Suppress warnings for cleaner notebook output
import warnings
warnings.filterwarnings(action='ignore')


# Load data
def load_data(filepath):
    """ Load dataset from a specified file path. """
    df = pd.read_csv(filepath, usecols=["account_id", "media_id", "score"])
    print(df.shape)
    df.head()
    return df


# Preprocess data
def preprocess_data(df):
    """ Preprocess the data by checking duplicates, normalizing and encoding features. """
    # Checking if there are any duplicate rows
    duplicated_rows = df[df.duplicated()]
    print("Duplicated Rows:")
    print(duplicated_rows)

    # Scaling our "rating" column
    scaler = MinMaxScaler(feature_range=(0, 1))
    df['scaled_score'] = scaler.fit_transform(df[['score']])

    # Encoding categorical data
    user_encoder = LabelEncoder()
    df["user_encoded"] = user_encoder.fit_transform(df["account_id"])
    num_users = len(user_encoder.classes_)

    anime_encoder = LabelEncoder()
    df["anime_encoded"] = anime_encoder.fit_transform(df["media_id"])
    num_animes = len(anime_encoder.classes_)

    print("Number of unique users: {}, Number of unique anime: {}".format(num_users, num_animes))
    print("Minimum rating: {}, Maximum rating: {}".format(min(df['score']), max(df['score'])))

    return df, user_encoder, anime_encoder, num_users, num_animes


# Shuffle and split the dataset
def split_data(df, test_size=10000):
    """ Shuffle and split the data into training and testing datasets. """
    df = shuffle(df, random_state=100)
    X = df[['user_encoded', 'anime_encoded']].values
    y = df["scaled_score"].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=73)
    print("Number of samples in the training set:", len(y_train))
    print("Number of samples in the test set:", len(y_test))
    return X_train, X_test, y_train, y_test


# Define the recommender neural network
def RecommenderNet(num_users, num_animes, embedding_size=128):
    """ Build a neural network model for recommendation. """
    user = Input(name='user_encoded', shape=[1])
    user_embedding = Embedding(name='user_embedding', input_dim=num_users, output_dim=embedding_size)(user)

    anime = Input(name='anime_encoded', shape=[1])
    anime_embedding = Embedding(name='anime_embedding', input_dim=num_animes, output_dim=embedding_size)(anime)

    dot_product = Dot(name='dot_product', normalize=True, axes=2)([user_embedding, anime_embedding])
    flattened = Flatten()(dot_product)

    dense = Dense(64, activation='relu')(flattened)
    output = Dense(1, activation='sigmoid')(dense)

    model = Model(inputs=[user, anime], outputs=output)
    model.compile(loss='binary_crossentropy', optimizer=Adam(learning_rate=0.001), metrics=["mae", "mse"])
    return model


# Load additional data for TF-IDF
def load_genre_data(filepath):
    """ Load additional data that contains genres for TF-IDF vectorization. """
    df = pd.read_csv(filepath)
    return df


# Generate TF-IDF matrix for content-based filtering
def generate_tfidf_matrix(df):
    """ Generate a TF-IDF matrix from anime genres to use for content-based similarity. """
    for i, entry in enumerate(df['genre_id']):
        if entry is np.nan:
            df['genres'][i] = "N/A"
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['genre_id'])
    return tfidf_matrix


# Find recommendations based on cosine similarity
def find_recommendations(media_id, df, tfidf_matrix, top_n=10):
    """ Find top-n recommendations based on cosine similarity of genre vectors. """
    idx = df.index[df['media_id'] == media_id].tolist()[0]
    cosine_similarities = linear_kernel(tfidf_matrix[idx], tfidf_matrix).flatten()
    similar_indices = cosine_similarities.argsort()[-top_n - 1:-1][::-1]
    return [df.iloc[i]['media_id'] for i in similar_indices if i != idx]


# Function to get predictions from the neural network
def get_nn_predictions(user_id, anime_ids, model, user_encoder, anime_encoder):
    """ Given a list of anime IDs, predict the user's rating for these animes using the trained neural network model. """
    user_encoded = user_encoder.transform([user_id] * len(anime_ids))
    anime_encoded = anime_encoder.transform(anime_ids)
    predictions = model.predict([user_encoded, anime_encoded]).flatten()
    return predictions


def refine_recommendations(user_id, candidate_anime_ids, df, model, user_encoder, anime_encoder):
    """ Refine recommendations by re-ranking candidate anime ids based on the collaborative filtering model predictions. """
    predictions = get_nn_predictions(user_id, candidate_anime_ids, model, user_encoder, anime_encoder)
    recommended_anime_ids = np.array(candidate_anime_ids)[
        np.argsort(predictions)[::-1]]  # Sort by descending prediction score
    return df[df['media_id'].isin(recommended_anime_ids)][['media_id', 'media_id']].set_index('media_id').loc[
        recommended_anime_ids].reset_index()


def main():
    # Load and preprocess data
    df = load_data('Tables/Media_List_Entry.csv')
    df, user_encoder, anime_encoder, num_users, num_animes = preprocess_data(df)

    # Additional data loading for TF-IDF
    df_genres = load_genre_data('Tables/Media_Genres.csv')
    tfidf_matrix = generate_tfidf_matrix(df_genres)

    # User input
    user_id = '5454172'  # Example user ID
    media_id = 105932  # Starting point for recommendations

    # Get initial recommendations
    candidate_anime_ids = find_recommendations(media_id, df_genres, tfidf_matrix, top_n=10)

    # Split data
    X_train, X_test, y_train, y_test = split_data(df)

    # Prepare and train model
    model = RecommenderNet(num_users, num_animes)
    model.fit([X_train[:, 0], X_train[:, 1]], y_train, epochs=1, verbose=1,
              validation_data=([X_test[:, 0], X_test[:, 1]], y_test))

    # Refine recommendations using the trained model
    final_recommendations = refine_recommendations(user_id, candidate_anime_ids, df_genres, model, user_encoder,
                                                   anime_encoder)
    print("Refined Recommendations:")
    print(final_recommendations)


if __name__ == "__main__":
    main()
