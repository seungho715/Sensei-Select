import pandas as pd
from queries import *
from helper import *

alex_id = 5454172


def get_user_data(user_id):
    query = user_query(user_id)
    data = retrieve_data(query)
    user = data["data"]["User"]

    user_tuple = (user["id"], user["name"], user["about"],

                  user["avatar"]["large"], user["avatar"]["medium"], user["bannerImage"],

                  user["options"]["titleLanguage"], user["options"]["displayAdultContent"],
                  user["options"]["airingNotifications"], user["options"]["profileColor"],
                  user["options"]["staffNameLanguage"],

                  user["mediaListOptions"]["scoreFormat"],
                  user["siteUrl"],
                  user["createdAt"], user["updatedAt"],

                  user["statistics"]["anime"]["count"], user["statistics"]["anime"]["meanScore"],
                  user["statistics"]["anime"]["standardDeviation"], user["statistics"]["anime"]["minutesWatched"],
                  user["statistics"]["anime"]["episodesWatched"],

                  user["statistics"]["manga"]["count"], user["statistics"]["manga"]["meanScore"],
                  user["statistics"]["manga"]["standardDeviation"], user["statistics"]["manga"]["chaptersRead"],
                  user["statistics"]["manga"]["volumesRead"],
                  )

    write_row_to_csv("../tables/user.csv", user_tuple)


def get_user_table():
    user_ids = pd.read_csv("../scrapeddata/user_ids.csv", header=None, names=(['id']))["id"]
    visited = set(pd.read_csv("../tables/user.csv")["id"].unique()).union(
              set(pd.read_csv("../scrapeddata/failed_user_ids.csv", header=None, names=(['id']))["id"].unique()))

    count = 0
    for user_id in user_ids:
        count += 1
        progress_count(count, len(user_ids))

        if user_id in visited:
            continue

        try:
            get_user_data(user_id)
        except:
            failed_user_ids.append(user_id)
            write_row_to_csv("../scrapeddata/failed_user_ids.csv", [user_id])

        visited.add(user_id)


failed_user_ids = []

# get_user_data(alex_id)
get_user_table()
print(f"Failed ids: {failed_user_ids}")
print("done")







