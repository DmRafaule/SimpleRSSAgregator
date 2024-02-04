import functools
from datamanager import DataManager
# To manage time
from utils import GetNewItems, GetOldItems


def displayer():
    def decorator_repeat(func):
        @functools.wraps(func)
        def wrapper_debug(*args, **kwargs):
            args = list(args)
            items = args[0]
            items_to_display = []
            dm = DataManager()
            display_option = dm.data['display']
            match display_option:
                case 'new':
                    source = items[0]['title_detail']['base']
                    items_to_display = GetNewItems(source)
                    if len(items_to_display) == 0:
                        print("There is no new items in feed")
                case 'old':
                    source = items[0]['title_detail']['base']
                    items_to_display = GetOldItems(source)
                case 'all':
                    items_to_display = items
            args[0] = items_to_display
            func(*args, **kwargs)
        return wrapper_debug
    return decorator_repeat
