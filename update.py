import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import os

API_URL = "https://www.nhk.or.jp/radio-api/app/v1/web/ondemand/corners/new_arrivals"
MAX_EPISODES = 10

def fetch_episodes():
    res = requests.get(API_URL)
    data = res.json()
    episodes = []

    for item in data.get("data", [])[:MAX_EPISODES]:
        title = item.get("title", "NHKラジオニュース")
        pub_date = item.get("ondemand_publish_date", "")
        audio_url = item.get("ondemand_url", "")
        if not audio_url.endswith(".mp3"):
            continue

        episodes.append({
            "title": title,
            "pubDate": pub_date,
            "url": audio_url
        })

    return episodes

def build_rss(episodes):
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")

    ET.SubElement(channel, "title").text = "NHK Rolling Archive"
    ET.SubElement(channel, "link").text = "https://www.nhk.or.jp/radio/"
    ET.SubElement(channel, "description").text = "Latest NHKラジオニュース episodes"
    ET.SubElement(channel, "language").text = "ja"
    ET.SubElement(channel, "lastBuildDate").text = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

    for ep in episodes:
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = ep["title"]
        ET.SubElement(item, "pubDate").text = ep["pubDate"]
        ET.SubElement(item, "enclosure", url=ep["url"], type="audio/mpeg", length="12345678")
        ET.SubElement(item, "guid").text = ep["url"]

    tree = ET.ElementTree(rss)
    tree.write("feed.xml", encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    episodes = fetch_episodes()
    build_rss(episodes)
