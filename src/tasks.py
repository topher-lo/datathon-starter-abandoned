"""Individual data tasks (preprocessing, modelling, and postprocessing) are
encapsulated into the following functions:

--- Preprocessing ---

1. `retrieve_data(url, sep)`: retrieves data from a url, returns data
as a DataFrame

2. `_column_wrangler(data)`: transforms column names
into a consistent format

3. `_obj_wrangler(data)`: converts columns with
`object` dtype into `StringDtype`

4. `_factor_wrangler(data, is_factor)`:
converts columns in `is_factor` into `CategoricalDtype`

5. `_check_model_assumptions(data)`: empty function

6. `clean_data(data, is_factor, na_values)`:
a pandas pipeline of data wranglers

7. `transform_data(data)`: empty function

8. `encode_data(data)`:
transforms columns with `category` dtype
using `pd.get_dummies`. NA values for each categorical column
are represented by their own dummy column.

--- Modelling ---

9. `run_model(data, y, X)`: `statsmodels` linear regression implementation

--- Post-processing ---

10. `plot_confidence_intervals(result)`: given a fitted OLS model in
`statsmodels`, returns a box and whisker regression coefficient plot.

Note 1. Public functions (i.e. functions without a leading underscore `_func`)
are wrapped around Prefect's `@task` decorator.

Note 2. Empty functions (e.g. `_check_model_assumptions`) are
suggested data tasks for the boilerplate's user to implement.
For instance, the model assumptions of multiple linear regression
(i.e. no multicollinearity) might not apply for another model
(e.g. non-parametric models such as random forest).

Note 3. The implementations in functions 9. and 10. are simple examples only.
Replace the code within these functions to according to your data model.
"""

import datetime as dt
import numpy as np
import pandas as pd
import seaborn as sns

import statsmodels.api as sm

from prefect import task
from typing import List
from typing import Union
from typing import Mapping

from matplotlib.axes import Axes

from statsmodels.regression.linear_model import OLSResults


# Pre-processing

@task(max_retries=3, retry_delay=dt.timedelta(seconds=10))
def retrieve_data(url: str,
                  sep: str = ',',
                  nrows: Union[None, int] = None) -> pd.DataFrame:
    """Reads data (from url string) into a DataFrame.
    Assumes download data is a text file (a.k.a flat file).
    `sep` defaults to ',' accept CSV files.

    If `sep` is specified as None, the separator is automatically
    detected using Python's builtin sniffer tool `csv.sniffer`.

    `nrows` specifies the number of rows of the file to read. Useful
    for examining the header without downloading the entire file, or
    for reading pieces of large files.

    Note 1. pandas uses its super fast C engine to read flat files
    ONLY IF `sep` is explicitly given. Otherwise, it uses
    Python's parsing engine to automically detect the seperator
    and read the file. The Python engine is considerably slower.

    Note 2. pandas's input/output API supports an extensive range of
    data formats. See https://pandas.pydata.org/pandas-docs/dev/user_guide/io.html
    for more information. Change the code within this function to retrieve data
    from sources other than CSV (e.g. data stored on a SQL database).

    Note 3. ignores unnamed index columns.
    """
    data = pd.read_csv(url, sep=sep)
    # Remove unnamed index columns
    data = data.loc[:, ~data.columns.str.contains('Unnamed')]
    return data


def _column_wrangler(data: pd.DataFrame) -> pd.DataFrame:
    """Returns DataFrame with columns transformed into a consistent format:
    1. Stripped of all whitespaces at start and end
    2. Any excess whitespace in between are replaced with an underscore "_"
    3. All characters are lowercased
    """
    data.columns = (data.columns
                        .str.strip()
                        .str.replace(r' +', '_')
                        .str.lower())
    return data


def _obj_wrangler(data: pd.DataFrame) -> pd.DataFrame:
    """Converts columns with `object` dtype to `StringDtype`.
    """
    obj_cols = (data.select_dtypes(include=['object'])
                    .columns)
    data.loc[:, obj_cols] = (data.loc[:, obj_cols]
                                 .astype('string'))
    return data


def _factor_wrangler(
    data: pd.DataFrame,
    is_factor: Union[None, List[str]],
    categories: Union[None, Mapping[str, List[Union[str, int, float]]]]
) -> pd.DataFrame:
    """Converts columns in `is_factor` to `CategoricalDtype` dtype.
    TO DO: ordered / unordered AND set categories.
    """
    for col in is_factor:
        data.loc[:, col] = (data.loc[:, col]
                                .astype('categorical'))
    return data


def _check_model_assumptions(data: pd.DataFrame) -> pd.DataFrame:
    """To be implemented. Write checks for your model's assumptions.
    Consider throwing a ValueError exception if critical assumptions
    are violated.
    """
    return data


@task
def clean_data(
    data: pd.DataFrame,
    is_factor: Union[None, List[str]] = None,
    na_values: Union[None, List[Union[str, int, float]]] = None
) -> pd.DataFrame:
    """Data preprocessing pipeline. Relaces values in `na_values`
    with `np.nan` and runs the following data wranglers on `data`:
    1. _column_wrangler
    2. _obj_wrangler
    3._factor_wrangler
    4. _check_model_assumptions
    """
    data = (data.replace(na_values, np.nan)
                .pipe(_column_wrangler)
                .pipe(_obj_wrangler)
                .pipe(_factor_wrangler, is_factor=is_factor)
                .pipe(_check_model_assumptions))
    return data


@task
def transform_data(data: pd.DataFrame) -> pd.DataFrame:
    """To be implemented. Consider rescaling and log (or arcsine)
    transforming your data in this function.
    """
    return data


@task
def encode_data(data: pd.DataFrame, outcome_col: str) -> pd.DataFrame:
    """Transforms columns (not `outcome_col`) with `category` dtype
    using `pd.get_dummies`. Missing values for each categorical column
    are represented by their own dummy column.
    """
    data = (data.select_dtypes(include=['categorical'])
                .loc[:, ~outcome_col]
                .get_dummies(dummy_na=True))
    return data


# Modelling

@task
def run_model(data: pd.DataFrame,
              y: str,
              X: Union[str, List[str]]) -> OLSResults:
    """Runs a linear regression of y on X and returns
    a fitted OLS model in `statsmodels`. Replace the code
    within this function with your own model.
    """
    mod = sm.OLS(data[y], data[X])
    res = mod.fit()
    return res


# Post-processing

@task
def plot_confidence_intervals(res: OLSResults,
                              palette: str = 'spectral') -> Axes:
    """Returns a matplotlib axes containing a box and whisker
    Seaborn plot of regression coefficients' point estimates and
    confidence intervals.

    Set the plot's colour palette using `palette`.
    For a full list of colour palettes in Seaborn, check out:
    medium.com/@morganjonesartist/color-guide-to-seaborn-palettes-da849406d44f
    """
    conf_int = res.conf_int()  # 95% C.I.
    # Stack lower and upper columns
    conf_int = conf_int.stack()
    conf_int.name = "estimate"
    conf_int = pd.DataFrame(conf_int)
    conf_int = (conf_int.reset_index()
                        .rename(columns={'level_0': 'regressor',
                                         'level_1': 'interval'}))
    return sns.boxplot(x='regressor', y='estimate', data=conf_int)


if __name__ == "__main__":
    pass
