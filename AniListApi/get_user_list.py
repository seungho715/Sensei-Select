from helper import *
from queries import *
import pandas as pd

# tables:
# Media_List, Media_List_Entry, Media_List_Group

# alex      5454172
user = 5454172


def get_user_list(user_id):
    print(f'User: {user_id}')
    anime_query = meda_list_detail_query(user, "ANIME")
    manga_query = meda_list_detail_query(user, "MANGA")

    anime_list = retrieve_data(anime_query)["data"]["MediaListCollection"]["lists"]
    anime_list = [anime for sublist in anime_list for anime in sublist["entries"]]

    manga_list = retrieve_data(manga_query)["data"]["MediaListCollection"]["lists"]
    manga_list = [manga for sublist in manga_list for manga in sublist["entries"]]

    for anime in anime_list:
        entry = (user_id, anime["media"]["id"], anime["status"], anime["score"], anime["progress"], anime["progressVolumes"],
                 "", "", "", "", "", "", "", "")
        write_row_to_csv("../tables/media_list_entry.csv", entry)

    for manga in manga_list:
        entry = (user_id, manga["media"]["id"], manga["status"], manga["score"], manga["progress"], manga["progressVolumes"],
                 "", "", "", "", "", "", "", "")
        write_row_to_csv("../tables/media_list_entry.csv", entry)


def get_user_lists():
    user_ids = pd.read_csv("../scrapeddata/user_ids.csv", header=None, names=(['id']))["id"]
    visited = set(pd.read_csv("../tables/media_list_entry.csv")["account_id"].unique())

    count = 0
    for user_id in user_ids:
        count += 1
        progress_count(count, len(user_ids))

        if user_id in visited:
            continue

        get_user_list(user_id)
        visited.add(user_id)


# collect_user_list(user, account_id)
get_user_lists()
print("done")

