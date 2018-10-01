from requests import get
from shared import save_fixture, build_url
from bs4 import BeautifulSoup

html = get('https://azurlane.koumakan.jp/List_of_Ships').text
fp = BeautifulSoup(html, 'lxml')
rows = fp.select('.mw-parser-output .wikitable tr')
urls = [build_url(row.find('a')['href']) for row in rows if not row.find('th')]

for url in urls:
    name = url.split('/')[-1]
    print(name)
    save_fixture('ships_long', name, get(url).text)
