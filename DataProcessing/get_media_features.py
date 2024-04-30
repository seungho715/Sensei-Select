import pandas as pd
from get_character_features import *
from get_tag_features import *

def load_data():
    medias = pd.read_csv('../Tables/Media.csv')
    media_statuses = pd.read_csv('../Tables/Media_Statuses.csv')
    media_scores = pd.read_csv('../Tables/Media_Scores.csv')
    media_genres = pd.read_csv('../Tables/Media_Genres.csv')
    media_tags = pd.read_csv('../Tables/Media_Tag.csv')
    media_tag_connection = pd.read_csv('../Tables/Media_Tag_Connection.csv')
    media_characters = pd.read_csv('../Tables/Character.csv')
    character_cast = pd.read_csv('../Tables/Character_Cast.csv')
    return medias, media_statuses, media_scores, media_genres, media_tags, media_tag_connection, media_characters, character_cast

def get_year(media):
    try:
        return int(media['start_date'][0][:4])
    except:
        return -1

# def get_media_features(id, medias, media_genres, media_statuses, media_scores, media_tags, media_tag_connection, media_characters, character_cast):
#     media = medias.loc[medias['id'] == id].drop_duplicates()
#     if media.empty:
#         return None
#
#     media.fillna({
#         'title_romanji': 'Unknown Title',
#         'type': 'Unknown',
#         'format': 'Unknown',
#         'status': 'Unknown',
#         'description': 'No Description Available',
#         'episodes': 0,
#         'episode_duration': 0,
#         'volumes': 0,
#         'source': 'Unknown',
#         'mean_score': 0,
#         'popularity': 0,
#         'favourites': 0,
#         'is_adult': False
#     }, inplace=True)
#
#     media = medias.loc[medias['id'] == id].drop_duplicates()
#     genres = media_genres.loc[media_genres['media_id'] == id]['genre_id']
#     statuses = media_statuses.loc[media_statuses['media_id'] == id]
#     scores = media_scores.loc[media_scores['media_id'] == id]
#     tags = media_tags.merge(
#         media_tag_connection.loc[media_tag_connection['media_id'] == id],
#         left_on='id', right_on='tag_id'
#     )\
#         .drop(columns=['id', 'tag_id', 'is_media_spoiler'])
#
#     characters = media_characters.merge(
#         character_cast.loc[character_cast['media_id'] == id],
#         left_on='id', right_on='character_id'
#     )\
#         .rename(columns={'id_x': 'id'})\
#         .drop(columns=['id_y', 'character_id', 'character_name', 'media_id', 'mod_notes'])
#
#     features = {
#         'id': media['id'],
#
#         # turn into TF-IDF
#         'title': media['title_romanji'],
#
#         'type_anime': int(media['type'] == 'ANIME'),
#         'type_manga': int(media['type'] == 'MANGA'),
#
#         'format_tv': int(media['format'] == 'TV'),
#         'format_tv_short': int(media['format'] == 'TV_SHORT'),
#         'format_movie': int(media['format'] == 'MOVIE'),
#         'format_special': int(media['format'] == 'SPECIAL'),
#         'format_ova': int(media['format'] == 'OVA'),
#         'format_ona': int(media['format'] == 'ONA'),
#         'format_music': int(media['format'] == 'MUSIC'),
#         'format_manga': int(media['format'] == 'MANGA'),
#         'format_novel': int(media['format'] == 'NOVEL'),
#         'format_one_shot': int(media['format'] == 'ONE_SHOT'),
#
#         # could choose to drop these
#         'status_finished': int(media['status'] == 'FINISHED'),
#         'status_releasing': int(media['status'] == 'RELEASING'),
#         'status_not_yet_released': int(media['status'] == 'NOT_YET_RELEASED'),
#         'status_cancelled': int(media['status'] == 'CANCELLED'),
#         'status_hiatus': int(media['status'] == 'HIATUS'),
#
#         # turn into TF-IDF
#         'description': media['description'],
#
#         'start_year': get_year(media),
#
#         # 'episodes': media['episodes'],
#         'episodes_0_1': int(0 <= media['episodes'].iloc[0] <= 1),
#         'episodes_1_15': int(1 < media['episodes'].iloc[0] <= 15),
#         'episodes_15_30': int(15 < media['episodes'].iloc[0] <= 30),
#         'episodes_30_60': int(30 < media['episodes'].iloc[0] <= 60),
#         'episodes_60_100': int(60 < media['episodes'].iloc[0] <= 100),
#         'episodes_100_300': int(100 < media['episodes'].iloc[0] <= 300),
#         'episodes_300+': int(300 < media['episodes'].iloc[0]),
#
#         'episode_duration': int(media['episode_duration'].iloc[0]),
#         'episodes_duration_0_8': int(0 <= media['episode_duration'].iloc[0] <= 8),
#         'episodes_duration_8_16': int(8 < media['episode_duration'].iloc[0] <= 16),
#         'episodes_duration_16_28': int(16 < media['episode_duration'].iloc[0] <= 28),
#         'episodes_duration_28_55': int(28 < media['episode_duration'].iloc[0] <= 55),
#         'episodes_duration_55_90': int(55 < media['episode_duration'].iloc[0] <= 90),
#         'episodes_duration_90_180': int(90 < media['episode_duration'].iloc[0] <= 180),
#         'episodes_duration_180+': int(180 < media['episode_duration'].iloc[0]),
#
#         # 'chapters': media['chapters'],
#
#         # 'volumes': media['volumes'],
#         'volumes_0_1': int(0 <= media['volumes'].iloc[0] <= 1),
#         'volumes_1_2': int(1 < media['volumes'].iloc[0] <= 2),
#         'volumes_2_8': int(2 < media['volumes'].iloc[0] <= 8),
#         'volumes_8_16': int(8 < media['volumes'].iloc[0] <= 16),
#         'volumes_16_30': int(16 < media['volumes'].iloc[0] <= 30),
#         'volumes_30_60': int(30 < media['volumes'].iloc[0] <= 60),
#         'volumes_60_100': int(60 < media['volumes'].iloc[0] <= 100),
#         'volumes_100+': int(100 < media['volumes'].iloc[0]),
#
#         'source_original': int(media['source'] == 'ORIGINAL'),
#         'source_manga': int(media['source'] == 'MANGA'),
#         'source_light_novel': int(media['source'] == 'LIGHT_NOVEL'),
#         'source_visual_novel': int(media['source'] == 'VISUAL_NOVEL'),
#         'source_video_game': int(media['source'] == 'VIDEO_GAME'),
#         'source_other': int(media['source'] == 'OTHER'),
#         'source_novel': int(media['source'] == 'NOVEL'),
#         'source_doujinshi': int(media['source'] == 'DOUJINSHI'),
#         'source_anime': int(media['source'] == 'ANIME'),
#         'source_web_novel': int(media['source'] == 'WEB_NOVEL'),
#         'source_live_action': int(media['source'] == 'LIVE_ACTION'),
#         'source_game': int(media['source'] == 'GAME'),
#         'source_comic': int(media['source'] == 'COMIC'),
#         'source_multimedia_project': int(media['source'] == 'MULTIMEDIA_PROJECT'),
#         'source_picture_book': int(media['source'] == 'PICTURE_BOOK'),
#
#         # pick one to use, mean is likely better
#         # 'average_score': media['average_score'],
#         'mean_score': media['mean_score'],
#
#         'popularity': media['popularity'],
#         'favourites': media['favourites'],
#
#         'is_adult': int(media['is_adult']),
#
#         'genre_action': int('Action' in genres.values),
#         'genre_adventure': int('Adventure' in genres.values),
#         'genre_comedy': int('Comedy' in genres.values),
#         'genre_drama': int('Drama' in genres.values),
#         'genre_ecchi': int('Ecchi' in genres.values),
#         'genre_fantasy': int('Fantasy' in genres.values),
#         'genre_hentai': int('Hentai' in genres.values),
#         'genre_horror': int('Horror' in genres.values),
#         'genre_mahou_shoujo': int('Mahou Shoujo' in genres.values),
#         'genre_mecha': int('Mecha' in genres.values),
#         'genre_music': int('Music' in genres.values),
#         'genre_mystery': int('Mystery' in genres.values),
#         'genre_psychological': int('Psychological' in genres.values),
#         'genre_romance': int('Romance' in genres.values),
#         'genre_sci-fi': int('Sci-Fi' in genres.values),
#         'genre_slice_of_life': int('Slice of Life' in genres.values),
#         'genre_sports': int('Sports' in genres.values),
#         'genre_supernatural': int('Supernatural' in genres.values),
#         'genre_thriller': int('Thriller' in genres.values),
#
#         'percent_current': next(iter(statuses.loc[statuses['status'] == 'CURRENT']['amount'].values), 0) / (sum(statuses['amount']) or -1),
#         'percent_planning': next(iter(statuses.loc[statuses['status'] == 'PLANNING']['amount'].values), 0) / (sum(statuses['amount']) or -1),
#         'percent_completed': next(iter(statuses.loc[statuses['status'] == 'COMPLETED']['amount'].values), 0) / (sum(statuses['amount']) or -1),
#         'percent_dropped': next(iter(statuses.loc[statuses['status'] == 'DROPPED']['amount'].values), 0) / (sum(statuses['amount']) or -1),
#         'percent_paused': next(iter(statuses.loc[statuses['status'] == 'PAUSED']['amount'].values), 0) / (sum(statuses['amount']) or -1),
#
#         'percent_score_10': next(iter(scores.loc[scores['score'] == 10]['amount'].values), 0) / (sum(scores['amount']) or -1),
#         'percent_score_20': next(iter(scores.loc[scores['score'] == 20]['amount'].values), 0) / (sum(scores['amount']) or -1),
#         'percent_score_30': next(iter(scores.loc[scores['score'] == 30]['amount'].values), 0) / (sum(scores['amount']) or -1),
#         'percent_score_40': next(iter(scores.loc[scores['score'] == 40]['amount'].values), 0) / (sum(scores['amount']) or -1),
#         'percent_score_50': next(iter(scores.loc[scores['score'] == 50]['amount'].values), 0) / (sum(scores['amount']) or -1),
#         'percent_score_60': next(iter(scores.loc[scores['score'] == 60]['amount'].values), 0) / (sum(scores['amount']) or -1),
#         'percent_score_70': next(iter(scores.loc[scores['score'] == 70]['amount'].values), 0) / (sum(scores['amount']) or -1),
#         'percent_score_80': next(iter(scores.loc[scores['score'] == 80]['amount'].values), 0) / (sum(scores['amount']) or -1),
#         'percent_score_90': next(iter(scores.loc[scores['score'] == 90]['amount'].values), 0) / (sum(scores['amount']) or -1),
#         'percent_score_100': next(iter(scores.loc[scores['score'] == 100]['amount'].values), 0) / (sum(scores['amount']) or -1),
#     }
#
#     # get average of character TF-IDF stuff
#     # for index, row in characters.iterrows():
#     #     print(get_character_features(row))
#
#     # get average of tag TF-IDF stuff
#     # for index, row in tags.iterrows():
#     #     print(get_tag_features(row))
#
#     # concatenate character and tag features to the main media stuff
#
#     features = {'id': media['id'].iloc[0], 'title': media['title'].iloc[0], ...}
#     return pd.DataFrame([features])

