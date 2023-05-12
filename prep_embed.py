import functools
import logging
import os
import pprint
import sys
import texthero as hero
import pandas as pd 
import config
import openai
from typing import Any, Optional

"""
Prepare file for embeddings.
- tokenize articles
- drop unwanted columns if exists
"""

_LOG = logging.getLogger(__name__)

def get_tokens(df: pd.DataFrame, client: str,  *args: Any, **kwargs: Any)-> pd.DataFrame:
    """
    Tokenize the article content and return
    the count of the number of tokens as 
    new column 'tokens'
    """
    df['article'] = df.article.apply(lambda s: client + ' ' +s)
    df['token'] = hero.tokenize(df['article'])
    tokens = []
    for idx, row in df.iterrows():
        tokens.append(len(row['token']))
    df['tokens'] = tokens
    return df

def drop_cols(df: pd.DataFrame):
    """
    Drop Unnamed: 0 and token cols
    if exists
    """
    df = df.drop(['Unnamed: 0', 'token'], axis=1, errors='ignore')
    df = df.set_index(["client", "url"])
    return df


def get_embedding(text: str, model: str="text-embedding-ada-002", *args: Any, **kwargs: Any) -> list[float]:
    openai.api_key = config.api_key
    result = openai.Embedding.create(
      model=model,
      input=text
    )
    return result["data"][0]["embedding"]