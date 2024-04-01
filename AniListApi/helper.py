import requests
import csv
import time
import random


def flatten(l):
    return [item for sublist in l for item in sublist]


def write_row_to_csv(path, row):
    with open(path, "a", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerow(row)


def write_rows_to_csv(path, rows):
    with open(path, "a", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=",")
        writer.writerows(rows)


iteration_count = 0
last_refresh = time.time()


def retrieve_data(query, sleep_time=0.75):
    global iteration_count
    global last_refresh

    iteration_count += 1

    # rate limit self to under 90 requests/min
    if iteration_count % 90 == 0 and iteration_count != 0:
        # sleep until the next minute
        time.sleep(max(60 - (time.time() - last_refresh), 0))
        last_refresh = time.time()

    time.sleep(sleep_time + random.uniform(0, sleep_time))  # rate limit self to 80 requests/min

    while True:
        try:
            response = requests.post("https://graphql.anilist.co", data={"query": query}).json()

            if "errors" in response["data"] and response["data"]["errors"][0]["message"] == "Too Many Requests.":
                raise Exception("Too Many Requests.")

            return response
        except:
            time.sleep(60)


def progress_count(current, total):
    ending = '\n' if current == total else ''
    print(f'\rProgress: {current}/{total}', end=ending)


