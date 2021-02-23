"""This module contains data workflow (AKA pipeline) of data tasks from
proprocessing, to modelling, and lastly post-processing. The data workflow
is orchestrated using Prefect.
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

    data = retrieve_data



if __name__ == "__main__":
    pass