import argparse
import logging
from pathlib import Path
import pandas as pd

import helpers.hdbg as hdbg
import helpers.hparser as hparser

import download_site as dwd 
import saver as sav 
import helpers.extract as ex 
import requests 
"""
Download data from sitemap and save it as csv.
Use as:
> download_args.py \
    --list_of_websites "https://hudsonhardwood.com/" \
    --client 'hudsonhardwood' 
"""
_LOG = logging.getLogger(__name__)


def _add_download_args(
    parser: argparse.ArgumentParser,
) -> argparse.ArgumentParser:
    """
    Add the command line options for download.
    """
    parser.add_argument(
        "--list_of_websites",
        required=True,
        action="store",
        nargs="+",
        help="Target URL",
    )
    parser.add_argument(
        "--client",
        action="store",
        required=True,
        type=str,
        help="Client Name",
    )
    return parser


def _parse() -> argparse.ArgumentParser:
    hdbg.init_logger(use_exec_path=True)
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser = _add_download_args(parser)
    parser = hparser.add_verbosity_arg(parser)
    return parser


def _main(parser: argparse.ArgumentParser) -> None:
    args = parser.parse_args()
    # Load data.
  
    list_of_websites = args.list_of_websites
    client = str(args.client)
    downloader = dwd.SiteDownloader()
    raw_data, df, datadict = downloader.download(list_of_websites, client)
    # Save data to cd as csv
    saver = sav.SiteSaver()
    saver.save(raw_data, client)


if __name__ == "__main__":
    _main(_parse())