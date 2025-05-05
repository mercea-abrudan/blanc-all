import argparse
# import sys

from utils import copy_file, get_hosts_path
# from block import BlockingManager
# from block import ListBlockedSitesCommand


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Block, unblock, list, or restore websites via the hosts file."
    )
    parser.add_argument(
        "action",
        choices=["block", "restore", "unblock", "list"],
        help="Action to perform.",
    )
    parser.add_argument(
        "target",
        nargs="?",
        help="The website to block/unblock (e.g., facebook.com) or '-all'.",
    )
    parser.add_argument(
        "-m", "--minutes", type=int, help="Duration in minutes for temporary blocking."
    )
    parser.add_argument(
        "-s",
        "--sites",
        nargs="+",
        help="List of sites to block/unblock (used with -all).",
    )

    args = parser.parse_args()
    hosts_file = get_hosts_path()
    copy_file(hosts_file, r"../data/original_hosts")
    # blocking_manager = BlockingManager(hosts_file)

    # try:
    #     with open(hosts_file, 'r') as f:
    #         original_hosts_content = f.read()
    # except IOError as e:
    #     print(f"Error reading the hosts file: {e}")
    #     sys.exit(1)

    # command = None

    if args.action == "":
        pass

    # if args.action == 'block':
    #     if args.target:
    #         if args.target == '-all':
    #             if args.sites:
    #                 command = BlockAllCommand(args.sites, blocking_manager, args.minutes)
    #             else:
    #                 print("Please specify sites to block with '-all' using the '-s' option.")
    #         else:
    #             command = BlockSiteCommand(args.target, blocking_manager, args.minutes)
    #     else:
    #         print("Please specify a website to block or use '-all'.")

    # elif args.action == 'unblock':
    #     if args.target:
    #         if args.target == '-all':
    #             if args.sites:
    #                 command = UnblockAllCommand(args.sites, blocking_manager)
    #             else:
    #                 print("Please specify sites to unblock with '-all' using the '-s' option.")
    #         else:
    #             command = UnblockSiteCommand(args.target, blocking_manager)
    #     else:
    #         print("Please specify a website to unblock or use '-all'.")

    # elif args.action == 'restore':
    #     command = RestoreHostsCommand(hosts_file, original_hosts_content)
    #     # Optionally clear the blocking manager's state on restore
    #     blocking_manager.indefinitely_blocked.clear()
    #     blocking_manager.temporarily_blocked.clear()
    #     blocking_manager._save_state()

    # elif args.action == 'list':
    #     command = ListBlockedSitesCommand(blocking_manager)

    # if command:
    #     command.execute()
