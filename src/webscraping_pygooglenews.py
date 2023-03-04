from pygooglenews import GoogleNews

gn = GoogleNews(lang='de', country='Germany')

results = gn.search(query="Streik",
                    when="1d")

print(results["feed"])
for entry in results['entries']:
    print(entry)
