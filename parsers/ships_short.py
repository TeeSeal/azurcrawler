from shared import read_fixture, build_url, save_json

def parse_row(row):
    tds = [td.text for td in row.select("td")]
    img = thumbnails.select_one(f'a[title="{tds[1]}"] img')
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
        'url': build_url(row.select_one('a')['href']),
        'thumbnail': build_url(img['srcset'].split()[0] if img.has_attr('srcset') else img['src'])
    }

    return data


fixture = read_fixture('ships_short', 'list_of_ships')
thumbnails = read_fixture('ships_short', 'list_of_ships_by_image')
rows = fixture.select('.mw-parser-output .wikitable tr')
data = [parse_row(row) for row in rows if not row.th]
save_json('ships_short', data)
