from os import makedirs, listdir
from os.path import realpath, dirname, join, isdir, abspath
from bs4 import BeautifulSoup
from json import dump

ROOT = abspath(join(dirname(realpath(__file__)), '..'))
FIXTURES = join(ROOT, 'fixtures')
DATA = join(ROOT, 'data')


def read_fixture(dir_name, file_name):
    if not file_name.endswith('.html'):
        file_name = f'{file_name}.html'

    fp = open(join(FIXTURES, dir_name, file_name))
    return BeautifulSoup(fp, 'html.parser')


def read_all_fixtures(dir_name):
    dir_path = join(FIXTURES, dir_name)
    return [read_fixture(dir_name, fixture) for fixture in listdir(dir_path)]


def save_json(file_name, json):
    if not isdir(DATA):
        makedirs(DATA)

    with open(join(DATA, f'{file_name}.json'), 'w') as output:
        dump(json, output, indent=2)
