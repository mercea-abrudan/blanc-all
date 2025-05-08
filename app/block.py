from utils import extract_blocked_site


class BlockingManager:
    def __init__(self, hosts_path, redirect="127.0.0.1"):
        self.hosts_path = hosts_path
        self.redirect = redirect
        self.blocked = {}  # {site: unblock_timestamp}
        self._load_cache()

    def _load_cache(self):
        try:
            with open(self.hosts_path, "r") as file:
                lines = file.readlines()
                for line in lines:
                    blocked_site = extract_blocked_site(line)
                    if blocked_site:
                        self.blocked[blocked_site] = 0
        except FileNotFoundError:
            print("Hosts file is missing.")
        except IOError as e:
            print(f"Error accessing the hosts file: {e}")

    def _add_to_hosts(self, site):
        comment = "# blocked by blanc-all"
        try:
            with open(self.hosts_path, "a") as file:
                file.write(f"{self.redirect} {site}  {comment}")
        except FileNotFoundError:
            print("Hosts file is missing.")
        except IOError as e:
            print(f"Error accessing the hosts file: {e}")

    def _remove_from_hosts(self, site):
        try:
            with open(self.hosts_path, "r+") as file:
                lines = file.readlines()
                file.seek(0)
                file.truncate()
                for line in lines:
                    if site not in line.split():
                        file.write(line)
        except FileNotFoundError:
            print("Hosts file is missing.")
        except IOError as e:
            print(f"Error accessing the hosts file: {e}")

    def get_blocked_sites(self):
        return list(self.blocked.keys())

    def block(self, site: str, duration: int = 0):
        if site in self.blocked:
            print("Site is already blocked.")
        else:
            self._add_to_hosts(site)
            self.blocked[site] = duration

    def unblock(self, site):
        if site in self.blocked:
            self._remove_from_hosts(site)
            del self.blocked[site]
        else:
            print("Site is not blocked.")
