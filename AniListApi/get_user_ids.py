import pandas as pd
from queries import *
from helper import *


def get_user_ids():
    visited = set(pd.read_csv("../scrapeddata/user_ids.csv", header=None, names=(['id']))["id"].unique())
    count = len(visited)

    while True:
        query = user_collecting_query()
        data = retrieve_data(query)
        users = data["data"]["Page"]["users"]

        for user in users:
            user_id = user["id"]
            if user_id in visited:
                continue

            stats = user["statistics"]["anime"]
            if stats["count"] == 0 or stats["episodesWatched"] == 0 or stats["minutesWatched"] == 0:
                continue

            count += 1
            visited.add(user_id)
            write_row_to_csv("../scrapeddata/user_ids.csv", [user_id])

            progress_count(count, 0)


# will run until you manually stop it
print("Starting...")
get_user_ids()

