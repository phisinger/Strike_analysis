import marimo

__generated_with = "0.7.12"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import pandas as pd
    import plotly.express as px
    from ydata_profiling import ProfileReport
    return ProfileReport, mo, pd, px


@app.cell
def __(mo):
    mo.md("""# Exploratory Data Analysis""")
    return


@app.cell
def __(pd):
    # import data
    raw_data = pd.read_json("./data/dynamodb_data.json")
    raw_data["publishedAt"] = pd.to_datetime(raw_data["publishedAt"])
    return raw_data,


@app.cell
def __(raw_data):
    raw_data.head(15)
    return


@app.cell
def __(ProfileReport, raw_data):
    # Create Report for initial EDA
    report = ProfileReport(raw_data, title="Initial EDA")
    report.to_file("reports/initial_eda.html")
    return report,


@app.cell
def __(px, raw_data):
    # Assess 'publishedAt' column regarding date
    px.histogram(data_frame=raw_data, x="publishedAt", title="Histogram publishing dates of articles")
    return


@app.cell
def __(px, raw_data):
    # Assess "publishedAt" column regarding time
    raw_data_copy = raw_data.copy()
    raw_data_copy["publishedAt_time"] = raw_data_copy["publishedAt"].apply(lambda x: int(x.strftime("%H")))
    px.histogram(data_frame=raw_data_copy, x="publishedAt_time", title="Histogramm which hour the articles are published in")
    return raw_data_copy,


@app.cell
def __(raw_data):
    raw_data[raw_data["publishedAt"].apply(lambda x: x.year) < 2020]
    return


@app.cell
def __(px, raw_data):
    # Assess 'source' column
    px.histogram(data_frame=raw_data, y="source", title="Histogram sources", height=1800).update_yaxes(categoryorder="total ascending")
    return


@app.cell
def __(px, raw_data):
    # Assess 'author' column
    px.histogram(data_frame=raw_data, y="author", title="Histogram author", height=1800).update_yaxes(categoryorder="total ascending")
    return


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
