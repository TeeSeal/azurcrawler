from os import makedirs
from os.path import realpath, dirname, join, isdir

ROOT = join(dirname(realpath(__file__)), '..')
FIXTURES = join(ROOT, 'fixtures')


def save_fixture(dir_name, file_name, html):
    dir_path = join(FIXTURES, dir_name)
    if not isdir(dir_path):
        makedirs(dir_path)

    path = join(dir_path, f'{file_name}.html')
    with open(path, "w") as file:
        file.write(html)
