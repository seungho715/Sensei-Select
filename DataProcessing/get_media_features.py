import pandas as pd
from get_character_features import *
from get_tag_features import *

medias = pd.read_csv('../Tables/Media.csv')
media_statuses = pd.read_csv('../Tables/Media_Statuses.csv')
media_scores = pd.read_csv('../Tables/Media_Scores.csv')

media_genres = pd.read_csv('../Tables/Media_Genres.csv')

media_tags = pd.read_csv('../Tables/Media_Tag.csv')
media_tag_connection = pd.read_csv('../Tables/Media_Tag_Connection.csv')

media_characters = pd.read_csv('../Tables/Character.csv')
character_cast = pd.read_csv('../Tables/Character_Cast.csv')

media_ids = medias['id'].unique()


def get_media_features(id):
    media = medias.loc[medias['id'] == id]
    genres = media_genres.loc[media_genres['media_id'] == id]['genre_id']
    statuses = media_statuses.loc[media_statuses['media_id'] == id]
    scores = media_scores.loc[media_scores['media_id'] == id]
    tags = media_tags.merge(
        media_tag_connection.loc[media_tag_connection['media_id'] == id],
        left_on='id', right_on='tag_id'
    )\
        .drop(columns=['id', 'tag_id', 'is_media_spoiler'])

    characters = media_characters.merge(
        character_cast.loc[character_cast['media_id'] == id],
        left_on='id', right_on='character_id'
    )\
        .rename(columns={'id_x': 'id'})\
        .drop(columns=['id_y', 'character_id', 'character_name', 'media_id', 'mod_notes'])

    features = {
        'id': media['id'],

        # turn into TF-IDF
        'title': media['title_english'],

        'type_anime': int(media['type'] == 'ANIME'),
        'type_manga': int(media['type'] == 'MANGA'),

        'format_tv': int(media['format'] == 'TV'),
        'format_tv_short': int(media['format'] == 'TV_SHORT'),
        'format_movie': int(media['format'] == 'MOVIE'),
        'format_special': int(media['format'] == 'SPECIAL'),
        'format_ova': int(media['format'] == 'OVA'),
        'format_ona': int(media['format'] == 'ONA'),
        'format_music': int(media['format'] == 'MUSIC'),
        'format_manga': int(media['format'] == 'MANGA'),
        'format_novel': int(media['format'] == 'NOVEL'),
        'format_one_shot': int(media['format'] == 'ONE_SHOT'),

        # could choose to drop these
        'status_finished': int(media['status'] == 'FINISHED'),
        'status_releasing': int(media['status'] == 'RELEASING'),
        'status_not_yet_released': int(media['status'] == 'NOT_YET_RELEASED'),
        'status_cancelled': int(media['status'] == 'CANCELLED'),
        'status_hiatus': int(media['status'] == 'HIATUS'),

        # turn into TF-IDF
        'description': media['description'],

        'start_year': int(media['start_date'][0][:4]),

        # 'episodes': media['episodes'],
        'episodes_0_1': int(0 <= media['episodes'][0] <= 1),
        'episodes_1_15': int(1 < media['episodes'][0] <= 15),
        'episodes_15_30': int(15 < media['episodes'][0] <= 30),
        'episodes_30_60': int(30 < media['episodes'][0] <= 60),
        'episodes_60_100': int(60 < media['episodes'][0] <= 100),
        'episodes_100_300': int(100 < media['episodes'][0] <= 300),
        'episodes_300+': int(300 < media['episodes'][0]),

        'episode_duration': media['episode_duration'],
        'episodes_duration_0_8': int(0 <= media['episode_duration'][0] <= 8),
        'episodes_duration_8_16': int(8 < media['episode_duration'][0] <= 16),
        'episodes_duration_16_28': int(16 < media['episode_duration'][0] <= 28),
        'episodes_duration_28_55': int(28 < media['episode_duration'][0] <= 55),
        'episodes_duration_55_90': int(55 < media['episode_duration'][0] <= 90),
        'episodes_duration_90_180': int(90 < media['episode_duration'][0] <= 180),
        'episodes_duration_180+': int(180 < media['episode_duration'][0]),

        # 'chapters': media['chapters'],

        # 'volumes': media['volumes'],
        'volumes_0_1': int(0 <= media['volumes'][0] <= 1),
        'volumes_1_2': int(1 < media['volumes'][0] <= 2),
        'volumes_2_8': int(2 < media['volumes'][0] <= 8),
        'volumes_8_16': int(8 < media['volumes'][0] <= 16),
        'volumes_16_30': int(16 < media['volumes'][0] <= 30),
        'volumes_30_60': int(30 < media['volumes'][0] <= 60),
        'volumes_60_100': int(60 < media['volumes'][0] <= 100),
        'volumes_100+': int(100 < media['volumes'][0]),

        'source_original': int(media['source'] == 'ORIGINAL'),
        'source_manga': int(media['source'] == 'MANGA'),
        'source_light_novel': int(media['source'] == 'LIGHT_NOVEL'),
        'source_visual_novel': int(media['source'] == 'VISUAL_NOVEL'),
        'source_video_game': int(media['source'] == 'VIDEO_GAME'),
        'source_other': int(media['source'] == 'OTHER'),
        'source_novel': int(media['source'] == 'NOVEL'),
        'source_doujinshi': int(media['source'] == 'DOUJINSHI'),
        'source_anime': int(media['source'] == 'ANIME'),
        'source_web_novel': int(media['source'] == 'WEB_NOVEL'),
        'source_live_action': int(media['source'] == 'LIVE_ACTION'),
        'source_game': int(media['source'] == 'GAME'),
        'source_comic': int(media['source'] == 'COMIC'),
        'source_multimedia_project': int(media['source'] == 'MULTIMEDIA_PROJECT'),
        'source_picture_book': int(media['source'] == 'PICTURE_BOOK'),

        # pick one to use, mean is likely better
        # 'average_score': media['average_score'],
        'mean_score': media['mean_score'],

        'popularity': media['popularity'],
        'favourites': media['favourites'],

        'is_adult': int(media['is_adult']),

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

        'percent_current': statuses.loc[statuses['status'] == 'CURRENT']['amount'].values[0] / sum(statuses['amount']),
        'percent_planning': statuses.loc[statuses['status'] == 'PLANNING']['amount'].values[0] / sum(statuses['amount']),
        'percent_completed': statuses.loc[statuses['status'] == 'COMPLETED']['amount'].values[0] / sum(statuses['amount']),
        'percent_dropped': statuses.loc[statuses['status'] == 'DROPPED']['amount'].values[0] / sum(statuses['amount']),
        'percent_paused': statuses.loc[statuses['status'] == 'PAUSED']['amount'].values[0] / sum(statuses['amount']),

        'percent_score_10': scores.loc[scores['score'] == 10]['amount'].values[0] / sum(scores['amount']),
        'percent_score_20': scores.loc[scores['score'] == 20]['amount'].values[0] / sum(scores['amount']),
        'percent_score_30': scores.loc[scores['score'] == 30]['amount'].values[0] / sum(scores['amount']),
        'percent_score_40': scores.loc[scores['score'] == 40]['amount'].values[0] / sum(scores['amount']),
        'percent_score_50': scores.loc[scores['score'] == 50]['amount'].values[0] / sum(scores['amount']),
        'percent_score_60': scores.loc[scores['score'] == 60]['amount'].values[0] / sum(scores['amount']),
        'percent_score_70': scores.loc[scores['score'] == 70]['amount'].values[0] / sum(scores['amount']),
        'percent_score_80': scores.loc[scores['score'] == 80]['amount'].values[0] / sum(scores['amount']),
        'percent_score_90': scores.loc[scores['score'] == 90]['amount'].values[0] / sum(scores['amount']),
        'percent_score_100': scores.loc[scores['score'] == 100]['amount'].values[0] / sum(scores['amount']),
    }

    # get average of character TF-IDF stuff
    # for index, row in characters.iterrows():
    #     print(get_character_features(row))

    # get average of tag TF-IDF stuff
    # for index, row in tags.iterrows():
    #     print(get_tag_features(row))

    # concatenate character and tag features to the main media stuff

    df = pd.DataFrame(data=features, index=[0])
    return df



print(get_media_features(21))

