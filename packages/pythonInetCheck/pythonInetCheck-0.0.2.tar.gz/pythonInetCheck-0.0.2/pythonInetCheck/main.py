"""
main program to check if internet is available
"""
import notify2
import requests
import time
from config import *


def main_loop():
    """
    Description:
        main loop
    Parameters:
        :return: None
    """
    inet_status = False
    while True:
        inet_status, site_name = check_inet_status()
        if inet_status:
            status = "up"
        else:
            status = "down"
        notify(status, site_name)
        if not inet_status:
            time.sleep(60)
        else:
            time.sleep(300)


def check_inet_status():
    """
    Description:
        Checks the current status of internet connection with all loaded sites
    Parameters:
        :return: a tuple consisting of a bool of whether the internet is up and the site it connected or failed to
        connect to
    """
    status = []
    for site_name, url in WEB_SITES.items():
        site_is_up = check_site(url)
        status.append(site_is_up)
        if site_is_up:
            return True, site_name
    return False, "all loaded sites"


def check_site(site: str):
    """
    Description:
        checks if a site can be accessed
    Parameters:
        :param site:
        :return: True if site can be accessed False otherwise
    """
    try:
        req = requests.get(site)
    except Exception:
        return False
    if req.ok:
        return True
    return False


def notify(inet_status: str, site: str = "all loaded sites"):
    """
    Description:
        notifies the user via system notification
    Parameters:
        :param inet_status: "up" or "down" depending on the status of internet
        :param site: Default is "all loaded sites", the name of the site used
        :return: None
    """
    message = f"the inet status is {inet_status} on account of {site}"
    notify2.init("Inet Checker")
    notice = notify2.Notification("inet status", message)
    notice.show()


if __name__ == "__main__":
    main_loop()
