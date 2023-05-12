import logging
import os
from typing import Any, Optional, Dict, Iterable, List, Set, Tuple, Type, Union
import pandas as pd
import common.save as sinsasav
import helpers.hdbg as hdbg
import common.download as sinsadow
import os
import json

_LOG = logging.getLogger(__name__)

class SiteSaver(sinsasav.DataSaver):
    """
    Class for Saving to CD
    """
    def __init__(self):
        self = self

    def save(
    self, data: sinsadow.RawData, client: str, *args: Any, **kwargs: Any
) -> None:
        """
        Save RawData storing a DataFrame to CD

        :param data: data to save as csv
        """
        hdbg.dassert_isinstance(data.get_data(), pd.DataFrame, "Only DataFrame is supported.")
        # Transform dataframe into list of tuples.
        df = data.get_data()
        cwd = os.getcwd()
        path = cwd + "/" + client 
        df.to_csv(path)

    def save_json(
    self, data: dict[tuple[str,str], list[float]], filename: str, *args: Any, **kwargs: Any
) -> None:
        """
        Save embeddings to CD

        :param data: data to save as json/txt
        """
        cwd = os.getcwd()
        path = cwd + "/" + filename
        with open(path, 'w') as f:
            json_string = json.dumps({str(k): v for k, v in data.items()})
            f.write(json_string)
        