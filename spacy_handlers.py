import spacy

from functions import remove_url

nlp = spacy.load("en_core_web_sm")
nlp_fr = spacy.load("fr_core_news_sm")

query_words = []

with open('queries.txt', 'r', encoding='utf-8') as query_file:
    queries = query_file.read()
    query_file.close()


for query in queries:
    for word in query.split():
        query_words.append(word)

class SpacyHandler:
    def __init__(self, text) :
            text = remove_url(text).lower()
            self.doc = nlp(text)
            self.lemmas = []
            self.lemma_dict = {}

    def handler(self):

        sents = self.doc.sents

        for sent in sents:
            
            chunks = nlp(sent.text).noun_chunks

            

            for chunk in chunks:
                ents = nlp(chunk.text).ents
                for token in nlp(chunk.text):

                    if token.text not in queries:
                        this_label = None
                        for ent in ents:
                            if ent.text == token.text:
                                this_label = ent.label_

                        lemma = token.lemma_

                        if lemma not in nlp.Defaults.stop_words and nlp_fr.Defaults.stop_words:
                            self.lemmas.append(lemma)
                            self.lemma_dict[lemma] = {}
                            self.lemma_dict[lemma]['sent'] = [sent]
                            self.lemma_dict[lemma]['chunk'] = [chunk]
                            self.lemma_dict[lemma]['this_label'] = [this_label]
                        else:
                            continue



