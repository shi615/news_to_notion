import feedparser
from datetime import datetime, timedelta
import requests

NOTION_API_URL = "https://api.notion.com/v1/pages"
NOTION_API_KEY = "<your_notion_api_key>"
NOTION_PAGE_ID = "<your_notion_database_id>"
NOTION_VERSION = "2022-06-28"

headers = {
  "Authorization": f"Bearer {NOTION_API_KEY}",
  "Content-Type": "application/json",
  "Notion-Version": NOTION_VERSION
}

def get_news_from_rss(url):
  feed = feedparser.parse(url)
  articles = [{'title': entry.title, 'link': entry.link, 'published': entry.published} for entry in feed.entries]
  
  return articles

def filter_articles_by_date(articles, start_timestamp, end_timestamp):
  filtered_articles = []
  
  for article in articles:
    published_date = datetime.strptime(article['published'], '%a, %d %b %Y %H:%M:%S %z')
    published_timestamp = published_date.timestamp()
    
    if start_timestamp <= published_timestamp <= end_timestamp:
      filtered_articles.append(article)

  return filtered_articles

def add_article_to_notion(title, link, published, inserted_date):
  # ISO 8601形式に日付を変換
  published_date = datetime.strptime(published, '%a, %d %b %Y %H:%M:%S %z').isoformat()

  data = {
    "parent": { "database_id": NOTION_PAGE_ID },
    "icon": {
      "emoji": "📰"
    },
    "properties": {
      "記事タイトル": {
        "title": [
          {
            "text": {
              "content": title
            }
          }
        ]
      },
      "リンク": {
        "url": link
      },
      "記事公開日": {
        "date": {
          "start": published_date
        }
      },
      "追加日": {
        "date": {
          "start": inserted_date
        }
      }
    }
  }

  response = requests.post(NOTION_API_URL, headers=headers, json=data)
  
  if response.status_code != 200:
    print(f"Failed to add article to Notion: {response.text}")
    
  response.raise_for_status()

def job():
  rss_urls = {
    "https://piyolog.hatenadiary.jp/rss"
  }
  
  now = datetime.now()
  end_date = datetime(now.year, now.month, now.day, 7, 0, 0)
  start_date = end_date - timedelta(days=1)
  
  end_timestamp = end_date.timestamp()
  start_timestamp = start_date.timestamp()
  
  date_filtered_news = []
  
  for rss_url in rss_urls:
    news = get_news_from_rss(rss_url)
    date_filtered_news += filter_articles_by_date(news, start_timestamp, end_timestamp)
    inserted_date = datetime.now().isoformat()

  for article in date_filtered_news:
    add_article_to_notion(article['title'], article['link'], article['published'], inserted_date)

if __name__ == "__main__":
  job()
