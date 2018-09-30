from shared import read_all_fixtures, build_url, save_json
from re import sub, search, findall

def extract_names(html):
    title = sub(r'^[A-Z]{3,4} ', '', html.find('span').text.strip())
    names = {
        'en': search(r'^[^\(]+', title).group(0).strip(),
        'cn': search(r'(?<=cn: )[^;]+', title).group(0).strip(),
        'jp': search(r'(?<=jp: )[^\)]+', title).group(0).strip()
    }
    return { 'names': names }

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
    return {
        'base': parse_stats_table(html.select_one('[title*="Base Stats"]')),
        'max': parse_stats_table(html.select_one('[title*="Level 100"]')),
        'max20': parse_stats_table(html.select_one('[title*="Level 120"]')),
        'speed': speed,
        'reinforcement_value': dict(zip(['firepower', 'torpedo', 'air_power', 'reload'], reinforcement_value)),
        'scrap_income': dict(zip(['coin', 'oil', 'medal'], scrap_income))
    }

def parse_stats_table(table):
    keys = ['health', 'armor', 'reload', 'firepower', 'torpedo', 'speed', 'anti_air', 'air_power', 'oil_usage', 'anti_sub']
    # Oh boi
    data = zip(keys, map(lambda td: int(sub(r'\D', '', td.text.strip())) if search(r'\d+', td.text) else td.text.strip(), table.select('td')[:10]))
    return dict(data)

def extract_equipment_data(html):
    equips = [row for div in html.select('div[style*="text-align:center;"]') for table in div.select('table') for row in table.select('tr')[-3:]]
    return { 'equipment': [parse_equip(row) for row in equips] }

def parse_equip(row):
    strings = [td.text.strip() for td in row.find_all('td')]
    return dict(zip(['slot', 'efficiency', 'equipable'], strings))

def extract_pictures(html):
    return {
        'images': [extract_skin(tab) for tab in html.select('div.shiparttabbernew .tabbertab')],
        'icon': build_url(html.select_one('img')['src']) if html.select_one('img') else '',
        'chibi': build_url(html.select_one('#talkingchibi img')['src']) if html.select_one('#talkingchibi img') else ''
    }

def extract_skin(tab):
    image_path = tab.select_one('img')['srcset'].split(' ')[-2]
    return { 'name': tab['title'], 'url': build_url(image_path) }

def extract_drop_locations(html):
    chapters = html.select('.nodesktop table tr')[6:]
    drop_locations = [parse_drop_stages(index, chapter) for index, chapter in enumerate(chapters)]
    return { 'drop_locations': [location for sublist in drop_locations for location in sublist] }

def parse_drop_stages(chapter_index, chapter):
    stages = ['Green' in td['style'] for td in chapter.find_all('td')]
    indexes = [i for i, drops in enumerate(stages) if drops]
    return [f'{chapter_index + 1}-{index + 1}' for index in indexes]

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
    data.append({
        **dict({ 'page_url': fp.select_one('meta[property="og:url"]')['content'] }),
        **extract_names(fp),
        **extract_base_data(fp),
        **extract_stats(fp),
        **extract_equipment_data(fp),
        **extract_pictures(fp),
        **extract_drop_locations(fp)
    })

save_json('ships_long', data)
