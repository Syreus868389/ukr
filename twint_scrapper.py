import twint
import json
from deep_translator import LibreTranslator
from spacy_handlers import *

# the base query should be in english
base_query = "ukraine kiev"

languages = ['fr']
queries = [base_query]


for lang in languages:
    queries.append(LibreTranslator(source='en',target=lang).translate(base_query))

languages.insert(0, 'en')

with open('queries.txt', 'w', encoding='utf-8') as query_file:
    query_file.write(' '.join(queries))
    query_file.close()


c = twint.Config()
c.Custom = ['datestamp','username', 'name', 'user_id', 'tweet', 'hashtags', 'link', 'likes_count', 'replies_count', 'retweets_count', 'lang']
c.Filter_retweets = True
c.Retries_count = 40
c.Until = "2022-10-01"
c.Since = "2022-10-13"
c.Utc = False
c.Full_text = False
c.Store_object = True
c.Count = True
c.Hide_output = False

main_id = 0

for query, lang in zip(queries, languages):
    print(query)
    c.Search = query
    c.Lang = lang
    twint.run.Search(c)

    out_tweets = twint.output.tweets_list

    tweet_id = 0

    chunk = 1

    tweet_list = []
    
    for tweet in out_tweets:
        unique_id = {"unique_id": str(main_id)+str(tweet_id)}
        tweet_content = tweet.__dict__
        tweet_content.update(unique_id)
        
        if len(tweet_list) < 300:
            tweet_list.append(tweet_content)

        else:
            tweet_chunk = f'./corpus/chunk{chunk}.json'

            with open(tweet_chunk, 'w', encoding='utf-8') as outfile:
                json.dump(tweet_list, outfile, indent=4, ensure_ascii=False)
            outfile.close()

            chunk += 1
            tweet_list = []

        print(tweet_id)
        tweet_id += 1


    main_id += 1





