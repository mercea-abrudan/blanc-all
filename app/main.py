import argparse
import os

from block import BlockingManager
from commands import BlockSiteCommand
from commands import ListBlockedSitesCommand
from commands import RestoreHostsCommand
from commands import UnblockSiteCommand
from commands import UnblockAllSitesCommand
from utils import copy_file, get_hosts_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Block, unblock or list websites via the hosts file."
    )
    parser.add_argument(
        "action",
        choices=["block", "unblock", "list", "restore"],
        help="Actions to perform.",
    )
    parser.add_argument(
        "target",
        nargs="?",
        help="The website to block/unblock (e.g., example.com) or '--all'.",
    )
    # parser.add_argument(
    #     "-m", "--minutes", type=int, help="Duration in minutes for temporary blocking."
    # )
    # parser.add_argument(
    #     "-s",
    #     "--sites",
    #     nargs="+",
    #     help="List of sites to block/unblock (used with -all).",
    # )

    args = parser.parse_args()
    hosts_file = get_hosts_path()
    command = None

    if not os.path.exists(r"../data/original_hosts"):
        try:
            copy_file(hosts_file, r"../data/original_hosts")
        except Exception as e:
            print(f"An error occured during copy: {e}")
    blocking_manager = BlockingManager(hosts_file)

    if args.action == "block":
        if args.target:
            if args.target == '--all':
                print(f"Blocking access to all sites is not supported yet.")
            else:
                command = BlockSiteCommand(blocking_manager, args.target)
        else:
            print("Please specify a website to block.")

    elif args.action == "unblock":
        if args.target:
                if args.target == '--all':
                    command = UnblockAllSitesCommand(args.sites, blocking_manager)
                else:
                    command = UnblockSiteCommand(blocking_manager, args.target)
        else:
            print("Please specify a website to unblock.")

    elif args.action == "list":
        command = ListBlockedSitesCommand(blocking_manager)
    
    elif args.action == "restore":
        command = RestoreHostsCommand(blocking_manager)

    if command:
        command.execute()
