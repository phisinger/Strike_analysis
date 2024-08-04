import json
import os
from datetime import datetime, timedelta
import requests
import math
import pandas as pd
from postgres_conn import store_db
from send_emails import send_email


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

        response_raw = requests.Response()

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


    def process_page(self, page: dict) -> pd.DataFrame:

        articles = page["articles"]

        for article_index in range(0, len(articles)):
            articles[article_index]["source"] = articles[article_index]["source"]["name"]

        df = pd.read_json(json.dumps(articles))

        return df








if __name__ == "__main__":
    scraper = Webscraping()

    articles_df = pd.DataFrame()

    for page in scraper.request_articles():
        if page:
            # process page
            temp_df = scraper.process_page(page)

            # print(temp_df.head())
            articles_df = pd.concat([articles_df, temp_df])
        else:
            break

    print(articles_df.shape)
    store_db(articles_df)
