import requests #первый шаг - это импорт библиотек
from bs4 import BeautifulSoup
import nltk
import nltk.corpus
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk import sent_tokenize
from string import punctuation
from nltk.corpus import stopwords
import pymorphy2
import gensim
from gensim import corpora
from pprint import pprint
from gensim import models
from gensim.models import LdaModel, LdaMulticore
from gensim.models import LsiModel
import pickle




punctuation = '—'.join(punctuation)
punctuation = '«'.join(punctuation)
punctuation = '»'.join(punctuation)
punctuation = "„".join(punctuation)
punctuation = '“'.join(punctuation)
punctuation = r"\'\'".join(punctuation)


morph = pymorphy2.MorphAnalyzer()
stopwords = stopwords.words('russian') + [a for a in punctuation]


all_tokens_lists = []
def main():
    url_generator = 'https://news.tut.by/daynews/{}'
    for i in range(1, 81):
        url = url_generator.format(str(i))
        grams(tokenizer(get_data(get_html(url))))
        #all_tokens = tokenizer(get_data(get_html(url)))
       # all_tokens_lists.append(all_tokens)
    #topics(all_tokens_lists)


def get_html(url):
    r = requests.get(url)
    if r.ok:
        return r.text
    print(r.status_code)

def get_data(html):
    soup = BeautifulSoup(html, 'html.parser').find_all('div', class_='news-entry big annoticed time ni')
    for art in soup:
        link = art.find('a', href=True)
        links = (link['href'])
        r2 = requests.get(links).text
        soup2 = BeautifulSoup(r2, 'lxml')
        article_text = soup2.find('div', id="article_body").text if soup2.find('div', id="article_body") else 'ОШИБКА'
        article_text_l = article_text.lower()
        return article_text_l

def tokenizer(article_text_l):
    tokens_clean = []
    tokens = word_tokenize(text = article_text_l)
    for token in tokens:
        if token not in stopwords:
            form = morph.parse(token)[0].normal_form
            tokens_clean.append(form)
    return tokens_clean

def grams(tokens_clean):
    bg = tokens_clean
    bgfd = nltk.FreqDist(bg)
    print(bgfd.most_common(10))

def topics(all_tokens_lists):
    mydict = corpora.Dictionary(all_tokens_lists)
    mycorpus = [mydict.doc2bow(doc) for doc in all_tokens_lists]
    import pickle
    pickle.dump(mycorpus, open('corpus1.pkl', 'wb'))
    mydict.save('dictionary1.gensim')
    ldamodel = gensim.models.ldamodel.LdaModel(corpus=mycorpus,
                                               id2word=mydict,
                                               num_topics=10,
                                               random_state=100,
                                               update_every=1,
                                               chunksize=100,
                                               passes=10,
                                               alpha='auto',
                                               per_word_topics=True)
    ldamodel.save('lda_model_10.gensim')
    pprint(ldamodel.print_topics())



def lsi(all_tokens_lists):
    dictionary = corpora.Dictionary(all_tokens_lists)
    corpus = [dictionary.doc2bow(text) for text in all_tokens_lists]
    tfidf = models.TfidfModel(corpus, smartirs = 'ntc')
    tfidf_model = tfidf[corpus]
    lsi_model = LsiModel(corpus = tfidf_model, id2word = dictionary, num_topics = 7, decay = 0.5)
    pprint(lsi_model.print_topics(-1, 10))




if __name__ == '__main__':
    main()

#def lemminger(article_text):
    #lemmas = m.lemmatize(article_text)
   # lemmas_clean = ''.join(lemmas)
   # print(lemmas_clean)





