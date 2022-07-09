from collections import defaultdict
from bs4 import BeautifulSoup
import requests
import time
import socket
import os
import requests.packages.urllib3.util.connection as urllib3_cn


####################
# START PARSE PART #
####################

# force ipv4 because ipv6 takes too long to respond
def allowed_gai_family():
    family = socket.AF_INET 
    return family
urllib3_cn.allowed_gai_family = allowed_gai_family

url_root = "https://ru.wikipedia.org"
first_url = url_root + "/wiki/Категория:Животные_по_алфавиту"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"
    }

def get_page(url: str):
    res = requests.get(url, headers=headers)
    html = res.text

    bs = BeautifulSoup(html, "html.parser")

    next_page_el = bs.find('a', text="Следующая страница")
    next_page_link = next_page_el['href'] if next_page_el is not None else None

    div = bs.find('div', { 'id': 'mw-pages'})
    lis = div.find_all('li')
    return [li.text for li in lis], next_page_link

def parse_last_page(bs):

    divs = bs.select("div.mw-category-group")
    lis = div.find_all('li')
    return [li.text for li in lis]


def get_all_iter():
    first_page, next_url = get_page(first_url)
    yield from first_page

    while next_url is not None:
        next_page, next_url = get_page(url_root + next_url)
        yield from next_page

def load_to_file(filename: str):
    def f_time(time_: int):
        return f"{int(time_ // 60)}:{int(time_ % 60)}"

    start_time = time.time()

    with open(filename, 'w+') as f:
        for animal in get_all_iter():
            print(animal)
            f.write(animal + '\n')
    
    end_time = time.time()
    delta = end_time - start_time
    print(f"Loaded all animals in {f_time(delta)}")

##################
# END PARSE PART #
##################

def count_letters(names: list[str]):
    count_dict = defaultdict(lambda: 0)

    for n in names:
        first_letter = n[0].upper()
        count_dict[first_letter] += 1
    
    for letter, count in count_dict.items():
        print(f"{letter}: {count}")


if __name__ == "__main__":
    # load all animals from wikipedia on first run
    animal_file = 'animals.txt'
    if not os.path.exists(animal_file):
        load_to_file(animal_file)

    with open(animal_file) as f:
        animals = f.readlines()

    count_letters(animals)