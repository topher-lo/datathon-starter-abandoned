"""This module contains data workflows (AKA pipeline) of data tasks from
proprocessing, to modelling, and lastly post-processing. Data workflows in
`datathon-mlapp-starter` are orchestrated using Prefect.
"""

from prefect import Flow
from prefect import Parameter
from ..tasks.data import sanitize_col_names
from ..tasks.data import retrieve_data
from ..tasks.data import clean_data
from ..tasks.data import transform_data
from ..tasks.data import encode_data
from ..tasks.data import wrangle_na
from ..tasks.data import gelman_standardize_data
from ..tasks.data import run_model
from ..tasks.data import plot_confidence_intervals


with Flow(name='e2e_pipeline') as e2e_pipeline:

    # Pipeline parameters
    url = Parameter('url', required=True)
    sep = Parameter('sep', default=',')
    cat_cols = Parameter('cat_cols', default=None)
    na_values = Parameter('na_values', default=None)
    na_strategy = Parameter('na_strategy', default='cc')
    transf_cols = Parameter('transf_cols', default=None)
    transf_func = Parameter('transf_func', default=None)
    endog = Parameter('endog', required=True)
    exog = Parameter('exog', required=True)

    # Sanitize column names
    cat_cols = sanitize_col_names(cat_cols)
    transformed_cols = sanitize_col_names(transf_cols)
    endog = sanitize_col_names(endog)
    exog = sanitize_col_names(exog)

    # Preprocessing
    data = retrieve_data(url, sep)
    cleaned_data = clean_data(data, na_values, cat_cols)
    encoded_data = encode_data(cleaned_data)
    wrangled_data = wrangle_na(encoded_data, na_strategy)
    transformed_data = transform_data(wrangled_data,
                                      transformed_cols,
                                      transf_func)
    standardized_data = gelman_standardize_data(transformed_data)

    # Modelling
    res = run_model(standardized_data, y=endog, X=exog)

    # Postprocessing
    conf_int_chart = plot_confidence_intervals(res)


if __name__ == "__main__":
    pass
