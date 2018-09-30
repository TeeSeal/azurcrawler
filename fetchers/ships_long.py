from requests import get
from shared import save_fixture
from bs4 import BeautifulSoup, SoupStrainer

def extract_url(row):
    path = row.select_one('a')['href']
    return f'https://azurlane.koumakan.jp{path}'

html = get('https://azurlane.koumakan.jp/List_of_Ships').text
only_output = SoupStrainer('div', attrs={'class': 'mw-parser-output'})
fp = BeautifulSoup(html, 'lxml', parse_only=only_output)
urls = [extract_url(row) for row in fp if not row.select_one('th')]

for url in urls:
    name = url.split('/')[-1]
    print(name)
    save_fixture('ships_long', name, get(url).text)
