import requests
import string
import os
from bs4 import BeautifulSoup

page = input()
article_type = input()
for i in range(1, int(page) + 1):
    url_list_articles = "https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=" + str(i)
    r1 = requests.get(url_list_articles, headers={'Accept-Language': 'en-US,en;q=0.5'})
    if r1.status_code == 200:
        soup1 = BeautifulSoup(r1.content, 'html.parser')

        types = soup1.find_all('span', {'class': "c-meta__type"})

        position_news_articles = []  # [9,11,18]
        k = 0
        for t in types:
            if t.text == article_type:  # Find the 'News' ones
                position_news_articles.append(k)
            k = k + 1

        hrefs = soup1.find_all('a', {'data-track-action': "view article"})
        articles_url = []  # stores all news articles urls
        for position in position_news_articles:
            href = hrefs[position]['href']
            url_article = "https://www.nature.com" + str(href)
            articles_url.append(url_article)

        articles_title = []
        os.mkdir('Page_' + str(i))
        for url in articles_url:
            r2 = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
            soup2 = BeautifulSoup(r2.content, 'html.parser')

            article_title = []
            if article_type == "Research Highlight":
                article_title = soup2.find('h1', {'class': "article-item__title"}).text.strip()
            else:
                article_title = soup2.find('h1', {'class': "c-article-magazine-title"}).text.strip()

            for p in article_title:
                if p in string.punctuation:
                    article_title = article_title.replace(p, "")

            article_title = article_title.replace(' ', '_')
            articles_title.append(article_title)
            article_body = []

            if article_type == "Research Highlight":
                article_body = soup2.find('div', {'class': "article-item__body"}).text.strip()
            else:
                article_body = soup2.find('div', {'class': "c-article-body u-clearfix"}).text.strip()

            os.chdir(os.getcwd() + '\\Page_' + str(i))
            file_name = article_title + '.txt'
            file = open(file_name, 'wb')
            file.write(article_body.encode())
            file.close()
            os.chdir("..")

        print("Saved articles:")
        print(articles_title)