def get_media_features(id, medias, media_genres, media_statuses, media_scores):
    media = medias.loc[medias['id'] == id]
    if media.empty:
        print(f"Warning: No data found for media ID {id}. Skipping...")
        return None

    # Fill missing values with appropriate defaults
    media.fillna({
        'title_romanji': 'Unknown Title',
        'type': 'Unknown',
        'format': 'Unknown',
        'status': 'Unknown',
        'description': 'No Description Available',
        'episodes': 0,
        'episode_duration': 0,
        'volumes': 0,
        'source': 'Unknown',
        'mean_score': 0,
        'popularity': 0,
        'favourites': 0,
        'is_adult': False
    }, inplace=True)

    genres = media_genres.loc[media_genres['media_id'] == id]['genre_id']
    statuses = media_statuses.loc[media_statuses['media_id'] == id]
    scores = media_scores.loc[media_scores['media_id'] == id]

    features = {
        'id': media['id'].iloc[0],
        'title': media['title_romanji'].iloc[0],
        'type_anime': int(media['type'].iloc[0] == 'ANIME'),
        'type_manga': int(media['type'].iloc[0] == 'MANGA'),
        'format_tv': int(media['format'].iloc[0] == 'TV'),
        'format_tv_short': int(media['format'].iloc[0] == 'TV_SHORT'),
        'format_movie': int(media['format'].iloc[0] == 'MOVIE'),
        'format_special': int(media['format'].iloc[0] == 'SPECIAL'),
        'format_ova': int(media['format'].iloc[0] == 'OVA'),
        'format_ona': int(media['format'].iloc[0] == 'ONA'),
        'format_music': int(media['format'].iloc[0] == 'MUSIC'),
        'format_manga': int(media['format'].iloc[0] == 'MANGA'),
        'format_novel': int(media['format'].iloc[0] == 'NOVEL'),
        'format_one_shot': int(media['format'].iloc[0] == 'ONE_SHOT'),
        'status_finished': int(media['status'].iloc[0] == 'FINISHED'),
        'status_releasing': int(media['status'].iloc[0] == 'RELEASING'),
        'status_not_yet_released': int(media['status'].iloc[0] == 'NOT_YET_RELEASED'),
        'status_cancelled': int(media['status'].iloc[0] == 'CANCELLED'),
        'status_hiatus': int(media['status'].iloc[0] == 'HIATUS'),
        'description': media['description'].iloc[0],
        'start_year': get_year(media),
        'episodes_0_1': int(0 <= media['episodes'].iloc[0] <= 1),
        'episodes_1_15': int(1 < media['episodes'].iloc[0] <= 15),
        'episodes_15_30': int(15 < media['episodes'].iloc[0] <= 30),
        'episodes_30_60': int(30 < media['episodes'].iloc[0] <= 60),
        'episodes_60_100': int(60 < media['episodes'].iloc[0] <= 100),
        'episodes_100_300': int(100 < media['episodes'].iloc[0] <= 300),
        'episodes_300+': int(300 < media['episodes'].iloc[0]),
        'episode_duration': int(media['episode_duration'].iloc[0]),
        'episodes_duration_0_8': int(0 <= media['episode_duration'].iloc[0] <= 8),
        'episodes_duration_8_16': int(8 < media['episode_duration'].iloc[0] <= 16),
        'episodes_duration_16_28': int(16 < media['episode_duration'].iloc[0] <= 28),
        'episodes_duration_28_55': int(28 < media['episode_duration'].iloc[0] <= 55),
        'episodes_duration_55_90': int(55 < media['episode_duration'].iloc[0] <= 90),
        'episodes_duration_90_180': int(90 < media['episode_duration'].iloc[0] <= 180),
        'episodes_duration_180+': int(180 < media['episode_duration'].iloc[0]),
        'volumes_0_1': int(0 <= media['volumes'].iloc[0] <= 1),
        'volumes_1_2': int(1 < media['volumes'].iloc[0] <= 2),
        'volumes_2_8': int(2 < media['volumes'].iloc[0] <= 8),
        'volumes_8_16': int(8 < media['volumes'].iloc[0] <= 16),
        'volumes_16_30': int(16 < media['volumes'].iloc[0] <= 30),
        'volumes_30_60': int(30 < media['volumes'].iloc[0] <= 60),
        'volumes_60_100': int(60 < media['volumes'].iloc[0] <= 100),
        'volumes_100+': int(100 < media['volumes'].iloc[0]),
        'source_original': int(media['source'].iloc[0] == 'ORIGINAL'),
        'source_manga': int(media['source'].iloc[0] == 'MANGA'),
        'source_light_novel': int(media['source'].iloc[0] == 'LIGHT_NOVEL'),
        'source_visual_novel': int(media['source'].iloc[0] == 'VISUAL_NOVEL'),
        'source_video_game': int(media['source'].iloc[0] == 'VIDEO_GAME'),
        'source_other': int(media['source'].iloc[0] == 'OTHER'),
        'source_novel': int(media['source'].iloc[0] == 'NOVEL'),
        'source_doujinshi': int(media['source'].iloc[0] == 'DOUJINSHI'),
        'source_anime': int(media['source'].iloc[0] == 'ANIME'),
        'source_web_novel': int(media['source'].iloc[0] == 'WEB_NOVEL'),
        'source_live_action': int(media['source'].iloc[0] == 'LIVE_ACTION'),
        'source_game': int(media['source'].iloc[0] == 'GAME'),
        'source_comic': int(media['source'].iloc[0] == 'COMIC'),
        'source_multimedia_project': int(media['source'].iloc[0] == 'MULTIMEDIA_PROJECT'),
        'source_picture_book': int(media['source'].iloc[0] == 'PICTURE_BOOK'),
        'mean_score': media['mean_score'].iloc[0],
        'popularity': media['popularity'].iloc[0],
        'favourites': media['favourites'].iloc[0],
        'is_adult': int(media['is_adult'].iloc[0]),
        'genre_action': int('Action' in genres.values),
        'genre_adventure': int('Adventure' in genres.values),
        'genre_comedy': int('Comedy' in genres.values),
        'genre_drama': int('Drama' in genres.values),
        'genre_ecchi': int('Ecchi' in genres.values),
        'genre_fantasy': int('Fantasy' in genres.values),
        'genre_hentai': int('Hentai' in genres.values),
        'genre_horror': int('Horror' in genres.values),
        'genre_mahou_shoujo': int('Mahou Shoujo' in genres.values),
        'genre_mecha': int('Mecha' in genres.values),
        'genre_music': int('Music' in genres.values),
        'genre_mystery': int('Mystery' in genres.values),
        'genre_psychological': int('Psychological' in genres.values),
        'genre_romance': int('Romance' in genres.values),
        'genre_sci-fi': int('Sci-Fi' in genres.values),
        'genre_slice_of_life': int('Slice of Life' in genres.values),
        'genre_sports': int('Sports' in genres.values),
        'genre_supernatural': int('Supernatural' in genres.values),
        'genre_thriller': int('Thriller' in genres.values),

        'percent_current': next(iter(statuses.loc[statuses['status'] == 'CURRENT']['amount'].values), 0) / (
                    sum(statuses['amount']) or -1),
        'percent_planning': next(iter(statuses.loc[statuses['status'] == 'PLANNING']['amount'].values), 0) / (
                    sum(statuses['amount']) or -1),
        'percent_completed': next(iter(statuses.loc[statuses['status'] == 'COMPLETED']['amount'].values), 0) / (
                    sum(statuses['amount']) or -1),
        'percent_dropped': next(iter(statuses.loc[statuses['status'] == 'DROPPED']['amount'].values), 0) / (
                    sum(statuses['amount']) or -1),
        'percent_paused': next(iter(statuses.loc[statuses['status'] == 'PAUSED']['amount'].values), 0) / (
                    sum(statuses['amount']) or -1),

        'percent_score_10': next(iter(scores.loc[scores['score'] == 10]['amount'].values), 0) / (
                    sum(scores['amount']) or -1),
        'percent_score_20': next(iter(scores.loc[scores['score'] == 20]['amount'].values), 0) / (
                    sum(scores['amount']) or -1),
        'percent_score_30': next(iter(scores.loc[scores['score'] == 30]['amount'].values), 0) / (
                    sum(scores['amount']) or -1),
        'percent_score_40': next(iter(scores.loc[scores['score'] == 40]['amount'].values), 0) / (
                    sum(scores['amount']) or -1),
        'percent_score_50': next(iter(scores.loc[scores['score'] == 50]['amount'].values), 0) / (
                    sum(scores['amount']) or -1),
        'percent_score_60': next(iter(scores.loc[scores['score'] == 60]['amount'].values), 0) / (
                    sum(scores['amount']) or -1),
        'percent_score_70': next(iter(scores.loc[scores['score'] == 70]['amount'].values), 0) / (
                    sum(scores['amount']) or -1),
        'percent_score_80': next(iter(scores.loc[scores['score'] == 80]['amount'].values), 0) / (
                    sum(scores['amount']) or -1),
        'percent_score_90': next(iter(scores.loc[scores['score'] == 90]['amount'].values), 0) / (
                    sum(scores['amount']) or -1),
        'percent_score_100': next(iter(scores.loc[scores['score'] == 100]['amount'].values), 0) / (
                    sum(scores['amount']) or -1),
    }
    return pd.DataFrame([features])


# pd.set_option('display.max_columns', None)
# print(get_media_features(1))


def main():
    medias, media_statuses, media_scores, media_genres, media_tags, media_tag_connection, media_characters, character_cast = load_data()

    media_ids = medias['id'].unique()
    all_features = []

    for count, media_id in enumerate(media_ids, 1):
        features_df = get_media_features(media_id, medias, media_genres, media_statuses, media_scores)
        if features_df is not None:
            all_features.append(features_df)
        print(f'\rProcessing {count}/{len(media_ids)}', end='')

    if all_features:
        # Concatenate all feature DataFrames
        full_features_df = pd.concat(all_features, ignore_index=True)
        # Save the concatenated DataFrame to a CSV file
        full_features_df.to_csv('../Tables/final_features_romanji.csv', index=False)
        print("\nAll media features have been saved to 'final_features_romanji.csv'.")
    else:
        print("\nNo features to save.")


if __name__ == "__main__":
    main()