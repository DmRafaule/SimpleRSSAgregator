from datamanager import DataManager
# To manage time
from datetime import datetime
# To parse date from RSS feeds
import feedparser


TIME_FORMAT = "%a, %d %b %Y %H:%M:%S"


def RemoveDateTimezone(time_in_str: str) -> str:
    anchor_pos = time_in_str.rfind(':')
    end = anchor_pos + 3
    return time_in_str[:end]


def ToDate(date_via_str: str) -> datetime:
    date_via_str = RemoveDateTimezone(date_via_str)
    date = None
    try:
        date = datetime.strptime(date_via_str, TIME_FORMAT)
    except:
        print("Can't read the date info. So, it will be null")

    return date


def DisplayItem(item: dict):
    print(f"title={item['title']}")
    print(f"link={item['link']}")
    print(f"published={item['published']}")
    print(f"summary={item['summary']}")
    print("\n")


# Find all groups
def GetAllGroups():
    dm = DataManager()
    groups = []
    for feed in dm.load():
        groups.append(feed['group'])
    groups = set(groups)
    return groups


# Find all feeds
def GetAllFeeds():
    dm = DataManager()
    feeds = []
    for feed in dm.load():
        feeds.append(feed['source'])
    feeds = set(feeds)
    return feeds


def SyncFeed(feed_url: str):
    dm = DataManager()
    for feed in dm.load():
        if feed['source'] == feed_url:
            date = datetime.today()
            feed['time_updated'] = str(date.strftime(TIME_FORMAT))
    dm.updateDataBase()


def GetNumOfNewItemInFeed(feed_url: str) -> int:
    new_items_num = 0
    dm = DataManager()
    for feed in dm.load():
        if feed['source'] == feed_url:
            # Obtain value from feed
            last_visit = feed['time_updated']
            # If it will be None then this means that we did't check
            # This feed yet
            if last_visit is not None:
                last_visit = ToDate(feed['time_updated'])
            feed = feedparser.parse(feed_url)
            for item in feed['entries']:
                item_date_published = ToDate(item['published'])
                # New item is those ones that appeared earlier than last visit
                # Of user
                if last_visit is None or last_visit < item_date_published:
                    new_items_num += 1
    return new_items_num


def GetNumOfNewItemInGroup(group_name: str) -> int:
    new_items_num = 0
    dm = DataManager()
    for feed in dm.load():
        if feed['group'] == group_name:
            # Obtain value from feed
            last_visit = feed['time_updated']
            # If it will be None then this means that we did't check
            # This feed yet
            if last_visit is not None:
                last_visit = ToDate(feed['time_updated'])
            feed_p = feedparser.parse(feed['source'])
            for item in feed_p['entries']:
                item_date_published = ToDate(item['published'])
                # New item is those ones that appeared earlier than last visit
                # Of user
                if last_visit is None or last_visit < item_date_published:
                    new_items_num += 1
    return new_items_num


def GetNewItems(feed_url: str) -> list:
    new_items = []
    dm = DataManager()
    for feed in dm.load():
        if feed['source'] == feed_url:
            # Obtain value from feed
            last_visit = feed['time_updated']
            # If it will be None then this means that we did't check
            # This feed yet
            if last_visit is not None:
                last_visit = ToDate(feed['time_updated'])
            items = feedparser.parse(feed['source'])['entries']
            for item in items:
                item_date_published = ToDate(item['published'])
                if last_visit is None or last_visit < item_date_published:
                    new_items.append(item)
        break
    return new_items


def GetOldItems(feed_url: str) -> list:
    old_items = []
    dm = DataManager()
    for feed in dm.load():
        if feed['source'] == feed_url:
            # Obtain value from feed
            last_visit = feed['time_updated']
            # If it will be None then this means that we did't check
            # This feed yet
            if last_visit is not None:
                last_visit = ToDate(feed['time_updated'])
            items = feedparser.parse(feed['source'])['entries']
            for item in items:
                item_date_published = ToDate(item['published'])
                if last_visit is None or last_visit > item_date_published:
                    old_items.append(item)
        break
    return old_items
