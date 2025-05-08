from abc import ABC, abstractmethod
from utils import is_valid_site


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass


class BlockSiteCommand(Command):
    def __init__(self, blocking_manager, site):
        self.site = site
        self.blocking_manager = blocking_manager

    def execute(self):
        if is_valid_site(self.site):
            self.blocking_manager.block(self.site)
            print(f"Access to {self.site} has been blocked.")
        else:
            print("Please specify a valid website to block.")


class UnblockSiteCommand(Command):
    def __init__(self, blocking_manager, site):
        self.site = site
        self.blocking_manager = blocking_manager

    def execute(self):
        self.blocking_manager.unblock(self.site)
        print(f"Access to {self.site} has been unblocked.")


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
                print(f"- {site}")
        else:
            print("No sites are currently blocked.")
