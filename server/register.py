"""Registers flows to be managed by the Prefect Backend.
"""

from configparser import ConfigParser

from src.flows.e2e_pipeline import e2e_pipeline
from prefect.storage import GitHub

from prefect.engine.executors import DaskExecutor
from prefect.engine.results.azure_result import AzureResult
from prefect.engine.results.s3_result import S3Result
from prefect.engine.results.local_result import LocalResult


# Get configs
config = ConfigParser(allow_no_value=True)
config.read('configs/pipeline.ini')

PROJECT_NAME = config.get('prefect', 'PROJECT_NAME')
RESULT_SUBCLASS = config.get('prefect', 'RESULTS_SUBCLASS')
AZURE_RESULT_CONTAINER = config.get('prefect', 'LOCAL_RESULTS_DIR')
S3_RESULT_BUCKET = config.get('prefect', 'LOCAL_RESULT_DIR')
LOCAL_RESULT_DIR = config.get('prefect', 'LOCAL_RESULT_DIR')
DASK_SCHEDULER_ADDR = config.get('prefect', 'LOCAL_RESULTS_DIR')
GITHUB_STORAGE_REPO = config.get('prefect', 'GITHUB_STORAGE_REPO')
GITHUB_FLOWS_PATH = config.get('prefect', 'GITHUB_FLOWS_PATH')


# Prefect configs
gh_storage_kwargs = {
    'repo': GITHUB_STORAGE_REPO,
    'access_token_secret': 'GITHUB_ACCESS_TOKEN'
}
executer = DaskExecutor(address=DASK_SCHEDULER_ADDR)
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

# Set Flow Executer
e2e_pipeline.executer = executer

# Set Flow Result
e2e_pipeline.result = result

# Register Flows
e2e_pipeline.register(project_name=PROJECT_NAME)


if __name__ == "__main__":
    pass
