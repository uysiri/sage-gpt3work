import logging
import time
from typing import Any, Optional
import pandas as pd
import requests
from trafilatura.sitemaps import sitemap_search
from tqdm import tqdm #creates a smart progress bar for loops
from trafilatura import fetch_url, extract
import time
import os 
import common.download as ssandown
import helpers.extract as ex

_LOG = logging.getLogger(__name__)
###ok
class SiteDownloader(ssandown.DataDownloader):
    """
    Class for downloading Coingecko Data for ETH and BTC
    """

    # def __init__(self, api: str):
    #     self.api = api
    def __init__(self):
        self = self
        

    def download(
        self, list_of_websites: list, client: str, *args: Any, **kwargs: Any
    ) -> ssandown.RawData:
        data = []
        for website in tqdm(list_of_websites, desc="Websites"):
            urls = ex.get_urls_from_sitemap(website)
            for url in tqdm(urls, desc="URLs"):
                d = {
                    'url': url,
                    "article": ex.extract_article(url)
                }
                data.append(d)
                time.sleep(0.5)

        df = pd.DataFrame(data)
        df = df.drop_duplicates()
        df = df.dropna()
        df['client'] = client
        print(df.columns)
        # save as pandas df AND as dict

        _LOG.info(f"Downloaded data: \n\t {df.head(5)}")
        return ssandown.RawData(df), df, data

print('Done')