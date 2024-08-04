import boto3
import json
from webscraping import Webscraping


print('Loading function')
print("boto3 version", boto3.__version__)
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('strike_analyses')


def lambda_handler(event, context):
    scraper = Webscraping()

    for page in scraper.request_articles():
        if page:
            # process page data
            processed_page = scraper.process_page(page)

            # storing into dynamoDB
            with table.batch_writer(overwrite_by_pkeys=["url"]) as batch:
                for article in processed_page:
                    if article["url"] != None:
                        batch.put_item(Item=article)

        else:
            break

    return "success"
