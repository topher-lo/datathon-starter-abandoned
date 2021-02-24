"""This module contains data workflows (AKA pipeline) of data tasks from
proprocessing, to modelling, and lastly post-processing. Data workflows in
`streamlit-e2e-boilerplate` are orchestrated using Prefect.
"""

from prefect import Flow
from prefect import Parameter
from tasks import retrieve_data
from tasks import clean_data
from tasks import transform_data
from tasks import encode_data
from tasks import run_model
from tasks import plot_confidence_intervals


with Flow('e2e_pipeline') as e2e_pipeline:
    # Pipeline parameters
    url = Parameter('url', required=True)
    sep = Parameter('sep', default=',')
    na_values = Parameter('na_values', default=None)
    is_factor = Parameter('is_factor', default=None)
    endog = Parameter('endog', required=True)
    exog = Parameter('exog', required=True)

    # Preprocessing
    data = retrieve_data(url, sep)
    clean_data = clean_data(data, is_factor, na_values)
    transformed_data = transform_data(clean_data)
    encoded_data = encode_data(transformed_data)

    # Modelling
    res = run_model(data, y=endog, X=exog)

    # Postprocessing
    conf_int_plot = plot_confidence_intervals(res)


if __name__ == "__main__":
    pass
