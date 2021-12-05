import requests
import bs4

KEYWORDS = ['design', 'photo', 'web', 'python']

url = 'https://habr.com/'
domain = "https://habr.com"

response = requests.get(url)
response.raise_for_status()

soup = bs4.BeautifulSoup(response.text, features='html.parser')
articles = soup.find_all('article')

print(f'Статьи с сайта {domain}, в которых присутствуют ключевые слова {KEYWORDS}')
print(f'в формате: дата - заголовок - ссылка')


def find_article(article_to_test, article_snippet):
    for word in KEYWORDS:
        if word.title() in article_snippet or word.lower() in article_snippet or word.upper() in article_snippet:
            title = article_to_test.find('h2').text.strip()
            link_part = article_to_test.find(class_='tm-article-snippet__title-link').attrs['href']
            link = domain + link_part
            date = article_to_test.find("span",
                                        class_="tm-article-snippet__datetime-published").find("time").get("title")
            print(f'{date} - {title} - {link}. Ключевое слово: {word}')
            break


print('---')
print('Поиск по превью статьи:')

for article in articles:
    snippet = article.find("div", class_="tm-article-body tm-article-snippet__lead").text.strip()
    find_article(article, snippet)

print('---')
print('Поиск по всей статье:')

for article in articles:
    link_part = (article.find("div", class_="tm-article-body tm-article-snippet__lead").
                 find("a", class_="tm-article-snippet__readmore").get("href"))
    link = domain + link_part
    response_full_article = requests.get(link)
    response_full_article.raise_for_status()
    soup_full_article = (bs4.BeautifulSoup(response_full_article.text, features='html.parser')
                         .find("div", class_="tm-article-presenter__body").text.strip())
    find_article(article, soup_full_article)
