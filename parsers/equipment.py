from shared import read_all_fixtures, build_url, save_json, read_fixture
from re import sub, search, findall

def parse_tab(tab):
    return {
        'title': tab['title'],
        **extract_base_data(tab),
        **extract_stats(tab),
        **extract_additional_data(tab)
    }

def extract_base_data(tab):
    table = tab.find('table')
    data = [row.select('td')[-1].text.replace('★', '').strip() for row in table.find_all('tr')[3:]]
    keys = ['rarity', 'nation', 'tech_level']
    return dict(zip(keys, data))

def extract_stats(tab):
    table = tab.find_all('table')[1]
    equip_type = tab.find_all('tr')[2].select('td')[-1].text.strip()

    data = [td.text.strip() for td in table.find_all('td') if not td.select('b, img')]
    keys = stats_keys_for(equip_type)

    if not equip_type in ['Fighter', 'Dive Bomber']:
        return { **dict(zip(keys, data)) }

    # Special handling for aviation
    diff = len(data) - len(keys)
    stats = data[:-diff]
    weapons = [weapon for weapon in data[-diff:] if not weapon == ""]

    return { **dict(zip(keys, stats)), 'weapons': weapons }

def stats_keys_for(equip_type):
    if equip_type in ['Fighter', 'Dive Bomber', 'Torpedo Bomber']:
        return ['health', 'air_power', 'damage', 'range', 'rate_of_fire', 'spread', 'rounds', 'angle']

    if equip_type == 'Torpedo':
        return ['torpedo', 'torpedo_count', 'damage', 'range', 'rate_of_fire', 'spread', 'characteristic']

    if equip_type == 'Auxiliary':
        return ['health', 'torpedo', 'reload', 'firepower', 'air_power', 'speed', 'anti_air', 'oxygen']

    if equip_type == 'Sonar':
        return ['anti_sub', 'accuracy', 'ping_frequency', 'range', 'characteristic']

    # Keys for the gun type
    return [
        'fire_power', 'anit_air', 'damage', 'range', 'rate_of_fire',
        'spread','volley', 'angle', 'ammo_type', 'characteristic'
    ]

def extract_additional_data(tab):
    table = tab.find_all('table')[-1]
    data = [td.text.strip() for td in table.find_all("td")[1::2]]

    return dict(zip(['obtained_from', 'notes'], data))

def extract_picture(html):
    img = html.find('img')
    path = img['srcset'].split(' ')[-2] if img.has_attr('srcset') else img['src']
    return build_url(path)

data = []
for fp in read_all_fixtures('equipment'):
    print(fp.select_one('meta[property="og:url"]')['content'])
    if not fp.find('th'):
        continue

    data.append({
        **dict({
            'page_url': fp.select_one('meta[property="og:url"]')['content'],
            'name': fp.find('th').text.strip(),
            'type': fp.find_all('tr')[2].select('td')[-1].text.strip(),
            'icon': extract_picture(fp),
            'types': [parse_tab(tab) for tab in fp.select('.tabbertab')]
        }),
    })

save_json('equipment', data)
