"""This module contains data workflows (AKA pipeline) of data tasks from
proprocessing, to modelling, and lastly post-processing. Data workflows in
`streamlit-e2e-boilerplate` are orchestrated using Prefect.
"""

from prefect import Flow
from prefect import Parameter
from configparser import ConfigParser
from .tasks import sanitize_col_names
from .tasks import retrieve_data
from .tasks import clean_data
from .tasks import transform_data
from .tasks import encode_data
from .tasks import wrangle_na
from .tasks import gelman_standardize_data
from .tasks import run_model
from .tasks import plot_confidence_intervals

from prefect.engine.results.local_result import LocalResult


# Get configs
config = ConfigParser()
config.read('pipeline.ini')

RESULTS_DIR = config.get('prefect', 'LOCAL_RESULTS_DIR')


with Flow('wrangle_na_pipeline',
          result=LocalResult(dir=RESULTS_DIR)) as wrangle_na_pipeline:
    url = Parameter('url', required=True)
    sep = Parameter('sep', default=',')
    strategy = Parameter('strategy', default='cc')
    data = retrieve_data(url, sep)
    wrangled_data = wrangle_na(data, strategy)


with Flow('e2e_pipeline',
          result=LocalResult(dir=RESULTS_DIR)) as e2e_pipeline:

    # Pipeline parameters
    url = Parameter('url', required=True)
    sep = Parameter('sep', default=',')
    cat_cols = Parameter('cat_cols', default=None)
    na_values = Parameter('na_values', default=None)
    na_strategy = Parameter('na_strategy', default='cc')
    transformed_cols = Parameter('transformed_cols', default=None)
    transf = Parameter('transf', default=None)
    endog = Parameter('endog', required=True)
    exog = Parameter('exog', required=True)

    # Sanitize column names
    cat_cols = sanitize_col_names(cat_cols)
    transformed_cols = sanitize_col_names(transformed_cols)
    endog = sanitize_col_names(endog)
    exog = sanitize_col_names(exog)

    # Preprocessing
    data = retrieve_data(url, sep)
    cleaned_data = clean_data(data, na_values, cat_cols)
    encoded_data = encode_data(cleaned_data)
    wrangled_data = wrangle_na(encoded_data, na_strategy)
    transformed_data = transform_data(wrangled_data, transformed_cols, transf)
    standardized_data = gelman_standardize_data(transformed_data)

    # Modelling
    res = run_model(standardized_data, y=endog, X=exog)

    # Postprocessing
    conf_int_chart = plot_confidence_intervals(res)


if __name__ == "__main__":
    pass
