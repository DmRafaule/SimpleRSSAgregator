# To parse date from RSS feeds
import feedparser
from paginator import paginator
from displayer import displayer
# To save, load, update data and files
from datamanager import DataManager, Feed
from utils import DisplayItem, GetAllGroups, GetAllFeeds, SyncFeed, GetNumOfNewItemInFeed, GetNumOfNewItemInGroup


@displayer()
@paginator()
def DisplayFeed(items):
    for item in items:
        DisplayItem(item)


def interactiveChangeFeedGroup(parser, args):
    dm = DataManager()
    source = None
    while True:
        print("Select feed to change group name.\n")
        it = 0
        it_list = []
        for feed in dm.load():
            it_list.append(it)
            print(f"{it})\t{feed['source']}")
            it += 1
        key = int(input("\nSelect: "))
        if key in it_list:
            it = 0
            for feed in dm.load():
                if key == it:
                    source = feed['source']
                    break
                it += 1
            break
    group_new = input('Enter new feed group name: ')
    dm = DataManager()
    for feed in dm.load():
        if feed['source'] == source:
            feed['group'] = group_new
    dm.updateDataBase()


def ChangeFeedGroup(parser, args):
    source = args[0]
    group_new = args[1]
    dm = DataManager()
    for feed in dm.load():
        if feed['source'] == source:
            feed['group'] = group_new
    dm.updateDataBase()


def interactiveRenameGroup(parser, args):
    # Find all groups
    groups = GetAllGroups()
    group_old = None
    while True:
        # Print out all valid option to choose
        print("Select group to rename\n")
        for it, g in enumerate(groups):
            print(f"{it})\t{g}")
        # Make a decision
        key = int(input("\nSelect: "))
        # Assign a result of choosen group
        for it, g in enumerate(groups):
            if key == it:
                group_old = g
                break
        if group_old is not None:
            break

    group_new = input("\nType new group name: ")
    dm = DataManager()
    for feed in dm.load():
        if feed['group'] == group_old:
            print("Yes")
            feed['group'] = group_new

    dm.updateDataBase()


def RenameGroup(parser, args):
    group_old = args[0]
    group_new = args[1]
    dm = DataManager()
    for feed in dm.load():
        if feed['group'] == group_old:
            feed['group'] = group_new

    dm.updateDataBase()


def AddFeedToGroup(parser, args):
    url = args[0]
    group = args[1]
    feed = feedparser.parse(url)
    # Hack if empty string with '' will be sended
    if not len(url) >= 1:
        print("Error: Too short URL")
        exit(-1)
    # Check if feed is real
    if not feed['bozo'] or len(feed['entries']) > 0:
        dm = DataManager()
        feed_to_database = Feed({
            'group': group,
            'source': url,
            'time_updated': None,
        })
        dm.save(feed_to_database)
    else:
        print(f"Error: {feed['bozo_exception']}")


def RemoveFeedFromGroup(parser, args):
    feed = args[0]
    group = args[1]
    dm = DataManager()
    if group in GetAllGroups() and feed in GetAllFeeds():
        for feed_item in dm.load():
            if feed_item['source'] == feed:
                dm.data['feeds'].remove(feed_item)
        dm.updateDataBase()
    else:
        print("Error: There is no such feed or group.")


def interactiveRemoveFeedFromGroup(parser, args):
    # Find all groups
    groups = GetAllGroups()
    group = None
    while True:
        # Print out all valid option to choose
        print("Select group\n")
        for it, g in enumerate(groups):
            print(f"{it})\t{g}")
        # Make a decision
        key = int(input("\nSelect: "))
        # Assign a result of choosen group
        for it, g in enumerate(groups):
            if key == it:
                group = g
                break
        if group is not None:
            break

    dm = DataManager()
    while True:
        print("Select feed to remove from group.\n")
        it = 0
        it_list = []
        for feed in dm.load():
            if feed['group'] == group:
                it_list.append(it)
                print(f"{it})\t{feed['source']}")
                it += 1
        key = int(input("\nSelect: "))
        if key in it_list:
            it = 0
            for feed in dm.load():
                if feed['group'] == group:
                    if key == it:
                        dm.data['feeds'].remove(feed)
                        break
                    it += 1
            dm.updateDataBase()
            break


