from requests import get
from shared import save_fixture

result = get('https://azurlane.koumakan.jp/List_of_Ships')
save_fixture('ships_short', 'list_of_ships', result.text)

result = get('https://azurlane.koumakan.jp/List_of_Ships_by_Image')
save_fixture('ships_short', 'list_of_ships_by_image', result.text)
