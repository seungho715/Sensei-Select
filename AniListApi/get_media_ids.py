from helper import *
from queries import *
import pandas as pd


# ====================
#
# This file uses the following list of users to gather media ids.  It does
# so by first gathering all the media in the user's anime/manga list, then
# recursively gathers all directly and indirectly related media ids as
# well
#
#  ** uncomment the last line first to run this file
#
# ====================


# R4D777    5981030
# alex      5454172
# Jokertyf  5838827
# KayosXD   6172856
list_of_users = [5981030, 5454172, 5838827, 6172856]


def collect_user_lists(users):
    visited = set()

    # include data already gathered
    media_ids = pd.read_csv("../scrapedData/media_ids.csv", header=None, names=(['id']))
    for media_id in media_ids["id"]:
        visited.add(media_id)

    # get data for each user
    for user in users:
        print(f'User: {user}')
        anime_query = media_list_query(user, "ANIME")
        manga_query = media_list_query(user, "MANGA")

        anime_list = retrieve_data(anime_query)
        manga_list = retrieve_data(manga_query)

        entries = anime_list["data"]["MediaListCollection"]["lists"] + \
                  manga_list["data"]["MediaListCollection"]["lists"]

        for entry in entries:
            print(f"\tentry")
            for media in entry["entries"]:
                visit_media(media["media"], visited)

    return visited


def visit_media(media, visited):
    media_id = media["id"]
    if media_id in visited:
        return

    visited.add(media_id)
    write_row_to_csv("../scrapeddata/media_ids.csv", [media_id])

    # get list of children media
    children_media = set()
    for relation in media["relations"]["edges"]:
        related_media_id = relation["node"]["id"]
        children_media.add(related_media_id)

    # visit children media
    for child_id in children_media:
        if child_id not in visited:
            query = media_info_query(child_id)
            data = retrieve_data(query)
            child = data["data"]["Media"]
            visit_media(child, visited)


# uncomment to run file
# collect_user_lists(list_of_users)
print("done")
