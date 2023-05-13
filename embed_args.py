import argparse
import logging
from pathlib import Path
import pandas as pd
import config
import helpers.hdbg as hdbg
import helpers.hparser as hparser
import prep_embed as prep
import embed_model as emb
import saver as sav 
import helpers.extract as ex 
import requests 
import json
import os 

"""
Load csv file and return embeddings.
Use as:
> embed_args.py \
    colorguru \
    --filename 'colorguru_embeddings.json'\
    --client 'yourcolorguru'
"""
_LOG = logging.getLogger(__name__)


def _add_download_args(
    parser: argparse.ArgumentParser,
) -> argparse.ArgumentParser:
    """
    Add the command line options for embeddings.
    """
    parser.add_argument(
        "csvfile",
        action="store",
        type=argparse.FileType('r'),
        help="Target File",
    )
    parser.add_argument(
        "--filename",
        action="store",
        required=True,
        type=str,
        help="Name of new json file",
    )
    parser.add_argument(
        "--client",
        action="store",
        required=True,
        type=str,
        help="Name of Client",
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
    dataframe = pd.read_csv(args.csvfile)
    filename = str(args.filename)
    client = str(args.client)
    df = prep.get_tokens(dataframe, client)
    input = prep.drop_cols(df)
    embedder = emb.SiteEmbeddings()
    embeddings = embedder.compute_doc_embeddings(input)
    # Save data to cd as json 
    saver = sav.SiteSaver()
    saver.save_json(embeddings, filename)


if __name__ == "__main__":
    _main(_parse())