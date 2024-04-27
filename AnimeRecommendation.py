import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf

from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.utils import shuffle
from tensorflow import keras
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, LearningRateScheduler, EarlyStopping
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD

# Suppress warnings for cleaner notebook output
import warnings
warnings.filterwarnings(action='ignore')

class Recommender():

    df = None
    tfidf_matrix = None
    dense_tfidf_matrix = None

    def __init__(self):
        self.df = self.load_and_preprocess_data('Tables/final_features_romanji.csv')
        self.tfidf_matrix = self.generate_tfidf_matrix(self.df, max_features=5000)  # Reduced number of features
        self.dense_tfidf_matrix = self.reduce_dimensions(self.tfidf_matrix, n_components=500)  # Further reduction with SVD

    def reduce_dimensions(self, matrix, n_components=1000):
        svd = TruncatedSVD(n_components=n_components)
        return svd.fit_transform(matrix)

    # Helper function to normalize text
    def normalize_text(self,text):
        return text.replace(" ", "").lower()

    # Load and preprocess data
    def load_and_preprocess_data(self, filepath):
        df = pd.read_csv(filepath)
        df['title'] = df['title'].astype(str).apply(self.normalize_text)
        df['description'] = df['description'].astype(str)  # Ensure text is treated as string
        df = df.drop_duplicates()
        return df

    # Generate TF-IDF matrix
    def generate_tfidf_matrix(self, df, column='description', max_features=10000):
        tfidf = TfidfVectorizer(stop_words='english', max_features=max_features)
        return tfidf.fit_transform(df[column])


    # Build a neural network model
    def build_feature_model(self, input_dim):
        inputs = Input(shape=(input_dim,))
        x = Dense(128, activation='relu')(inputs)
        x = Dense(64, activation='relu')(x)
        outputs = Dense(input_dim, activation='linear')(x)
        model = Model(inputs=inputs, outputs=outputs)
        model.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error')
        return model

    # Find recommendations based on similarity
    def find_recommendations(self, title, df, tfidf_matrix, model, top_n=10):
        title = self.normalize_text(title)
        indices = df.index[df['title'] == title].tolist()
        if not indices:
            print(f"No recommendations found for title: {title}")
            return pd.DataFrame()

        idx = indices[0]
        features = tfidf_matrix[idx:idx+1]  # Select the TF-IDF features for the given title
        similarities = cosine_similarity(features, tfidf_matrix).flatten()
        top_indices = np.argsort(similarities)[-top_n-1:-1][::-1]

        all_shows = pd.read_csv("Tables/final_features_romanji.csv", index_col="id")
        matches = df.iloc[top_indices].set_index("id")
        matches.update(all_shows)
        matches.reset_index(inplace=True)
        #for index, match in matches.iterrows():
        #    print(all_shows.xs(index))
        #    match['title'] = all_shows.xs(index)['title']
        
        
        #for match in matches:
        #    match['title'] = all_shows.loc[all_shows['id'] == int(match['id'])]['title']

        return matches

    def recommendation_flow(self, initial_title, saved=False):
        feature_model = None
        if saved:
            feature_model = tf.keras.models.load_model('trained_model.h5')
            #feature_model = TFSMLayer('models/trained_model', call_endpoint='serving_default')
        else:
            feature_model = self.build_feature_model(self.dense_tfidf_matrix.shape[1])
            feature_model.fit(self.dense_tfidf_matrix, self.dense_tfidf_matrix, epochs=10, batch_size=32, verbose=1)

            feature_model.save('trained_model.h5')

        recommendations = self.find_recommendations(initial_title, self.df, self.tfidf_matrix, feature_model)
        print("Recommendations based on:", initial_title)
        if not recommendations.empty:
            print(recommendations['title'])
        else:
            print("No recommendations to display.")
        return recommendations

    # Main function to orchestrate the workflow
    def main(self):
        parser = argparse.ArgumentParser("animerecommendation")
        parser.add_argument("name", help="An anime similar to one you want to watch", type=str)
        parser.add_argument("--saved", help="Use a saved model rather than train a new one", type=bool, default=False)
        args = parser.parse_args()

        print(str(args))
        print(args.saved)
        self.recommendation_flow(args.name, args.saved)


if __name__ == "__main__":
    recommender = Recommender()
    recommender.main()