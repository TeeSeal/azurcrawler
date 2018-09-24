from os import makedirs
from os.path import realpath, dirname, join, isdir
from bs4 import BeautifulSoup
from json import dump

ROOT = join(dirname(realpath(__file__)), '..')
FIXTURES = join(ROOT, 'fixtures')
DATA = join(ROOT, 'data')


def read_fixture(dir_name, file_name):
    fp = open(join(FIXTURES, dir_name, f'{file_name}.html'))
    return BeautifulSoup(fp, 'html.parser')


def save_json(file_name, json):
    if not isdir(DATA):
        makedirs(DATA)

    with open(join(DATA, f'{file_name}.json'), 'w') as output:
        dump(json, output, indent=2)
