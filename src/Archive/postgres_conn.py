import pandas as pd
import json
from sqlalchemy import create_engine


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
        print("one exception occured during storing to database:", e, )