def RemoveGroup(parser, args):
    group = args[0]
    dm = DataManager()
    for feed in dm.load():
        if feed['group'] == group:
            dm.data['feeds'].remove(feed)
    dm.updateDataBase()


def interactiveRemoveGroup(parser, args):
    dm = DataManager()
    # Find all groups
    groups = GetAllGroups()

    while True:
        group = None
        # Print out all valid option to choose
        print("Select group to remove.\n")
        for it, g in enumerate(groups):
            print(f"{it})\t{g}")
        # Make a decision
        key = int(input("\nSelect: "))
        # Assign a result of choosen group
        for it, g in enumerate(groups):
            if key == it:
                group = g
        if group is not None:
            # Display feeds by group
            for feed in dm.load():
                if feed['group'] == group:
                    dm.data['feeds'].remove(feed)
            break


def ShowFeed(parser, args):
    feed = args[0]
    if feed in GetAllFeeds():
        feed_items = feedparser.parse(feed)['entries']
        SyncFeed(feed)
        DisplayFeed(feed_items)
    else:
        print("Error: This url is not in database.")


# Display all items in feed. Interactive selection.
def interactiveShowFeed(parser, args):
    dm = DataManager()
    while True:
        print("Select feed to view.\n")
        it = 0
        it_list = []
        for feed in dm.load():
            it_list.append(it)
            print(f"{it})\t{feed['source']}")
            it += 1
        key = int(input("\nSelect: "))
        if key in it_list:
            it = 0
            for feed in dm.load():
                if key == it:
                    feed_items = feedparser.parse(feed['source'])['entries']
                    SyncFeed(feed['source'])
                    DisplayFeed(feed_items)
                    break
                it += 1
            break


# Display all feed's items in group.
def ShowGroup(parser, args):
    group = args[0]
    dm = DataManager()
    groups = GetAllGroups()

    if group in groups:
        # Display feeds by group
        for feed in dm.load():
            if feed['group'] == group:
                print(feed['source'])
                feed_items = feedparser.parse(feed['source'])['entries']
                SyncFeed(feed['source'])
                DisplayFeed(feed_items)


# Display all feed's items in group. Interactive selection.
def interactiveShowGroup(parser, args):
    dm = DataManager()
    # Find all groups
    groups = GetAllGroups()

    while True:
        group = None
        # Print out all valid option to choose
        print("Select group to view.\n")
        for it, g in enumerate(groups):
            print(f"{it})\t{g}")
        # Make a decision
        key = int(input("\nSelect: "))
        # Assign a result of choosen group
        for it, g in enumerate(groups):
            if key == it:
                group = g
        if group is not None:
            # Display feeds by group
            for feed in dm.load():
                if feed['group'] == group:
                    print(feed['source'])
                    feed_items = feedparser.parse(feed['source'])['entries']
                    SyncFeed(feed['source'])
                    DisplayFeed(feed_items)
            break


# Display all available feeds.
def ShowAllFeeds(parser, args):
    dm = DataManager()
    print('Feeds:')
    for feed in dm.load():
        num_of_newone = f"+{GetNumOfNewItemInFeed(feed['source'])}"
        print(f"\t{feed['source']} {num_of_newone}")


def ShowAllGroups(parser, args):
    groups = GetAllGroups()
    print('Groups:')
    for group in groups:
        num_of_newone = f"+{GetNumOfNewItemInGroup(group)}"
        print(f"\t{group} {num_of_newone}")


def ShowAllFeedsByGroup(parser, args):
    group = args[0]
    dm = DataManager()
    print('Feeds:')
    for feed in dm.load():
        if feed['group'] == group:
            num_of_newone = f"+{GetNumOfNewItemInFeed(feed['source'])}"
            print(f"\t{feed['source']} {num_of_newone}")


def UpdateDisplayer(parser, args):
    display_option = args
    dm = DataManager()
    dm.data['display'] = display_option
    dm.updateDataBase()
