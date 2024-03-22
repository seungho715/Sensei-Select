import pandas as pd
from queries import *
from helper import *


# ====================
#
# This file scrapes the following tables from the following lists of ids:
#  TABLE_NAME                   FROM
#   Media_Tag                    "media_tag_ids.csv"
#
#   Staff                        "staff_ids.csv"
#   Staff_Occupations            "staff_ids.csv"
#   Staff_Name_Alternatives      "staff_ids.csv"
#
#   Character                    "character_ids.csv"
#   Character_Name_Alternatives  "character_ids.csv"
#
#   Studio                       "studio_ids.csv"
#
#   Genre                         N/A
#
#
#  ** uncomment the last few lines first to run this file
#
# ====================


def get_media_tag_table():
    query = media_tag_collection_query()
    data = retrieve_data(query)
    media_tags = data["data"]["MediaTagCollection"]

    for media_tag in media_tags:
        media_tag_tuple = [media_tag["id"], media_tag["name"], media_tag["description"],
                           media_tag["category"], media_tag["isGeneralSpoiler"], media_tag["isAdult"]]

        write_row_to_csv("../tables/Media_Tag.csv", media_tag_tuple)


def get_staff(staff_id):
    query = staff_info_query(staff_id)
    data = retrieve_data(query)
    staff = data["data"]["Staff"]

    id = staff["id"]

    name_first = staff["name"]["first"]
    name_middle = staff["name"]["middle"]
    name_last = staff["name"]["last"]
    name_full = staff["name"]["full"]
    name_native = staff["name"]["native"]

    language = staff["languageV2"]

    image_large = staff["image"]["large"]
    image_medium = staff["image"]["medium"]

    description = staff["description"]
    gender = staff["gender"]
    date_of_birth = f'{staff["dateOfBirth"]["year"]}-{staff["dateOfBirth"]["month"]}-{staff["dateOfBirth"]["day"]}'
    date_of_death = f'{staff["dateOfDeath"]["year"]}-{staff["dateOfDeath"]["month"]}-{staff["dateOfDeath"]["day"]}'
    active_from = staff["yearsActive"][0] if 0 < len(staff["yearsActive"]) else None
    active_to = staff["yearsActive"][1] if 1 < len(staff["yearsActive"]) else None
    home_town = staff["homeTown"]
    blood_type = staff["bloodType"]
    site_url = staff["siteUrl"]
    favorites = staff["favourites"]
    mod_notes = staff["modNotes"]

    # get rows for all the tables we want to make
    staff_tuple = [id, name_first, name_middle, name_last, name_full, name_native,
                   language, image_large, image_medium, description, gender,
                   date_of_birth, date_of_death, active_from, active_to, home_town,
                   blood_type, site_url, favorites, mod_notes]

    staff_occupation_tuples = [[id, occupation] for occupation in staff["primaryOccupations"]]
    staff_name_alternative_tuples = [[id, name] for name in staff["name"]["alternative"]]

    return staff_tuple, staff_occupation_tuples, staff_name_alternative_tuples


def get_staff_table():
    staff_ids = pd.read_csv("../scrapedData/staff_ids.csv", header=None, names=(['id']))
    visited = set(pd.read_csv("../tables/staff.csv")["id"])

    count = 0
    for staff_id in staff_ids["id"]:
        count += 1
        progress_count(count, len(staff_ids["id"]))

        # skip staff we already have data for
        if staff_id in visited:
            continue

        # some staff ids don't have data for some reason
        try:
            staff_tuple, staff_occupation_tuples, staff_name_alternative_tuples = get_staff(staff_id)
        except:
            failed_staff_ids.append(staff_id)
            continue

        # write rows to the corresponding tables
        write_row_to_csv("../tables/staff.csv", staff_tuple)
        write_rows_to_csv("../tables/staff_occupations.csv", staff_occupation_tuples)
        write_rows_to_csv("../tables/staff_name_alternatives.csv", staff_name_alternative_tuples)


