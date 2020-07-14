import spacy
from spacy import displacy
from spacy.lang.en import English
import spacy.cli
from nltk.stem.porter import *

import re

import json
from tqdm import tqdm

try:
    import en_core_web_lg
except:
    spacy.cli.download("en_core_web_lg")
    import en_core_web_lg


class EntityRetokenizeComponent:
    def __init__(self, nlp):
        pass

    def __call__(self, doc):
        with doc.retokenize() as retokenizer:
            for ent in doc.ents:
                retokenizer.merge(doc[ent.start:ent.end], attrs={"LEMMA": str(doc[ent.start:ent.end])})
        return doc


class Tokenizer:

    def __init__(self):
        # self.stemmer = PorterStemmer()
        self.nlp = nlp = spacy.load("en_core_web_lg")



    def getListOfWords(self, phrase):
        retokenizer = EntityRetokenizeComponent(self.nlp)
        
        try:
            self.nlp.add_pipe(retokenizer, name='merge_phrases', last=True)
        except:
            pass

        doc = self.nlp(phrase)

        # wordlist = [self.stemmer.stem(tok.lower_) for tok in doc if not (tok.is_punct)]  # tok.is_stop or 
        wordlist = [tok.lower_ for tok in doc if not (tok.is_punct)]
        wordlist = [w.replace(' ','') for w in wordlist]
        return [w for w in wordlist if w != '']


    def cleanText(self, text):
        # replace URLs
        re_url = re.compile(r"((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\
                            .([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*",
                            re.MULTILINE|re.UNICODE)
        text = re_url.sub("URL", text)

        # replace IPs
        re_ip = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
        text = re_ip.sub("IPADDRESS", text)
        # replace twitter username

        re_twitter_username = re.compile(r'@([A-Za-z0-9_]+)')
        text = re_twitter_username.sub("twitterUSERNAME", text)

        return self.getListOfWords(text)

def month_year_iter(start_month, start_year, end_month, end_year):
    ym_start= 12*start_year + start_month - 1
    ym_end= 12*end_year + end_month - 1
    for ym in range( ym_start, ym_end ):
        y, m = divmod( ym, 12 )
        yield y, m+1
