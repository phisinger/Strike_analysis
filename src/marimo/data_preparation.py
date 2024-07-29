import marimo

__generated_with = "0.7.12"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import pandas as pd
    import plotly.express as px
    return mo, pd, px


@app.cell
def __(pd):
    # import data
    raw_data = pd.read_json("./data/dynamodb_data.json")
    raw_data["publishedAt"] = pd.to_datetime(raw_data["publishedAt"])
    return raw_data,


@app.cell
def __(px, raw_data):
    data_c_year = raw_data[raw_data["publishedAt"].apply(lambda x: x.year) > 2020]
    px.histogram(data_frame=data_c_year, x="publishedAt")
    return data_c_year,


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
