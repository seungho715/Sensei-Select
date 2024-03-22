import pandas as pd
from queries import *
from helper import *


# ====================
#
# This file uses the "media_ids.csv" file to scrape the following tables:
#  Media, Media_Genres, Media_Title_Synonyms, Media_Tag_Connection
#  Character_Cast, Character_Cast_Voice
#  Media_Relation, Staff_Connection, Studio_Connection
#
#  ** Note about Media_Genres table:
#     this actually stores the genre as a string, not as an id
#     like it should eventually be
#
#  ** uncomment the last line first to run this file
#
# ====================


def get_media(media_id):
    query = media_info_query(media_id)
    data = retrieve_data(query)
    media = data["data"]["Media"]

    id = media["id"]

    # The official titles of the media in various languages
    title_romanji = media["title"]["romaji"]
    title_english = media["title"]["english"]
    title_native = media["title"]["native"]

    type = media["type"]
    format = media["format"]
    status = media["status"]
    # description = media["description"].replace('\n', '\\n').replace('\t', '\\t') \
    #     if media["description"] is not None else None
    description = media["description"]
    start_date = f'{media["startDate"]["year"]}-{media["startDate"]["month"]}-{media["startDate"]["day"]}'
    end_date = f'{media["endDate"]["year"]}-{media["endDate"]["month"]}-{media["endDate"]["day"]}'
    season = media["season"]
    season_year = media["seasonYear"]
    season_int = media["seasonInt"]

    # Only contains values for the relevant "type" (anime/manga)
    episodes = media["episodes"]
    episode_duration = media["duration"]
    chapters = media["chapters"]
    volumes = media["volumes"]

    country_of_origin = media["countryOfOrigin"]
    is_licensed = media["isLicensed"]
    source = media["source"]
    hashtag = media["hashtag"]
    trailer_id = media["trailer"]["id"] if media["trailer"] is not None else None
    updated_at = media["updatedAt"]

    # The cover images of the media
    cover_image_extra_large = media["coverImage"]["extraLarge"]
    cover_image_large = media["coverImage"]["large"]
    cover_image_medium = media["coverImage"]["medium"]
    cover_image_color = media["coverImage"]["color"]

    banner_image = media["bannerImage"]
    average_score = media["averageScore"]
    mean_score = media["meanScore"]
    popularity = media["popularity"]
    favourites = media["favourites"]
    is_adult = media["isAdult"]
    site_url = media["siteUrl"]
    mod_notes = media["modNotes"]

    # get rows for all the tables we want to make
    media_tuple = [id, title_romanji, title_english, title_native,
                   type, format, status, fr'{description}', start_date, end_date, season, season_year, season_int,
                   episodes, episode_duration, chapters, volumes,
                   country_of_origin, is_licensed, source, hashtag, trailer_id, updated_at,
                   cover_image_extra_large, cover_image_large, cover_image_medium, cover_image_color,
                   banner_image, average_score, mean_score, popularity, favourites, is_adult, site_url, mod_notes]

    media_title_synonyms_tuples = [[media_id, synonym] for synonym in media["synonyms"]]
    media_genres_tuples = [[media_id, genre] for genre in media["genres"]]

    character_cast_tuples = [[edge["id"], media_id, edge["node"]["id"], edge["name"], edge["role"]] for edge in
                             media["characters"]["edges"]]

    character_cast_voice_tuples = flatten(
        [[[edge["id"], voice["voiceActor"]["id"], voice["roleNotes"], voice["dubGroup"]]
          for voice in edge["voiceActorRoles"]]
         for edge in media["characters"]["edges"]])

    studio_connection_tuples = [[edge["node"]["id"], media_id, edge["isMain"]] for edge in media["studios"]["edges"]]
    media_relation_tuples = [[media_id, edge["node"]["id"], edge["relationType"]] for edge in media["relations"]["edges"]]
    media_tag_connection_tuples = [[media_id, tag["id"], tag["rank"], tag["isMediaSpoiler"]] for tag in media["tags"]]
    staff_connection_tuples = [[edge["node"]["id"], media_id, edge["role"]] for edge in media["staff"]["edges"]]

    # return all the rows we want
    return media_tuple, media_title_synonyms_tuples, media_genres_tuples, character_cast_tuples, \
        character_cast_voice_tuples, studio_connection_tuples, media_relation_tuples, \
        media_tag_connection_tuples, staff_connection_tuples


def get_media_table():
    media_ids = pd.read_csv("../scrapedData/media_ids.csv", header=None, names=(['id']))

    for media_id in media_ids["id"]:
        print(media_id)

        media_tuple, media_title_synonyms_tuples, media_genres_tuples, character_cast_tuples, \
            character_cast_voice_tuples, studio_connection_tuples, media_relation_tuples, \
            media_tag_connection_tuples, staff_connection_tuples = get_media(int(media_id))

        # write rows to the corresponding tables
        write_row_to_csv("../tables/media.csv", media_tuple)
        write_rows_to_csv("../tables/media_title_synonyms.csv", media_title_synonyms_tuples)
        write_rows_to_csv("../tables/media_genres.csv", media_genres_tuples)
        write_rows_to_csv("../tables/character_cast.csv", character_cast_tuples)
        write_rows_to_csv("../tables/character_cast_voice.csv", character_cast_voice_tuples)
        write_rows_to_csv("../tables/studio_connection.csv", studio_connection_tuples)
        write_rows_to_csv("../tables/media_relation.csv", media_relation_tuples)
        write_rows_to_csv("../tables/media_tag_connection.csv", media_tag_connection_tuples)
        write_rows_to_csv("../tables/staff_connection.csv", staff_connection_tuples)


# uncomment to run file
# get_media_table()
print("done")



