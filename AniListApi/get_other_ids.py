import pandas as pd


# ====================
#
# This file gets the list of ids for the following tables from the following tables
#  TABLE_NAME       FROM
#   Media_Tag        Media_Tag_Connection
#   Staff            Staff_Connection, Character_Cast_Voice
#   Character        Character_Cast
#   Studio           Studio_Connection
#
# ====================


# load data
media_tag_ids = pd.read_csv("../tables/Media_Tag_Connection.csv")["tag_id"].unique()
staff_ids = pd.concat([pd.read_csv("../tables/Staff_Connection.csv")["staff_id"],
                       pd.read_csv("../tables/Character_Cast_Voice.csv")["voice_actor_id"]]).unique()
character_ids = pd.read_csv("../tables/Character_Cast.csv")["character_id"].unique()
studio_ids = pd.read_csv("../tables/Studio_Connection.csv")["studio_id"].unique()


# save to csv files
pd.DataFrame(media_tag_ids).to_csv("../scrapedData/media_tag_ids.csv", index=False, header=False)
pd.DataFrame(staff_ids).to_csv("../scrapedData/staff_ids.csv", index=False, header=False)
pd.DataFrame(character_ids).to_csv("../scrapedData/character_ids.csv", index=False, header=False)
pd.DataFrame(studio_ids).to_csv("../scrapedData/studio_ids.csv", index=False, header=False)


print("done")


