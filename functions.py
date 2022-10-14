import math
import re
from spellchecker import SpellChecker

checker = SpellChecker(language='en')

def round_down_to_nearest_10(num):
    return math.floor(num / 10) * 10

def title_maker(response, list):
        results =  response['results']
        for result in results:
            title = result['title']
            list.append(title)

def api_call (api, query, page):
    response = api.news_api(language="fr,en", q=query, page=page)
    return response

def remove_url(txt):
    """Replace URLs found in a text string with nothing 
    (i.e. it will remove the URL from the string).

    Parameters
    ----------
    txt : string
        A text string that you want to parse and remove urls.

    Returns
    -------
    The same txt string with url's removed.
    """
    no_urls = " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())

    return no_urls

def spec_cleaner(txt):
    result = " ".join(filter(lambda x:x[0]!='@', txt.split()))
    return result

def punct_cleaner(txt):
    no_point_text = txt.translate(str.maketrans('','', '.:;-?!="'))
    return no_point_text

def spell_check(txt):
    spell_list = txt.split()
    for word in spell_list:
            if word not in checker:
                try:
                    cor = checker.correction(word)
                    txt = txt.replace(word, cor)
                except:
                    continue
    return txt