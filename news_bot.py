import asyncio
import feedparser
from telegram import Bot

import os
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

RSS_SOURCES = [
  "http://news.google.com/rss/search?q=산업재해&h1=ko&g1=KR&ceid=KR:ko",
  "http://news.google.com/rss/search?q=중대재해&h1=ko&g1=KR&ceid=KR:ko",
  "http://news.google.com/rss/search?q=산업안전+사고&h1=ko&g1=KR&ceid=KR:ko",
  "http://news.google.com/rss/search?q=산업보건+재해&h1=ko&g1=KR&ceid=KR:ko",
  "http://news.google.com/rss/search?q=건설현장+사고&h1=ko&g1=KR&ceid=KR:ko",
  "http://news.google.com/rss/search?q=산업안전보건법&h1=ko&g1=KR&ceid=KR:ko",
  "http://news.google.com/rss/search?q=위험물안전관리법&h1=ko&g1=KR&ceid=KR:ko",
  "http://news.google.com/rss/search?q=소방시설법&h1=ko&g1=KR&ceid=KR:ko",
]

KEYWORD_WHITELIST = ["산업재해", "중대재해", "산업안전", "산업보건", "안전사고", "추락", "끼임", "질식", "폭발", "화재사고", "산재", "근로자 사망", "작업중 사망"]
KEYWORD_BLACKLIST = ["안전자산", "안전마진"]
SENT_LOG_FILE = "sent_news.bot"

def load_sent_log():
  try:
    with open(SENT_LOG_FILE, "r", encoding="utf-8") as f:
      return set(line.strip() for line in f.readlines())
  except FileNotFoundError:
    return set()

def save_sent_log(sent_set):
  with open(SENT_LOG_FILE, "w", encoding="utf-8") as f:
    for link in sent_set:
      f.write(link+"\n")

def keyword_filter(title):
  return True
  
async def send_news():
  bot = Bot(token=TELEGRAM_TOKEN)
  sent_log = load_sent_log()
  new_sent = set(sent_log)

  for rss_url in RSS_SOURCES:
    feed = feedparser.parse(rss_url)
    for entry in feed.entries[:10]:
      title = entry.title
      link = entry.link
    
      if link in sent_log:
        continue
      if not keyword_filter(title):
        continue
      
      message = f"산업안전/재해 뉴스\n\n{title}\n\n {link}"
      await bot.send_message(chat_id=CHAT_ID, text=message)
      print(f"전송완료: {title}")
      new_sent.add(link)
  save_sent_log(new_sent)

if __name__ == "__main__":
  asyncio.run(send_news())
