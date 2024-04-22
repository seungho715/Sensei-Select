import pandas as pd


def get_character_features(character):
    # redo with TF-IDF
    features = {
        'character_name': character['name_full'],
        'character_description': character['description'],
    }

    df = pd.DataFrame(data=features, index=[0])
    return df