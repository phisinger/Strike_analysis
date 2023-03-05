import json
import os
from datetime import datetime, timedelta
import requests
from typing import List
import math
import pandas as pd
from sqlalchemy import create_engine


class Webscraping():

    def __init__(self) -> None:
        # read api key
        json_file = open("keys/newsapi.json", "r")
        self.api_key = json.load(json_file)["api_key"]
        self.session = requests.Session()

    def request_articles(self):
        # calculate date filter
        from_date = (datetime.now() - timedelta(days=2)
                     ).strftime("%Y-%m-%dT%H:%M:%S")

        search_params = {
            "apiKey": self.api_key,
            "q": "Streik",
            "from": from_date,
            "language": "de"
        }

        try:
            # API request
            url = "https://newsapi.org/v2/everything"
            response_raw = self.session.get(url, params=search_params)

            first_page = response_raw.json()

            yield first_page
            print("Successful API response at ", datetime.now())
            num_pages = math.ceil(first_page["totalResults"]/100)

            # On this API level max 5 pages are allowed
            if num_pages > 5:
                num_pages = 5

            for page in range(2, num_pages+1):
                search_params["page"] = page
                next_page_raw = self.session.get(url, params=search_params)
                yield next_page_raw.json()

        except:
            print("Failed API response at ", datetime.now())
            print("error code: ", response_raw.status_code)

            # send email
            send_email(response_raw.status_code)

            yield None


def process_page(page: dict) -> pd.DataFrame:

    articles = page["articles"]

    for article_index in range(0, len(articles)):
        articles[article_index]["source"] = articles[article_index]["source"]["name"]

    df = pd.read_json(json.dumps(articles))

    return df


def send_email(error: int) -> None:
    # ...
    print("email sent")
    return


def store_db(df: pd.DataFrame):
    # postgres connection parameters
    pg_cred = json.load(open("keys/postgresql.json", "r"))
    db_url = "postgresql://" + pg_cred["user"] + ":" + pg_cred["pw"] + \
        "@" + pg_cred["host"] + ":" + \
        pg_cred["port"] + "/" + pg_cred["database"]

    conn = create_engine(db_url)
    try:
        df.to_sql(pg_cred["table_name"], con=conn,
                  if_exists="append", index=False)
        return
    except Exception as e:
        print("one exception occured during storing to database:", e)


if __name__ == "__main__":
    scraper = Webscraping()

    articles_df = pd.DataFrame()

    for page in scraper.request_articles():
        if page:
            # process page
            temp_df = process_page(page)

            # print(temp_df.head())
            articles_df = pd.concat([articles_df, temp_df])
        else:
            break

    print(articles_df.shape)
    store_db(articles_df)
