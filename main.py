#!/usr/bin/env python

# To control program via CLI
import argparse
from commandmanager import CommandManager
import callbacks as CB


parser = argparse.ArgumentParser(
        usage="python main.py [-h]",
        description="Simple agregator of RSS feeds. You choose and manage your own feeds",
        add_help=True,
)
command_manager = CommandManager()

parser.add_argument(
        '--new',
        action="store_const",
        const='new',
        help="Display only new items in feeds.",
        required=False,
)
command_manager.set("new", CB.UpdateDisplayer)

parser.add_argument(
        '--all',
        action="store_const",
        const='all',
        help="Display all items in feeds. Default",
        required=False,
)
command_manager.set("all", CB.UpdateDisplayer)

parser.add_argument(
        '--old',
        action="store_const",
        const='old',
        help="Display only old items in feeds.",
        required=False,
)
command_manager.set("old", CB.UpdateDisplayer)

functional_args = parser.add_mutually_exclusive_group()

functional_args.add_argument(
        "-a",
        type=str,
        help="Add new RSS feed to group",
        required=False,
        metavar=("URL", "GROUP"),
        nargs=2
)
command_manager.set("a", CB.AddFeedToGroup)

functional_args.add_argument(
        "-r",
        type=str,
        help="Rename feed group",
        required=False,
        metavar=("URL", "NEW_GROUP_NAME"),
        nargs=2
)
command_manager.set("r", CB.ChangeFeedGroup)

functional_args.add_argument(
        "-rI",
        action="append_const",
        const=True,
        help="Rename feed group. Interactive.",
        required=False,
)
command_manager.set("rI", CB.interactiveChangeFeedGroup)

functional_args.add_argument(
        "-R",
        type=str,
        help="Rename group",
        required=False,
        metavar=("OLD_GROUP_NAME", "NEW_GROUP_NAME"),
        nargs=2
)
command_manager.set("R", CB.RenameGroup)

functional_args.add_argument(
        "-RI",
        action="append_const",
        const=True,
        help="Rename group. Interactive.",
        required=False,
)
command_manager.set("RI", CB.interactiveRenameGroup)

functional_args.add_argument(
        "-d",
        type=str,
        help="Remove RSS feed from group",
        required=False,
        metavar=("URL", "GROUP"),
        nargs=2
)
command_manager.set("d", CB.RemoveFeedFromGroup)

functional_args.add_argument(
        "-dI",
        action="append_const",
        const=True,
        help="Remove RSS feed from group. Interactive.",
        required=False,
)
command_manager.set("dI", CB.interactiveRemoveFeedFromGroup)

functional_args.add_argument(
        "-D",
        type=str,
        help="Remove all RSS feeds in this group",
        required=False,
        metavar=("GROUP"),
        nargs=1
)
command_manager.set("D", CB.RemoveGroup)

functional_args.add_argument(
        "-DI",
        action="append_const",
        const=True,
        help="Remove all RSS feeds in this group. Interactive.",
        required=False,
)
command_manager.set("DI", CB.interactiveRemoveGroup)

functional_args.add_argument(
        "-v",
        type=str,
        nargs=1,
        help="Show RSS feed",
        metavar=("URL"),
        required=False,
)
command_manager.set("v", CB.ShowFeed)

functional_args.add_argument(
        "-vI",
        action="append_const",
        const=True,
        help="Show RSS feed. Interactive.",
        required=False,
)
command_manager.set("vI", CB.interactiveShowFeed)

functional_args.add_argument(
        "-vv",
        type=str,
        help="Show RSS feeds in group",
        required=False,
        metavar=("GROUP"),
        nargs=1
)
command_manager.set("vv", CB.ShowGroup)

functional_args.add_argument(
        "-vvI",
        help="Show RSS feeds in group. Interactive.",
        required=False,
        action="append_const",
        const=True,
)
command_manager.set("vvI", CB.interactiveShowGroup)

functional_args.add_argument(
        "-V",
        action="append_const",
        const=True,
        help="Show all RSS feeds",
        required=False,
)
command_manager.set("V", CB.ShowAllFeeds)

functional_args.add_argument(
        "-G",
        action="append_const",
        const=True,
        help="Show all groups.",
        required=False,
)
command_manager.set("G", CB.ShowAllGroups)

functional_args.add_argument(
        "-F",
        metavar=("GROUP"),
        nargs=1,
        help="Show all feeds in group.",
        required=False,
)
command_manager.set("F", CB.ShowAllFeedsByGroup)


setup_args = ['new', 'old', 'all']
args = parser.parse_args()
dict_args = vars(args)

isEmpty = True


# Handle only setup commands
for a in reversed(dir(args)):
    if a in setup_args:
        if dict_args[a] is not None:
            func = command_manager.get(a)
            func(parser, dict_args[a])


# Handle all commands by callbacks on each command
for a in reversed(dir(args)):
    if not a.startswith('__') and not callable(getattr(args, a)) and a not in setup_args:
        if dict_args[a] is not None:
            isEmpty = False
            func = command_manager.get(a)
            func(parser, dict_args[a])
