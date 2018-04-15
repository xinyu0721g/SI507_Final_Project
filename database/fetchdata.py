import requests
from bs4 import BeautifulSoup
from classes import *


CACHE_FNAME_WHOLE = 'Fang_sh_all_second_hand_housing_cache.json'
CACHE_FNAME_INDIVIDUAL = 'Fang_sh_all_second_hand_housing_individual_cache.json'
CACHE_FNAME_OBJECT = 'Fang_sh_all_second_hand_housing_object_cache.json'


def get_unique_identifier(url):
    return url


def get_whole_web_page_from_cache(cache_fname_whole, web_url):
    """
    :param cache_fname_whole: cache-file's name
    :param web_url: web_url
    :return: cached whole web page in html format for a specific url
    """

    unique_identifier = get_unique_identifier(web_url)
    cache_fdest = 'cache/' + cache_fname_whole

    try:
        infile = open(cache_fdest, 'r')
        infile_content = infile.read()
        diction = json.loads(infile_content)
        infile.close()
    except Exception:
        diction = {}

    if unique_identifier in diction:
        print('Getting data from cache...')
        content = diction[unique_identifier]
    else:
        print('Getting data from new request...')
        content = requests.get(web_url).text
        diction[unique_identifier] = content
        dumped_dict = json.dumps(diction, indent=2)
        outfile = open(cache_fdest, 'w')
        outfile.write(dumped_dict)
        outfile.close()
    return content


def get_basic_individual_house_info_from_cache(cache_fname_individual, house_url):
    """
    This is used to cache basic information (tab-cont-right) for an individual housing post page.
    :param cache_fname_individual: cache-file's name
    :param house_url: url for a specific housing post
    :return: cached basic information in html format for a specific url
    """

    unique_identifier = get_unique_identifier(house_url)
    cache_fdest = 'cache/' + cache_fname_individual

    try:
        infile = open(cache_fdest, 'r')
        infile_content = infile.read()
        diction = json.loads(infile_content)
        infile.close()
    except Exception:
        diction = {}

    if unique_identifier in diction:
        print('Getting data from cache...')
        content = diction[unique_identifier]
    else:
        print('Getting data from new request...')
        html = requests.get(house_url).text
        soup = BeautifulSoup(html, 'html.parser')
        basic_info_div = soup.find('div', class_='tab-cont-right')
        content = str(basic_info_div)
        diction[unique_identifier] = content
        dumped_dict = json.dumps(diction, indent=2)
        outfile = open(cache_fdest, 'w')
        outfile.write(dumped_dict)
        outfile.close()
    return content


def create_House_object_from_cache(cache_fname_individual, house_url, title):
    """
    :param cache_fname_individual: cache-file's name
    :param house_url: url for a specific housing post
    :param title: title of the housing post
    :return: a House object
    """

    info_div_html = get_basic_individual_house_info_from_cache(
        cache_fname_individual, house_url)
    info_div = BeautifulSoup(info_div_html, 'html.parser')
    house_obj = House(title, house_url, info_div)
    return house_obj


def get_one_page_second_hand_housing_sh_Fang(cache_fname_individual, house_divs):
    base_url = 'http://esf.sh.fang.com'
    house_lst = []
    for h_div in house_divs:
        info = h_div.find('dd', class_="info rel floatr")
        try:
            house_url_extend = info.find('p', class_="title").a['href']
            house_url = base_url + house_url_extend
            house_title = info.find('p', class_="title").text.strip()
            house_object = create_House_object_from_cache(cache_fname_individual, house_url, house_title)
            house_lst.append(house_object)
            print(house_object)
        except:
            pass
    return house_lst


def get_first_page_second_hand_housing_sh_Fang(cache_fname_whole, cache_fname_individual):
    base_url = 'http://esf.sh.fang.com'
    html = get_whole_web_page_from_cache(cache_fname_whole, base_url)
    soup = BeautifulSoup(html, 'html.parser')
    div_houselist = soup.find('div', class_="houseList")
    house_divs = div_houselist.find_all('dl')
    house_lst = get_one_page_second_hand_housing_sh_Fang(cache_fname_individual, house_divs)
    return house_lst


def get_all_second_hand_housing_sh_Fang(cache_fname_whole, cache_fname_individual):
    """
    :return: list of House objects (around 3000 records)
    """

    base_url = 'http://esf.sh.fang.com'
    html = get_whole_web_page_from_cache(cache_fname_whole, base_url)
    house_lst = []

    while True:
        soup = BeautifulSoup(html, 'html.parser')
        div_houselist = soup.find('div', class_="houseList")
        house_divs = div_houselist.find_all('dl')
        house_lst += get_one_page_second_hand_housing_sh_Fang(cache_fname_individual, house_divs)
        try:
            next_page_url_extend = soup.find(id="PageControl1_hlk_next")['href']
            next_page_url = base_url + next_page_url_extend
            html = get_whole_web_page_from_cache(cache_fname_whole, next_page_url)
        except Exception:
            break
    return house_lst


if __name__ == '__main__':
    get_first_page_second_hand_housing_sh_Fang(CACHE_FNAME_WHOLE, CACHE_FNAME_INDIVIDUAL)
    # get_all_second_hand_housing_sh_Fang(CACHE_FNAME_WHOLE, CACHE_FNAME_INDIVIDUAL)
    pass


