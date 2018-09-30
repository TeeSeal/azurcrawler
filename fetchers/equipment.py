from requests import get
from shared import save_fixture
from bs4 import BeautifulSoup

html = get('https://azurlane.koumakan.jp/Equipment').text
fp = BeautifulSoup(html, 'lxml')

for td in fp.select('.mw-collapsible.wikitable td[style*="Gold"]'):
    link = td.select('a')[-1]
    path = link['href']
    print(link['title'])
    save_fixture('equipment', path[1:].replace('/', ''), get(f'https://azurlane.koumakan.jp{path}').text)
