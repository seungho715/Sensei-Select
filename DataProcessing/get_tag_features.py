import pandas as pd


def get_tag_features(tag):
    # redo with TF-IDF
    features = {
        'tag_name': tag['name'],
        'tag_description': tag['description'],
    }

    df = pd.DataFrame(data=features, index=[0])
    return df