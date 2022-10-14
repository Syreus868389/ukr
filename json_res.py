from pkgutil import iter_modules
from newsdataapi import NewsDataApiClient
import json

api = NewsDataApiClient(apikey="pub_1144217d205b7486109686d1f2de4d2fffe8e")

response = api.news_api(language="fr,en", q="ukraine")

with open('json_data.json', 'w') as outfile:
    json.dump(response, outfile, indent=4)

print(response["nextPage"])

