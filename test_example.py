import re
import asyncio
import xmltodict
import requests

from dateutil.parser import parse as date_parse
from aiohttp.client import ClientSession
from pymongo import MongoClient
from bs4 import BeautifulSoup
import opengraph_py3

url = "https://blogs.windows.com/windows-insider/feed/"
user_agent = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

async def fetchFeed(url: str, headers: dict) -> str:
    """fetches the feed"""
    async with ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise RuntimeError("Invalid status code: {0}".format(response.status))
            return await response.read()

def cleanText(text: str) -> str:
    processed_text = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', text)
    return processed_text


def parse_text(text: str):
    soup = BeautifulSoup(text, "lxml")
    return soup.get_text()


loop = asyncio.get_event_loop()
res = loop.run_until_complete(fetchFeed(url, user_agent))
rs = dict(xmltodict.parse(xml_input=res, process_namespaces=True))
a = dict(dict(rs["rss"])["channel"])["item"]


stroge = []

for i in a:
    title = i["title"]
    link = i["link"]
    pubDate = date_parse(i["pubDate"]).astimezone().strftime('%Y-%m-%d %H:%M:%S %z')
    description = parse_text(i["description"])
    stroge.append(dict(title=title, link=link, pubDate=pubDate, description=description))


ad = stroge[0]["link"]

r = requests.get(url=ad, headers=user_agent)

soup = BeautifulSoup(r.text, 'lxml')
# data holder
data = {
    "tag": {},
    "ogp": {}
}
# find all the meta tags in the web page
for i in soup.find_all("meta"):
    # extract individual tag with the property value
    if i.get("property", None) == "og:title":
        data["tag"]["title"] = i
        data["ogp"]["title"] = i.get("content", None)
    if i.get("property", None) == "og:url":
        data["tag"]["url"] = i
        data["ogp"]["url"] = i.get("content", None)
    if i.get("property", None) == "og:description":
        data["tag"]["description"] = i
        data["ogp"]["description"] = i.get("content", None)
    if i.get("property", None) == "og:image":
        data["tag"]["image"] = i
        data["ogp"]["image"] = i.get("content", None)
    if i.get("property", None) == "og:type":
        data["tag"]["type"] = i
        data["ogp"]["type"] = i.get("content", None)
    if i.get("property", None) == "og:site_name":
        data["tag"]["site_name"] = i
        data["ogp"]["site_name"] = i.get("content", None)
    if i.get("property", None) == "og:locale":
        data["tag"]["locale"] = i
        data["ogp"]["locale"] = i.get("content", None)

print(data["ogp"]["image"])
def pprint(data):
    import ujson
    json = ujson.dumps(data, sort_keys=True, indent=4, escape_forward_slashes=False)
    print(json)

"""
client = MongoClient('localhost', 27017)
db = client["WIB"]
last_feed = db.last_feed

source = last_feed.find_one().get("feeds")

# def pprint(data):
#     json = ujson.dumps(data, sort_keys=True, indent=4, escape_forward_slashes=False)
#     print(json)

# pprint(source)
# pprint(stroge)

if source == None:
    last_feed.insert_one({"feeds": stroge})
    raise RuntimeError("No previous feed found")

if source == stroge:
    print("No Change")
else:
    print("Change")
    last_feed.update_one({"feeds": source}, {"$set": {"feeds": stroge}})
"""