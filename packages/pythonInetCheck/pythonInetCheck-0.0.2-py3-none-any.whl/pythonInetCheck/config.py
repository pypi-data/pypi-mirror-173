"""
Loads and stores websites to be used in main file
"""
import json
import os

JSON_FILES = []
WEB_SITES = {
    "google": "https://www.google.com",
    "bing": "https://www.bing.com",
    "youtube": "https://www.youtube.com",
    "wikipedia": "https://www.wikipedia.org",
    "yahoo": "https://www.yahoo.com",
    "facebook": "https://www.facebook.com"
}

if len(JSON_FILES) >= 1:
    for file in JSON_FILES:
        try:
            with open(file) as f:
                WEB_SITES.update(json.load(f))
        except Exception:
            pass
