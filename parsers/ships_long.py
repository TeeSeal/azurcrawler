from shared import read_all_fixtures, build_url, save_json
from re import sub, search, findall

def extract_names(html):
    title = sub(r'^[A-Z]{3,4} ', '', html.find('span').text.strip())
    names = {
        'en': search(r'^[^\(]+', title).group(0).strip(),
        'cn': search(r'(?<=cn: )[^;]+', title).group(0).strip(),
        'jp': search(r'(?<=jp: )[^\)]+', title).group(0).strip()
    }

    return names

def extract_base_data(html):
    keys = ['construction_time', 'rarity', 'class', 'id', 'nationality', 'type']
    base_data = dict(zip(keys, [info.find('td').text.strip(' \n') for info in html.find_all('tr')[:6]]))
    base_data['rarity'] = parse_rarity(html.find_all('tr')[1].find('img')['alt'])
    return base_data

def extract_stats(html):
    base_stats = [stat.text.replace('\n', '').strip() for stat in html.select_one('[title*="Base Stats"]').find_all('tr')[-3:]]
    speed = int(search(r'\d+', base_stats[0]).group(0).strip()) if search(r'\d+', base_stats[0]) else 0
    reinforcement_value = [int(i) for i in findall(r'\d+', base_stats[1])]
    scrap_income = [int(i) for i in findall(r'\d+', base_stats[2])]

    stats = {
        'base': parse_stats_table(html.select_one('[title*="Base Stats"]')),
        'max': parse_stats_table(html.select_one('[title*="Level 100"]')),
        'max20': parse_stats_table(html.select_one('[title*="Level 120"]')),
        'speed': speed,
        'reinforcement_value': dict(zip(['firepower', 'torpedo', 'air_power', 'reload'], reinforcement_value)),
        'scrap_income': dict(zip(['coin', 'oil', 'medal'], scrap_income))
    }

    return stats

def parse_stats_table(table):
    keys = ['health', 'armor', 'reload', 'firepower', 'torpedo', 'speed', 'anti_air', 'air_power', 'oil_usage', 'anti_sub']
    # Oh boi
    data = zip(keys, map(lambda td: int(sub(r'\D', '', td.text.strip())) if search(r'\d+', td.text) else td.text.strip(), table.select('td')[:10]))

    return dict(data)

def extract_equipment_data(html):
    data = [row for div in html.select('div[style*="text-align:center;"]') for table in div.select('table') for row in table.select('tr')[-3:]]
    equipment = [equip.text.strip() for row in data for equip in row.select('td')[-2:]]
    test = dict(zip(equipment[1::2], equipment[::2]))

    return test

def extract_pictures(html):
    return {
        'images': [extract_skin(tab) for tab in html.select('div.shiparttabbernew .tabbertab')],
        'icon': build_url(html.select_one('img')['src']) if html.select_one('img') else 'N/A',
        'chibi': build_url(html.select_one('#talkingchibi img')['src']) if html.select_one('#talkingchibi img') else 'N/A'
    }

def extract_skin(tab):
    image_path = tab.select_one('img')['srcset'].split(' ')[-2]
    return { 'name': tab['title'], 'url': build_url(image_path) }

def parse_rarity(str):
    switch = {
        'Rarity Normal.png': 'Normal',
        'Rare.png': 'Rare',
        'Elite.png': 'Elite',
        'SuperRare.png': 'Super Rare',
        'Legendary.png': 'Legendary',
        'Priority.png': 'Priority'
    }

    return switch.get(str, 'Unknown')

data = []
fixtures = read_all_fixtures('ships_long')
for fp in fixtures:
    ship = { 'page_url': fp.select_one('meta[property="og:url"]')['content'] }
    names = extract_names(fp)
    base_data = extract_base_data(fp)
    stats = extract_stats(fp)
    equipment = extract_equipment_data(fp)
    pictures = extract_pictures(fp)
    data.append({**ship, **names, **base_data, **stats, **equipment, **pictures})

save_json('ships_long', data)
