from helper import *
from queries import *
import pandas as pd


def get_media_stats(media_id):
    query = media_stats_query(media_id)
    data = retrieve_data(query)
    score_distribution, status_distribution = \
        data["data"]["Media"]["stats"]["scoreDistribution"], data["data"]["Media"]["stats"]["statusDistribution"]

    return score_distribution, status_distribution


def get_media_stats_table():
    media_ids = pd.read_csv("../scrapedData/media_ids.csv", header=None, names=(['id']))
    visited = set(pd.read_csv("../tables/media_scores.csv")["media_id"].unique()).union(
              set(pd.read_csv("../tables/media_statuses.csv")["media_id"].unique()))

    count = 0
    for media_id in media_ids["id"]:
        count += 1
        progress_count(count, len(media_ids["id"]))

        if media_id in visited:
            continue

        try:
            score_distribution, status_distribution = get_media_stats(media_id)
        except:
            failed_media_ids.append(media_id)
            continue

        # write scores
        for score in score_distribution:
            write_row_to_csv("../tables/media_scores.csv", [media_id, score["score"], score["amount"]])

        # write statuses
        for status in status_distribution:
            write_row_to_csv("../tables/media_statuses.csv", [media_id, status["status"], status["amount"]])

        visited.add(media_id)


failed_media_ids = []

print("Getting Media_Scores and Media Statuses Tables")
get_media_stats_table()
print(f"Failed ids: {failed_media_ids}")
print("done\n")


# removing duplicates that got in the score and status tables somehow

scores = pd.read_csv("../tables/media_scores.csv")
statuses = pd.read_csv("../tables/media_statuses.csv")

scores.drop_duplicates(keep="first", inplace=True)
statuses.drop_duplicates(keep="first", inplace=True)


# add in 0 values for scores and statuses that don't have values for certain media

media_ids = pd.read_csv("../scrapedData/media_ids.csv", header=None, names=(['id']))

score_values = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
status_values = ["CURRENT", "PLANNING", "COMPLETED", "DROPPED", "PAUSED"]

for media_id in media_ids['id']:
    for score in score_values:
        if not ((scores['media_id'] == media_id) & (scores['score'] == score)).any():
            new_row = pd.Series({'media_id': media_id, 'score': score, 'amount': 0})
            scores = pd.concat([scores, new_row.to_frame().T], ignore_index=True)

    for status in status_values:
        if not ((statuses['media_id'] == media_id) & (statuses['status'] == status)).any():
            new_row = pd.Series({'media_id': media_id, 'status': status, 'amount': 0})
            statuses = pd.concat([statuses, new_row.to_frame().T], ignore_index=True)


# check that lengths are what they are supposed to be
print(f'num_media:       {len(media_ids)}')
print(f'num_scores/10:   {len(scores["media_id"]) / 10}')
print(f'num_statuses/5:  {len(statuses["media_id"]) / 5}')


# save data to csv
scores.to_csv("../tables/media_scores.csv", index=False, header=True)
statuses.to_csv("../tables/media_statuses.csv", index=False, header=True)


# check that counts are what they should be
for media_id in media_ids["id"]:
    if len(scores.loc[scores['media_id'] == media_id]) != 10:
        print("FAIL")

    if len(statuses.loc[statuses['media_id'] == media_id]) != 5:
        print("FAIL")



