import pandas as pd
from queries import *
from helper import *

user_id = 5454172


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


# get_user_data(user_id)
print("done")






