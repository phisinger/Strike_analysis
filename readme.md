# News analysis regarding Strikes in Germany

Content aka. TL;DR:

1. Collect news articles regarding the keyword "Streik" (English strike) with Python data pipeline.
2. Analyse this data
3. Predict next strikes

## Webscraping news articles and storing them in Postgres DB

This project uses the the the REST API of [News API](https://newsapi.org/) by implementing the request library. Sample outputs can be found on the website. A paging functionality is used to receive all (maximal) 500 articles. A seperate method is used to process the raw data.
After that the articles are stored in a local PostgreSQL database via Pandas' interface.

The whole pipeline is executed automatically once a day as you can see in the [cronjob](etc/cronjob.txt). Through limiting the results there should be no duplicates. This should be tested during the data analytics phase. The postgres database and the python script are run on a ec2 instance on AWS.

## Data Analysis

This part of the project will follow once, there is enough data received.

This phase includes data validation, data cleaning, optional data augmentation, exploratory data analysis, focused Storytelling with data

## Prediction

Depending on the results of the Data Analytics phase and the general data quality this phase will include data modelling for prediction. Probably it will include components of time series forecasting.