def get_character(character_id):
    query = character_info_query(character_id)
    data = retrieve_data(query)
    character = data["data"]["Character"]

    id = character["id"]

    name_first = character["name"]["first"]
    name_middle = character["name"]["middle"]
    name_last = character["name"]["last"]
    name_full = character["name"]["full"]
    name_native = character["name"]["native"]

    image_large = character["image"]["large"]
    image_medium = character["image"]["medium"]

    description = character["description"]
    gender = character["gender"]
    date_of_birth = f'{character["dateOfBirth"]["year"]}-{character["dateOfBirth"]["month"]}-{character["dateOfBirth"]["day"]}'
    age = character["age"]
    blood_type = character["bloodType"]
    site_url = character["siteUrl"]
    favorites = character["favourites"]
    mod_notes = character["modNotes"]

    # get rows for all the tables we want to make
    character_tuple = [id, name_first, name_middle, name_last, name_full, name_native,
                       image_large, image_medium, description, gender, date_of_birth, age,
                       blood_type, site_url, favorites, mod_notes]
    character_name_alternative_tuples = [[id, name, "False"] for name in character["name"]["alternative"]] + \
                                        [[id, name, "True"] for name in character["name"]["alternativeSpoiler"]]

    return character_tuple, character_name_alternative_tuples


def get_character_table():
    character_ids = pd.read_csv("../scrapedData/character_ids.csv", header=None, names=(['id']))
    visited = set(pd.read_csv("../tables/character.csv")["id"])

    count = 0
    for character_id in character_ids["id"]:
        count += 1
        progress_count(count, len(character_ids["id"]))

        # skip staff we already have data for
        if character_id in visited:
            continue

        # some character ids don't have data for some reason
        try:
            character_tuple, character_name_alternative_tuples = get_character(character_id)
        except:
            failed_character_ids.append(character_id)
            continue

        # write rows to the corresponding tables
        write_row_to_csv("../tables/character.csv", character_tuple)
        write_rows_to_csv("../tables/character_name_alternatives.csv", character_name_alternative_tuples)


def get_studio(studio_id):
    query = studio_query(studio_id)
    data = retrieve_data(query)
    character = data["data"]["Studio"]

    id = character["id"]
    name = character["name"]
    is_animation_studio = character["isAnimationStudio"]
    site_url = character["siteUrl"]
    favourites = character["favourites"]

    studio_tuple = [id, name, is_animation_studio, site_url, favourites]
    return studio_tuple

def get_studio_table():
    studio_ids = pd.read_csv("../scrapedData/studio_ids.csv", header=None, names=(['id']))
    visited = set(pd.read_csv("../tables/studio.csv")["id"])

    count = 0
    for studio_id in studio_ids["id"]:
        count += 1
        progress_count(count, len(studio_ids["id"]))

        # skip staff we already have data for
        if studio_id in visited:
            continue

        # some studio ids don't have data for some reason
        try:
            studio_tuple = get_studio(studio_id)
        except:
            failed_studio_ids.append(studio_id)
            continue

        # write rows to the corresponding tables
        write_row_to_csv("../tables/studio.csv", studio_tuple)


def get_genre_table():
    query = genre_collection_query()
    data = retrieve_data(query)
    media_genres = data["data"]["GenreCollection"]

    df = pd.DataFrame(media_genres)
    df.index += 1
    df.to_csv("../tables/genre.csv", index=True, header=["name"], index_label="id")


failed_staff_ids = []
failed_character_ids = []
failed_studio_ids = []

print("Getting Media_Tag Table")
# get_media_tag_table()
print("done\n")


print("Getting Staff Table")
# get_staff_table()
print(f"Failed ids: {failed_staff_ids}")
print("done\n")


print("Getting Character Table")
# get_character_table()
print(f"Failed ids: {failed_character_ids}")
print("done\n")


print("Getting Studio Table")
# get_studio_table()
print(f"Failed ids: {failed_studio_ids}")
print("done\n")


print("Getting Media_Genre Table")
# get_genre_table()
print("done\n")


# removing duplicates that got in the character table somehow

# staff = pd.read_csv("../tables/staff.csv")
# character = pd.read_csv("../tables/character.csv")
# character.drop_duplicates(subset="id", keep="first", inplace=True)
#
# print(len(staff["id"]))
#
# character.to_csv("../tables/character.csv", index=False, header=True)
#
# print(len(character["id"]))
# print(len(character["id"].unique()))




