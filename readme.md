# News analysis regarding Strikes in Germany

Content aka. TL;DR:

1. Collect news articles regarding the keyword "Streik" (English strike) with AWS Lambda function.
2. Prepare the data
3. Analysis Storytelling

## Webscraping news articles on AWS

This project uses the the the REST API of [News API](https://newsapi.org/) by implementing the request library. Sample outputs can be found on the website. A paging functionality is used to receive all (maximal) 500 articles. A seperate method is used to process the raw data.
After that the articles are stored in a local PostgreSQL database via Pandas' interface.

The whole pipeline is executed automatically once a day as you can see in the [cronjob](etc/cronjob.txt). Through limiting the results there should be no duplicates. This should be tested during the data analytics phase. The postgres database and the python script are run on a ec2 instance on AWS.

## Data Analysis

This phase includes data validation, data cleaning, optional data augmentation, exploratory data analysis.

The location of the news article is received from the stored text if possible. Location data is cleaned by cross-checking it against the (countries-states-cities-database)[https://github.com/dr5hn/countries-states-cities-database].

## Storytelling with data

Show interesting facts that can be derived from the data
