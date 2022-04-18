import os
import sys
import logging
import re
from urllib.parse import urlparse
from os.path import basename

import requests
from bs4 import BeautifulSoup

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
headers = {"User-Agent": user_agent}
topage_url_pattern = re.compile(r"window\.location=\"(.+)\"\+this\.value")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_page_urls(root_url):
    parsed_url = urlparse(root_url)
    logger.debug("root_url: {0}, parsed_url: {1}".format(root_url, parsed_url))

    html = requests.get(root_url, headers=headers).content
    soup = BeautifulSoup(html, 'lxml')

    topage = soup.select('select[name=topage]')
    if not topage:
        return []
    onchange = topage[0].get("onchange", None)
    if not onchange:
        return []
    m = topage_url_pattern.search(onchange)
    if not m:
        return []
    method = m.group(1)

    options = topage[0].select('option')
    return [parsed_url.scheme+"://"+parsed_url.netloc+method+option.text.strip() for option in options]


def get_img_url(soup):
    urls = []
    container = soup.select('div#model8_photos')[0]
    links = container.select('td.album_td_blue > a')
    for link in links:
        if "uschoolnet.com" in link.get('href') and \
           "http://tw" in link.get('href'):
            urls.append(link.get('href'))
    return urls


def get_topic(soup):
    return soup.select('font.t1')[0].text


def crawl_photos(root_url):
    html = requests.get(root_url, headers=headers).content
    soup = BeautifulSoup(html, 'lxml')

    topic = get_topic(soup)
    if not os.path.isdir(topic):
        os.mkdir(topic)
        print("create directory {0}".format(topic))

    img_url_list = get_img_url(soup)
    for img_url in img_url_list:
        filename = "{0}/{1}".format(topic, basename(img_url))
        with open(filename, "wb") as f:
            print("Downliad {0} to {1}".format(img_url, filename))
            f.write(requests.get(img_url).content)


def get_topics(root_url):
    parsed_url = urlparse(root_url)
    logger.debug("root_url: {0}, parsed_url: {1}".format(root_url, parsed_url))

    html = requests.get(root_url, headers=headers).content
    soup = BeautifulSoup(html, 'lxml')

    page_count = soup.find_all('option')[-1]["value"]

    topics = []
    for page_idx in range(int(page_count)):
        page_id = page_idx + 1

        page_url = "{0}&page={1}".format(root_url, page_id)
        html = requests.get(page_url, headers=headers).content
        soup = BeautifulSoup(html, 'lxml')

        topics.extend(soup.select(
            'td.jblowball_row2_1 a'))
        topics.extend(soup.select(
            'td.jblowball_row2_2 a'))
        logger.debug("topics: {0}".format(topics))

    resp = []
    for topic in topics:
        if not topic.text.strip():
            continue
        name = topic.text.strip()
        url = parsed_url.scheme + "://" + \
            parsed_url.netloc + parsed_url.path + topic['href']
        logger.debug("topic: {0}, url: {1}".format(
            name, url))
        resp.append({"name": name, "url": url})
    return resp


if __name__ == '__main__':
    root_urls = [
        {"name": "110學年度 袋鼠班 教學活動",
            "url": "http://tw.class.uschoolnet.com/class/?csid=css000000256274&id=model8&cl=1630661127-8083-580&page=1"},
        {"name": "110學年度 袋鼠班 戶外教學活動",
            "url": "http://tw.class.uschoolnet.com/class/?csid=css000000256274&id=model8&cl=1630035940-9464-2427&page=1"},
    ]
    for idx, entry in enumerate(root_urls):
        print("No. {0} -> name: {1}".format(idx, entry['name']))
    idx = input("Please input the No. you want to download photos: ")
    selected_entry = root_urls[int(idx)]
    print("Name: {0}, Root URL: {1}".format(
        selected_entry["name"], selected_entry["url"]))

    topics = get_topics(selected_entry["url"])
    all_idx = list(range(len(topics)))
    for idx, topic in enumerate(topics):
        print("No. {0} -> name: {1}".format(idx, topic['name']))
        logger.debug("Url: {0}\n".format(topic["url"]))

    is_all = input("Do you want to download all photos? [Y/N]: ")
    if not "yes" in is_all.lower() and not "y" in is_all.lower():
        no = input("Please input the No. you want to download photos: ")
        idx_list = [int(no)]
    else:
        idx_list = all_idx

    confirm = input(
        "Ready to download topic No: {0}. Please confirm? [Y/N] ".format(idx_list))
    if not "yes" in confirm.lower() and not "y" in confirm.lower():
        sys.exit(0)
    for idx in idx_list:
        topics[idx]["name"]
        urls = get_page_urls(topics[idx]["url"])
        for url in urls:
            print("Ready to crawl photo inside {0}".format(
                url))
            crawl_photos(url)
