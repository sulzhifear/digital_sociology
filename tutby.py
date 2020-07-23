import requests
from bs4 import BeautifulSoup
import json
import csv

key_word1 = 'коронавир'
key_word2 = 'covid'
key_word3 = 'эпидем'
key_word4 = 'пандем'


all_data = []


def main():
    url_generator = 'https://news.tut.by/daynews/{}'
    for i in range(1, 181):
        url = url_generator.format(str(i))
        get_data(get_html(url))


def write_json(all_data):
    with open('16_06_2020_nata_json_day_news_tut.json', 'w', encoding='utf-8') as file:
        json.dump(all_data, file, indent=2, ensure_ascii=False)

def write_csv(text_info):
     with open("10_tut_covid_new.csv", "a", encoding='utf-8') as fi:
         wrtr = csv.DictWriter(fi, fieldnames={"article_name",
                                               "article_text",
                                               "date",
                                               })
         wrtr.writerow(text_info)

def get_html(url):
    r = requests.get(url)
    if r.ok:
        return r.text
    print(r.status_code)

def get_data(html):
    soup = BeautifulSoup(html, 'html.parser').find_all('div', class_='news-entry big annoticed time ni')
    for art in soup:
        link = art.find('a', class_='entry__link', href=True)
        links = (link['href'])
        r2 = requests.get(links)
        r2 = r2.text
        soup2 = BeautifulSoup(r2, 'lxml')
        try:
            article_name = soup2.find('div', class_='m_header').find('h1').text
            date = soup2.find('p', class_="b-article-details").find('time').text
            article_text = soup2.find('div', id="article_body").text.replace('\xa0', ' ')
        except:
            print('Это что ещё такое?')
        text_info = {'article_name': article_name,
                     'article_text': article_text,
                     'date': date
        }
        all_data.append(text_info)
        write_json(all_data)
        article_name_l = article_name
        article_text_l = article_text
        try:
            print('Заголовог статьи===========>', article_name)
            print("Текст статьи=============>", article_text)
            print("Дата публикации===========>", date)
            print('Автор==========>', soup2.find('p', class_="b-article-details").find('span').text)
            print("Теги==============>", soup2.find('li', class_="tag-taxonomy-topic").text)
            print("********************************************************************************")
            print("Number of words in title", len(str.split(article_name_l)))
            print('Number of characters in title:', len(article_name_l))
            print('Number of characters in the text', len(article_text_l))
            print('The density of keyword Coronavirus in the title:',
                  article_name_l.count(key_word1) / (len(str.split(article_name_l))) * 100)
            print('The density of keyword Covid-19 in the title',
                  article_name_l.count(key_word2) / (len(str.split(article_name_l))) * 100)
            print('The density of keyword Epidemy in the title',
                  article_name_l.count(key_word3) / (len(str.split(article_name_l))) * 100)
            print('The density of keyword Pandemy in the title', article_name_l.count(key_word4) / (
                len(str.split(article_name_l))) * 100)
            print('The density of keyword Coronavirus in the text',
                  article_text_l.count(key_word1) / (len(str.split(article_text_l))) * 100)
            print('The density of keyword Covid-19  in the text',
                  article_text_l.count(key_word2) / (len(str.split(article_text_l))) * 100)
            print('The density of keyword Epidemy in the text:',
                  article_text_l.count(key_word3) / (len(str.split(article_text_l))) * 100)
            print('The density of keyword Pandemy in the text',
                  article_text_l.count(key_word4) / (len(str.split(article_text_l))) * 100)
        except:
            print(article_name, 'ошибочка вышла')





if __name__ == '__main__':
    main()






