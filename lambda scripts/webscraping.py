import json
import os
from datetime import datetime, timedelta
import requests
import math


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

        # response_raw = requests.Response()

        # API request
        url = "https://newsapi.org/v2/everything"
        response_raw = self.session.get(url, params=search_params)

        first_page = response_raw.json()

        yield first_page
        # print("Successful API response at ", datetime.now())
        num_pages = math.ceil(first_page["totalResults"]/100)

        # On this API level max 5 pages are allowed
        if num_pages > 5:
            num_pages = 5

        for page in range(2, num_pages+1):
            search_params["page"] = page
            next_page_raw = self.session.get(url, params=search_params)
            yield next_page_raw.json()

    def process_page(self, page: dict) -> dict:

        articles = page["articles"]

        for article_index in range(0, len(articles)):
            articles[article_index]["source"] = articles[article_index]["source"]["name"]

        return articles
