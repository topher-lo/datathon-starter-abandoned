"""Registers flows to be managed by the Prefect Backend.
"""

from configparser import ConfigParser

from prefect.storage import GitHub
from prefect.executors import DaskExecutor

from prefect.engine.results.azure_result import AzureResult
from prefect.engine.results.s3_result import S3Result
from prefect.engine.results.local_result import LocalResult

from server.src.flows.e2e_pipeline import e2e_pipeline
from server.src.flows.mock_flow import mock_flow


# Get configs
config = ConfigParser(allow_no_value=True)
config.read('configs/pipeline.ini')

PROJECT_NAME = config.get('prefect', 'PROJECT_NAME')
RESULT_SUBCLASS = config.get('prefect', 'RESULT_SUBCLASS')
AZURE_RESULT_CONTAINER = config.get('prefect', 'AZURE_RESULT_CONTAINER')
S3_RESULT_BUCKET = config.get('prefect', 'S3_RESULT_BUCKET')
LOCAL_RESULT_DIR = config.get('prefect', 'LOCAL_RESULT_DIR')
DASK_SCHEDULER_ADDR = config.get('prefect', 'DASK_SCHEDULER_ADDR')
GITHUB_STORAGE_REPO = config.get('prefect', 'GITHUB_STORAGE_REPO')
GITHUB_FLOWS_PATH = config.get('prefect', 'GITHUB_FLOWS_PATH')


# Prefect configs

# Storage
gh_storage_kwargs = {
    'repo': GITHUB_STORAGE_REPO,
    'access_token_secret': 'GITHUB_ACCESS_TOKEN'
}

# Executer
executor = DaskExecutor(address=DASK_SCHEDULER_ADDR)

# Result
if RESULT_SUBCLASS == 'azure':
    result = AzureResult(container=AZURE_RESULT_CONTAINER)
elif RESULT_SUBCLASS == 's3':
    result = S3Result(bucket=S3_RESULT_BUCKET)
else:
    result = LocalResult(dir=LOCAL_RESULT_DIR)


# Set Flow Storage
e2e_pipeline.storage = GitHub(
    path=f'{GITHUB_FLOWS_PATH}/e2e_pipeline.py',
    **gh_storage_kwargs
)
mock_flow.storage = GitHub(
    path=f'{GITHUB_FLOWS_PATH}/mock_flow.py',
    repo='topher-lo/streamlit-e2e-boilerplate',
)


# Set Flow Executer
e2e_pipeline.executor = executor
mock_flow.executor = executor


# Set Flow Result
e2e_pipeline.result = result
mock_flow.result = result


if __name__ == "__main__":
    pass
