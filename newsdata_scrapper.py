from pkgutil import iter_modules
from newsdataapi import NewsDataApiClient
import json
import urllib.parse
import spacy
from functions import *

nlp = spacy.load("en_core_web_sm")

query = "ukraine"



# API key authorization, Initialize the client with your API key

api = NewsDataApiClient(apikey="pub_1144217d205b7486109686d1f2de4d2fffe8e")

titles = []
responses = []

response = api_call(api, query, 0)
responses.append(response)

title_maker(response, titles)

total_res = response["totalResults"]
total_pages = round_down_to_nearest_10(total_res)
i = 1

while i < total_pages:
    response = api_call(api, query, i)
    responses.append(response)
    title_maker(response, titles)
    i += 1

with open('json_data.json', 'w', encoding='utf-8') as outfile:
    json.dump(response, outfile, indent=4)

print(titles)

#for title in titles:
#    doc = nlp(title)
#    for token in doc:
#        print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
#                token.shape_, token.is_alpha, token.is_stop)

