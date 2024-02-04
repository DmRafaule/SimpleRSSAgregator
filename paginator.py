import functools
import os
from getkey import getkey, keys


# Must be used with function that has his first argument as a list of items to paginate
def paginator():
    def decorator_repeat(func):
        @functools.wraps(func)
        def wrapper_debug(*args, **kwargs):
            # convert tuple object to list (muteable)
            args = list(args)
            # save all sended items
            items = args[0]
            # set up how much items to display at once
            step = 5
            # define how long is to paginate
            offset = len(items)
            # set up first position of paginating items
            counter = 0
            # set up last position of paginating items
            offset_counter = step
            # until position of paginating items will be less than number of this items
            while counter < offset:
                # clear terminal screen
                os.system('cls||clear')
                # to be in touch where we are when paginate
                print(f"{counter}-{offset_counter}/{offset}")
                # make a slice of needed items.
                # from first positon to last
                args[0] = items[counter:offset_counter]
                # send args to function that gonna to display itemS
                func(*args, **kwargs)
                # feedback, press Space for next items
                print("To new page, press [SPACE]")
                counter += step
                offset_counter += step
                # wait until space is pressed
                while getkey() is not keys.SPACE:
                    pass
            else:
                print("End of list")
        return wrapper_debug
    return decorator_repeat
