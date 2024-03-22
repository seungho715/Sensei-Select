from helper import *
from queries import *
import pandas as pd

# tables:
# Media_List, Media_List_Entry, Media_List_Group

# alex      5454172
user = 5454172
account_id = 2


def collect_user_list(user, account_id):
    print(f'User: {user}')
    anime_query = meda_list_detail_query(user, "ANIME")
    manga_query = meda_list_detail_query(user, "MANGA")

    anime_list = retrieve_data(anime_query)["data"]["MediaListCollection"]["lists"]
    anime_list = [anime for sublist in anime_list for anime in sublist["entries"]]

    manga_list = retrieve_data(manga_query)["data"]["MediaListCollection"]["lists"]
    manga_list = [manga for sublist in manga_list for manga in sublist["entries"]]

    for anime in anime_list:
        entry = (account_id, anime["media"]["id"], anime["status"], anime["score"] * 10, anime["progress"], anime["progressVolumes"],
                 "", "", "", "", "", "", "", "")
        write_row_to_csv("../tables/media_list_entry.csv", entry)

    for manga in manga_list:
        entry = (account_id, manga["media"]["id"], manga["status"], manga["score"] * 10, manga["progress"], manga["progressVolumes"],
                 "", "", "", "", "", "", "", "")
        write_row_to_csv("../tables/media_list_entry.csv", entry)


# collect_user_list(user, account_id)
print("done")

