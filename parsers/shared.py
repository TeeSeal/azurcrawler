from os import makedirs, listdir
from os.path import realpath, dirname, join, isdir, abspath
from json import dumps
from bs4 import BeautifulSoup

ROOT = abspath(join(dirname(realpath(__file__)), '..'))
FIXTURES = join(ROOT, 'fixtures')
DATA = join(ROOT, 'data')

def read_fixture(dir_name, file_name):
    if not file_name.endswith('.html'):
        file_name = f'{file_name}.html'

    with open(join(FIXTURES, dir_name, file_name), encoding='utf8') as fp:
        return BeautifulSoup(fp, 'lxml')


def read_all_fixtures(dir_name):
    dir_path = join(FIXTURES, dir_name)
    return [read_fixture(dir_name, fixture) for fixture in listdir(dir_path)]


def save_json(file_name, json):
    if not isdir(DATA):
        makedirs(DATA)

    with open(join(DATA, f'{file_name}.json'), 'w', encoding='utf8') as output:
        output.write(dumps(json, indent=2, ensure_ascii=False))

def build_url(path):
    return f'https://azurlane.koumakan.jp{path}'
