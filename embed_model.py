# load libraries
import openai
import os
import config
import pandas as pd
import numpy as np
import texthero as hero
import os 
import common.download as ssandown
import helpers.extract as ex
import logging
import abc
import prep_embed as prep
from typing import Any, Optional

_LOG = logging.getLogger(__name__)
###ok
class SiteEmbeddings:
    """
    Class for transforming embeddings
    """

    # def __init__(self, api: str):
    #     self.api = api
    def __init__(self):
        self = self

    def compute_doc_embeddings(self, df: pd.DataFrame, *args: Any, **kwargs: Any) -> dict[tuple[str,str], list[float]]:
        """
        Create an embedding for each row in the dataframe using the OpenAI Embeddings API function defined above.

        Returns a dictionary that maps between each embedding vector and the index of the row that it corresponds to.

        Format: tuple(client, article url): list[embeddings]
        """
        return {
            idx: prep.get_embedding(r.article) for idx, r in df.iterrows() 
        }

print('Done')