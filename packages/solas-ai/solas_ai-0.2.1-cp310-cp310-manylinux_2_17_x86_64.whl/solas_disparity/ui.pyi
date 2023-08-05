import pandas as pd
import typing
from _typeshed import Incomplete
from rich import console as console
from solas_disparity import const as const
from typing import Any, Union

AUTO_FORMATTERS: Incomplete

def autoformatter() -> typing.Callable: ...

NA_REP: str

def is_in_ipynb() -> bool: ...
def df_to_html_defaults(obj: pd.DataFrame, is_notebook: bool = ...) -> dict: ...
def show(obj: Union[pd.DataFrame, Any], auto_format: bool = ...) -> None: ...
def init_notebook() -> None: ...
