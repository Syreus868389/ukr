import collections
from concurrent.futures import process
import ijson
from functions import *
from spacy_handlers import *
import pandas as pd

# import required module
import os
# assign directory
directory = 'corpus'


counter = 0

clean_wordlist = []
nlp_dict = {}

for filename in os.listdir(directory):
    file = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(file):
        with open(file, "rb") as f:
            for record in ijson.items(f, "item"):
                tweet_txt = record['tweet']
                processed = SpacyHandler(tweet_txt)
                processed.handler()

                for lemma in processed.lemmas:
                    clean_wordlist.append(lemma)
                
                for key in processed.lemma_dict.keys():
                    if key in nlp_dict:
                        current_value_sent = nlp_dict[key]['sent']
                        nlp_dict[key]['sent'] = processed.lemma_dict[key]['sent'] + current_value_sent
                        current_value_chunk = nlp_dict[key]['chunk']
                        nlp_dict[key]['chunk'] = processed.lemma_dict[key]['chunk'] + current_value_chunk
                        current_value_label = nlp_dict[key]['this_label']
                        nlp_dict[key]['this_label'] = processed.lemma_dict[key]['this_label'] + current_value_label
                    else:
                        nlp_dict[key] = {}
                        nlp_dict[key]['chunk'] = processed.lemma_dict[key]['chunk']
                        nlp_dict[key]['sent'] = processed.lemma_dict[key]['sent']
                        nlp_dict[key]['this_label'] = processed.lemma_dict[key]['this_label']



                print(f'counter is {counter}')
                counter += 1

freq_data = list(filter(None, clean_wordlist))

count = collections.Counter(freq_data)

common = count.most_common(None)

for x,y in common:
    nlp_dict[x]['count'] = y

counting_dict = {}

for key in nlp_dict.keys():
    counting_dict[key]= nlp_dict[key]['count']

freq_df = pd.DataFrame.from_dict(counting_dict, orient='index', columns=['count'])

print(freq_df.sort_values('count', ascending=False))

