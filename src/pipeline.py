"""This module contains data workflows (AKA pipeline) of data tasks from
proprocessing, to modelling, and lastly post-processing. Data workflows in
`streamlit-e2e-boilerplate` are orchestrated using Prefect.
"""

from prefect import Flow
from prefect import Parameter
from .tasks import retrieve_data
from .tasks import clean_data
from .tasks import transform_data
from .tasks import encode_data
from .tasks import wrangle_na
from .tasks import run_model
from .tasks import plot_confidence_intervals


with Flow('wrangle_na') as wrangle_na_pipeline:
    data = Parameter('data', required=True)
    na_strategy = Parameter('na_strategy', default='cc')
    wrangled_data = wrangle_na(data, na_strategy)


with Flow('e2e_pipeline') as e2e_pipeline:

    # Pipeline parameters
    url = Parameter('url', required=True)
    sep = Parameter('sep', default=',')
    is_cat = Parameter('is_cat', default=None)
    na_values = Parameter('na_values', default=None)
    na_method = Parameter('na_method', default='cc')
    cols_transf = Parameter('cols_transf', default=None)
    transf = Parameter('transf', default=None)
    endog = Parameter('endog', required=True)
    exog = Parameter('exog', required=True)

    # Preprocessing
    data = retrieve_data(url, sep)
    cleaned_data = clean_data(data, na_values, is_cat)
    wrangled_data = wrangle_na(cleaned_data, na_method)
    transformed_data = transform_data(wrangled_data, cols_transf, transf)
    encoded_data = encode_data(transformed_data)

    # Modelling
    res = run_model(encoded_data, y=endog, X=exog)

    # Postprocessing
    conf_int_chart = plot_confidence_intervals(res)


if __name__ == "__main__":
    pass
