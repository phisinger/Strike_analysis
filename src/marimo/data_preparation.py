import marimo

__generated_with = "0.7.12"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import pandas as pd
    import plotly.express as px
    import spacy
    nlp = spacy.load("de_core_news_sm")
    from collections import Counter
    return Counter, mo, nlp, pd, px, spacy


@app.cell
def __(pd):
    # import data
    raw_data = pd.read_json("./data/dynamodb_data.json", encoding="utf-8")
    raw_data["publishedAt"] = pd.to_datetime(raw_data["publishedAt"])
    return raw_data,


@app.cell
def __(px, raw_data):
    # Remove entry with wrong date
    data_c_year = raw_data[raw_data["publishedAt"].apply(lambda x: x.year) > 2020]
    px.histogram(data_frame=data_c_year, x="publishedAt")
    return data_c_year,


@app.cell
def __(data_c_year):
    # Fill missing description with empty string
    data_f_description = data_c_year.fillna(value="")
    # Fill missing author with source
    data_f_author = data_f_description.copy()
    data_f_author["author"] = [author if author  else source for author, source in zip(data_f_author["author"], data_f_author["source"])]
    # Drop missing title entries
    data_d_title = data_f_author.dropna(subset="title")
    return data_d_title, data_f_author, data_f_description


@app.cell
def __(data_d_title):
    # Encode/Decode unicodes for German characters
    data_c_unicode = data_d_title.copy()
    # for col in ["content", "source", "description", "author", "title"]:
    #     data_c_unicode[col] = data_c_unicode[col].apply(lambda t: t.encode().decode('unicode_escape'))
    return data_c_unicode,


@app.cell
def __(data_c_unicode, nlp):
    # Extract author if possible
    data_c_author = data_c_unicode.copy()
    clean_author_list = []
    for au in data_c_author["author"]:
        clean_author_list.append([ent.text for ent in nlp(au).ents if ent.label_ == "PER"])
    data_c_author["author_clean"] = clean_author_list
    return au, clean_author_list, data_c_author


@app.cell
def __(data_c_author):
    data_c_author.describe()
    return


@app.cell
def __(data_c_author):
    # Merge all text into one column (title, description, content)
    data_c_text = data_c_author.copy()
    data_c_text["text"] = data_c_text["title"] + " \n" + data_c_text["description"] + " \n" + data_c_text["content"]
    return data_c_text,


@app.cell
def __(data_c_text):
    data_c_columns = data_c_text.copy()
    data_c_columns = data_c_columns.drop(columns=["content", "title", "description"])
    return data_c_columns,


@app.cell
def __(data_c_columns):
    data_c_columns.head()
    return


@app.cell
def __(data_c_columns, nlp):
    # Derive location from text
    data_c_columns["location"] = data_c_columns["text"].apply(lambda txt: [ent.text for ent in nlp(txt).ents if ent.label_ == "LOC"])


    return


@app.cell
def __(pd):
    # Cross check the extracted locations

    # Construct a list of proven locations form the database csv
    loc_df = pd.read_csv("data/cities.csv")
    master_loc_list = set([str(city).lower() for city in loc_df["name"].to_list()])
    for col in ["state_name", "country_name"]:
        geo_list = [str(geo).lower() for geo in loc_df[col].drop_duplicates().to_list()]
        for ele in geo_list:
            try:
                master_loc_list.add(ele)
            except:
                print(f"error with {ele} in column {col}")
                continue

    print(master_loc_list)

     
    return col, ele, geo_list, loc_df, master_loc_list


@app.cell
def __(Counter, data_c_columns, master_loc_list):
    def clean_location(loc_list:list):
        if loc_list != []:
            #lower entries
            low_loc_list = [str(element).lower() for element in loc_list]

            # replace Hollywood
            low_loc_list = ["los angeles" if loc == "hollywood" else loc for loc in low_loc_list ]

            # clean elements that are not cities, states, countries or continents
            check_loc_list = []
            for loc in low_loc_list:
                if loc in master_loc_list:
                    check_loc_list.append(loc)

            if check_loc_list == []:
                return ""
            
            #find the most common element in the list and return this
            loc_counter = Counter(check_loc_list)
            return loc_counter.most_common()[0][0]
        else:
            return ""

        
    data_c_location = data_c_columns.copy()
    data_c_location["location"] = data_c_columns["location"].apply(clean_location)
    return clean_location, data_c_location


@app.cell
def __(data_c_location):
    data_c_location["location"].value_counts().head(10)
    return


@app.cell
def __(data_c_location):
    data_c_location.to_json("data/data_prepared.json", orient="index")
    return


@app.cell
def __():
    return


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
