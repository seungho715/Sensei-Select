from helper import *
from queries import *
import pandas as pd

# tables:
# Media_List, Media_List_Entry, Media_List_Group

# alex      5454172
user = 5454172


def get_user_list(user_id):
    anime_query = meda_list_detail_query(user, "ANIME")
    manga_query = meda_list_detail_query(user, "MANGA")

    failed = 0

    try:
        anime_list = retrieve_data(anime_query, sleep_time=2)["data"]["MediaListCollection"]["lists"]
        anime_list = [anime for sublist in anime_list for anime in sublist["entries"]]

        for anime in anime_list:
            entry = (user_id, anime["media"]["id"], anime["status"], anime["score"], anime["progress"], anime["progressVolumes"],
                     anime["repeat"], anime["priority"], anime["private"], anime["notes"],
                     f'{anime["startedAt"]["year"]}-{anime["startedAt"]["month"]}-{anime["startedAt"]["day"]}',
                     f'{anime["completedAt"]["year"]}-{anime["completedAt"]["month"]}-{anime["completedAt"]["day"]}',
                     anime["updatedAt"], anime["createdAt"])
            write_row_to_csv("../tables/media_list_entry.csv", entry)
    except:
        failed += 1

    try:
        manga_list = retrieve_data(manga_query, sleep_time=2)["data"]["MediaListCollection"]["lists"]
        manga_list = [manga for sublist in manga_list for manga in sublist["entries"]]

        for manga in manga_list:
            entry = (user_id, manga["media"]["id"], manga["status"], manga["score"], manga["progress"], manga["progressVolumes"],
                     manga["repeat"], manga["priority"], manga["private"], manga["notes"],
                     f'{manga["startedAt"]["year"]}-{manga["startedAt"]["month"]}-{manga["startedAt"]["day"]}',
                     f'{manga["completedAt"]["year"]}-{manga["completedAt"]["month"]}-{manga["completedAt"]["day"]}',
                     manga["updatedAt"], manga["createdAt"])
            write_row_to_csv("../tables/media_list_entry.csv", entry)
    except:
        failed += 1

    if failed >= 2:
        raise Exception("Both lists failed")


def get_user_lists():
    user_ids = pd.read_csv("../scrapeddata/user_ids.csv", header=None, names=(['id']))["id"]
    visited = set(pd.read_csv("../tables/media_list_entry.csv")["account_id"].unique()).union(
              set(pd.read_csv("../scrapeddata/failed_user_ids.csv", header=None, names=(['id']))["id"].unique()))

    count = 0
    for user_id in user_ids:
        count += 1
        progress_count(count, len(user_ids))

        if user_id in visited:
            continue

        try:
            get_user_list(user_id)
        except:
            failed_user_ids.append(user_id)
            write_row_to_csv("../scrapeddata/failed_user_ids.csv", [user_id])
            continue

        visited.add(user_id)


failed_user_ids = []

# collect_user_list(user, account_id)
# get_user_list(6253653)
get_user_lists()
print(f"Failed ids: {failed_user_ids}")
print("done")

