import os
from abc import ABC, abstractmethod
from utils import copy_file
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


class UnblockAllSitesCommand(Command):
    def __init__(self, blocking_manager):
        self.blocking_manager = blocking_manager

    def execute(self):
        blocked_sites = self.blocking_manager.get_blocked_sites()
        if blocked_sites:
            for site in blocked_sites:
                self.blocking_manager.unblock(site)
        print(f"Access to all sites has been unblocked.")


class RestoreHostsCommand(Command):
    def __init__(self, blocking_manager):
        self.blocking_manager = blocking_manager

    def execute(self):
        if os.path.exists(r"../data/original_hosts"):
            try:
                copy_file(r"../data/original_hosts", self.blocking_manager.hosts_path)
                print("Hosts file has been restored to its original state.")
            except Exception as e:
                print(f"An error occured during restore: {e}")


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
