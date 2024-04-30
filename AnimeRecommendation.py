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
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.base import TransformerMixin, BaseEstimator

# Suppress warnings for cleaner notebook output
import warnings
warnings.filterwarnings(action='ignore')

class DenseTransformer(TransformerMixin):
    """Ensures that output from the pipeline is a dense matrix."""

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        if isinstance(X, np.ndarray):
            return X
        else:
            return X.toarray()
        
class DebugTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        print(f"Fit - Data type: {type(X)}, Shape: {X.shape if hasattr(X, 'shape') else 'No shape'}")
        return self

    def transform(self, X):
        print(f"Transform - Data type: {type(X)}, Shape: {X.shape if hasattr(X, 'shape') else 'No shape'}")
        return X

class Recommender():

    df = None
    tfidf_matrix = None
    feature_matrix = None

    def __init__(self):
        self.df = pd.read_csv('Tables/final_features_romanji.csv')
        self.df.fillna('unknown', inplace=True)
        self.df['description'] = self.df['description'].apply(lambda x: x.strip() if x.strip() != '' else 'unknown')

        self.feature_matrix, self.df = self.load_and_preprocess_data('Tables/final_features_romanji.csv')
        print("Data processing completed.")

    def reduce_dimensions(self, matrix, n_components=1000):
        svd = TruncatedSVD(n_components=n_components)
        return svd.fit_transform(matrix)

    # Helper function to normalize text
    def normalize_text(self,text):
        return text.replace(" ", "").lower()

    # Load and preprocess data
    def load_and_preprocess_data(self, filepath):
        # Load the data
        df = pd.read_csv(filepath)
        df.fillna('unknown', inplace=True)
        df['description'] = df['description'].apply(lambda x: x.strip() if x.strip() != '' else 'unknown')

        # Normalize text data for 'title' and 'description'
        df['title'] = df['title'].astype(str).apply(self.normalize_text)
        df['description'] = df['description'].astype(str)

        print("Number of descriptions to process:", len(df['description']))  # Ensure full length is considered

        numerical_cols = ['start_year', 'mean_score', 'popularity', 'favourites']
        categorical_cols = [
            'type_anime', 'type_manga', 'format_tv', 'format_tv_short', 'format_movie',
            'format_special', 'format_ova', 'format_ona', 'format_music', 'format_manga',
            'format_novel', 'format_one_shot', 'status_finished', 'status_releasing',
            'status_not_yet_released', 'status_cancelled'
        ]
        text_col = 'description'  # Directly use the column name as a string

        numerical_transformer = Pipeline([
            ('imputer', SimpleImputer(strategy='mean')),
            ('scaler', MinMaxScaler())
        ])
        categorical_transformer = Pipeline([
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(handle_unknown='ignore')),
            ('to_dense', DenseTransformer())  # Convert to dense
        ])
        text_transformer = Pipeline([
            ('debug_before', DebugTransformer()),
            ('tfidf', TfidfVectorizer(stop_words='english', max_features=5000)),
            ('debug_after', DebugTransformer()),
            ('to_dense', DenseTransformer())  # Ensure output is dense
        ])

        preprocessor = ColumnTransformer([
            ('num', numerical_transformer, numerical_cols),
            ('cat', categorical_transformer, categorical_cols),
            ('text', text_transformer, text_col)
        ], remainder='drop')

        feature_matrix = preprocessor.fit_transform(df)
        print("Shape of the fully processed feature matrix after ColumnTransformer:", feature_matrix.shape)
        return feature_matrix, df

    # Generate TF-IDF matrix
    '''def generate_tfidf_matrix(self, df, column='description', max_features=10000):
        tfidf = TfidfVectorizer(stop_words='english', max_features=max_features)
        return tfidf.fit_transform(df[column])
    '''


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
            feature_model = self.build_feature_model(self.feature_matrix.shape[1])
            feature_model.fit(self.feature_matrix, self.feature_matrix, epochs=10, batch_size=32, verbose=1)

            feature_model.save('trained_model.h5')

        recommendations = self.find_recommendations(initial_title, self.df, self.feature_matrix, feature_model)
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
