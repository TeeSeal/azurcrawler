from shared import read_fixture, save_json
from bs4 import BeautifulSoup, SoupStrainer

def parse_row(row):
    tds = [td.text for td in row.select("td")]
    data = {
        'id': tds[0],
        'name': tds[1],
        'rarity': tds[2],
        'type': tds[3],
        'affiliation': tds[4],
        'stats': {
            'firepower': tds[5],
            'health': tds[6],
            'antiAir': tds[7],
            'speed': tds[8],
            'airPower': tds[9],
            'torpedo': tds[10]
        },
        'url': 'https://azurlane.koumakan.jp{}'.format(row.select_one('a')['href'])
    }

    return data


fixture = read_fixture('ships_short', 'list_of_ships')
html = BeautifulSoup(fixture, 'lxml')
rows = html.select('.mw-parser-output .wikitable tr')
data = [parse_row(row) for row in rows if not row.th]
save_json('ships_short', data)
