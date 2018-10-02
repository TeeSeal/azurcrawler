from requests import get
from shared import save_fixture, build_url
from bs4 import BeautifulSoup

html = get('https://azurlane.koumakan.jp/Equipment_List').text
fp = BeautifulSoup(html, 'lxml')
category_urls = [link['href'] for link in fp.find('ul').select('a')]

for category_url in category_urls:
    category_html = get(build_url(category_url)).text
    table = BeautifulSoup(category_html, 'lxml').select_one('.tabbertab table')
    paths = set([row.find('a')['href'] for row in table.find_all('tr') if not row.find('th')])

    for path in paths:
        name = path[1:]
        if 'w/index.php?' in name:
            continue
        print(name)
        save_fixture('equipment', name, get(build_url(path)).text)
