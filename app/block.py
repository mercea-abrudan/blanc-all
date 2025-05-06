import json
import time
from abc import ABC, abstractmethod
from app.utils import extract_blocked_site


class BlockingManager:
    def __init__(
        self, hosts_path, redirect="127.0.0.1", state_file="blocking_state.json"
    ):
        self.hosts_path = hosts_path
        self.redirect = redirect
        self.state_file = state_file
        self.indefinitely_blocked = set()
        self.temporarily_blocked = {}  # {site: unblock_timestamp}
        self._load_state()
        # Start a background thread for checking expiry (optional)
        # self._start_expiry_checker()

    def _load_state(self):
        try:
            with open(self.hosts_path, "r") as file:
                lines = file.readlines()
                for line in lines:
                    if line.endswith("blanc-all"):
                            blocked_site = extract_blocked_site(line)
                            if blocked_site:
                                if "until" in line:
                                    self.temporarily_blocked[blocked_site] = "time"
                                else:
                                    self.indefinitely_blocked.add(blocked_site)
        except FileNotFoundError:
            print("Hosts file is missing.")


    def _save_state(self):
        comment = "# blocked by blanc-all"
        try:
            with open(self.hosts_path, "a") as file:
                for blocked_site in self.indefinitely_blocked:
                    file.write(f"{self.redirect} {blocked_site}  {comment}")
                for blocked_site in self.temporarily_blocked.keys():
                    file.write(f"{self.redirect} {blocked_site}  {comment} until time")
        except FileNotFoundError:
            print("Hosts file is missing.")


    def _update_hosts_file(self):
        try:
            with open(self.hosts_path, "r+") as file:
                lines = file.readlines()
                file.seek(0)
                file.truncate()
                for line in lines:
                    if not (
                        line.startswith(self.redirect)
                        and any(site in line for site in self.get_blocked_sites())
                    ):
                        file.write(line)
                for site in self.get_blocked_sites():
                    if not any(f"{self.redirect} {site}" in line for line in lines):
                        file.write(f"{self.redirect} {site}\n")
        except IOError as e:
            print(f"Error accessing the hosts file: {e}")

    def _check_expired_blocks(self):
        expired_sites = [
            site
            for site, expiry in self.temporarily_blocked.items()
            if time.time() >= expiry
        ]
        for site in expired_sites:
            del self.temporarily_blocked[site]
        self._update_hosts_file()
        self._save_state()

    def get_blocked_sites(self):
        # self._check_expired_blocks()
        return list(self.indefinitely_blocked) + list(self.temporarily_blocked.keys())

    def block_indefinitely(self, site):
        self.indefinitely_blocked.add(site)
        self._update_hosts_file()
        self._save_state()

    # def block_temporarily(self, site, duration_minutes):
    #     expiry_time = time.time() + duration_minutes * 60
    #     self.temporarily_blocked[site] = expiry_time
    #     self._update_hosts_file()
    #     self._save_state()

    # def unblock(self, site):
    #     if site in self.indefinitely_blocked:
    #         self.indefinitely_blocked.remove(site)
    #     if site in self.temporarily_blocked:
    #         del self.temporarily_blocked[site]
    #     self._update_hosts_file()
    #     self._save_state()

    # Optional background thread approach:
    # def _expiry_checker_loop(self):
    #     while True:
    #         time.sleep(60)  # Check every minute
    #         self._check_expired_blocks()

    # def _start_expiry_checker(self):
    #     thread = threading.Thread(target=self._expiry_checker_loop, daemon=True)
    #     thread.start()


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass


# class BlockSiteCommand(Command):
#     def __init__(self, site, blocking_manager, duration_minutes=None):
#         self.site = site
#         self.blocking_manager = blocking_manager
#         self.duration_minutes = duration_minutes

#     def execute(self):
#         if self.duration_minutes is not None:
#             self.blocking_manager.block_temporarily(self.site, self.duration_minutes)
#             print(
#                 f"Access to {self.site} has been blocked
#                 for {self.duration_minutes} minutes."
#             )
#         else:
#             self.blocking_manager.block_indefinitely(self.site)
#             print(f"Access to {self.site} has been blocked indefinitely.")

# class UnblockSiteCommand(Command):
#     def __init__(self, site, blocking_manager):
#         self.site = site
#         self.blocking_manager = blocking_manager

#     def execute(self):
#         self.blocking_manager.unblock(self.site)
#         print(f"Access to {self.site} has been unblocked.")

# class RestoreHostsCommand(Command):
#     def __init__(self, hosts_path, original_content):
#         self.hosts_path = hosts_path
#         self.original_content = original_content

#     def execute(self):
#         try:
#             with open(self.hosts_path, 'w') as file:
#                 file.write(self.original_content)
#             print("Hosts file has been restored to its original state.")
#             # Optionally clear the blocking state as well
#             BlockingManager(self.hosts_path)._save_state()
#         except IOError as e:
#             print(f"Error accessing the hosts file: {e}")

# class BlockAllCommand(Command):
#     def __init__(self, sites_to_block, blocking_manager, duration_minutes=None):
#         self.sites_to_block = sites_to_block
#         self.blocking_manager = blocking_manager
#         self.duration_minutes = duration_minutes

#     def execute(self):
#         if self.duration_minutes is not None:
#             for site in self.sites_to_block:
#                 self.blocking_manager.block_temporarily(site, self.duration_minutes)
#             if self.sites_to_block:
#                 print(f"Access to {self.sites_to_block} has been blocked for {self.duration_minutes} minutes.")
#         else:
#             for site in self.sites_to_block:
#                 self.blocking_manager.block_indefinitely(site)
#             if self.sites_to_block:
#                 print(f"Access to {self.sites_to_block} has been blocked indefinitely.")
#             elif not self.sites_to_block:
#                 print("No sites specified to block.")

# class UnblockAllCommand(Command):
#     def __init__(self, sites_to_block, blocking_manager):
#         self.sites_to_block = sites_to_block
#         self.blocking_manager = blocking_manager

#     def execute(self):
#         for site in self.sites_to_block:
#             self.blocking_manager.unblock(site)
#         if self.sites_to_block:
#             print(f"Access to {self.sites_to_block} has been unblocked.")
#         else:
#             print("No sites specified to unblock.")


class ListBlockedSitesCommand(Command):
    def __init__(self, blocking_manager):
        self.blocking_manager = blocking_manager

    def execute(self):
        blocked_sites = self.blocking_manager.get_blocked_sites()
        if blocked_sites:
            print("Currently blocked sites:")
            for site in blocked_sites:
                if site in self.blocking_manager.temporarily_blocked:
                    expiry_time = self.blocking_manager.temporarily_blocked[site]
                    remaining_time = int(expiry_time - time.time())
                    print(
                        f"- {site} (Temporary, unblocks in {remaining_time // 60} minutes {remaining_time % 60} seconds)"
                    )
                else:
                    print(f"- {site} (Indefinite)")
        else:
            print("No sites are currently blocked.")
