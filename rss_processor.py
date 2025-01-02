import feedparser
from bs4 import BeautifulSoup
import os
import requests
from requests.exceptions import RequestException

# URL of the RSS feed (replace with the actual URL)
rss_url = os.environ.get('RSS_URL', 'https://comicsdb.ru/rss')

def process_rss_feed(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        feed = feedparser.parse(response.content)
    except RequestException as e:
        print(f"Error fetching RSS feed: {e}")
        return []

    processed_items = []

    for entry in feed.entries:
        title = entry.title
        link = entry.link
        
        # Parse the description using BeautifulSoup
        description_html = entry.description
        soup = BeautifulSoup(description_html, 'html.parser')

        # Remove the image at the beginning of the description
        img_tag = soup.find('img')
        if img_tag:
            img_src = img_tag['src'] if 'src' in img_tag.attrs else ''
            img_tag.decompose()  # Remove the <img> tag

            # Find the new image and replace scale_avatar with scale_large
            if 'scale_avatar' in img_src:
                new_img_url = img_src.replace('scale_avatar', 'scale_large')
            else:
                new_img_url = img_src
        else:
            new_img_url = ''

        # Create a new entry format
        processed_item = {
            'title': title,
            'link': link,
            'description': str(soup),
            'media_thumbnail': new_img_url
        }
        processed_items.append(processed_item)

    return processed_items

def generate_rss():
    print("Starting RSS feed processing...")
    items = process_rss_feed(rss_url)

    rss_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    rss_content += '<rss version="2.0">\n'
    rss_content += '<channel>\n'
    rss_content += '<title>Translation DB</title>\n'
    rss_content += f'<link>{rss_url}</link>\n'
    rss_content += '<description>База переводов комиксов.</description>\n'

    for item in items:
        rss_content += '<item>\n'
        rss_content += f'<title>{item["title"]}</title>\n'
        rss_content += f'<link>{item["link"]}</link>\n'
        rss_content += f'<description>{item["description"]}</description>\n'
        rss_content += f'<media_thumbnail>{item["media_thumbnail"]}</media_thumbnail>\n'
        rss_content += '</item>\n'

    rss_content += '</channel>\n'
    rss_content += '</rss>'

    print("RSS feed processing completed.")
    return rss_content

