import functools
import logging
import os
import pprint
import sys
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple, Type, Union
from trafilatura.sitemaps import sitemap_search
from tqdm import tqdm #creates a smart progress bar for loops
from trafilatura import fetch_url, extract

# This module can depend only on:
# - Python standard modules
# - `helpers/hserver.py`

_LOG = logging.getLogger(__name__)

def get_urls_from_sitemap(resource_url: str) -> list:
    """
    Get a list of urls from a sitemap with trafilatura
    Call sitemap_search() with input url
    """
    urls = sitemap_search(resource_url)
    return urls
def extract_article(url: str) -> dict:
    """
    Extract text content from a url
    Call fetch_url() function from trafilatura
    Call extract() function to get text 
    """
    downloaded = fetch_url(url) 
    article = extract(downloaded, favor_precision=True)
    return article