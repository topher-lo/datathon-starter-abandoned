"""Registers flows to be managed by the Prefect Backend.
"""

from configparser import ConfigParser

from prefect.storage import Docker
from prefect.executors import DaskExecutor

from prefect.engine.results import AzureResult
from prefect.engine.results import S3Result
from prefect.engine.results import LocalResult

from server.src.flows.data import e2e_pipeline
from server.src.flows.mock import mapreduce_wordcount


# Get configs
config = ConfigParser(allow_no_value=True)
config.read('configs/pipeline.ini')

# Project name
PROJECT_NAME = config.get('prefect', 'PROJECT_NAME')
# URL to Docker registry to store Flow scripts
REGISTRY_URL = config.get('prefect', 'REGISTRY_URL')
# Dask scheduler address to be used in DaskExecutor
DASK_SCHEDULER_ADDR = config.get('prefect', 'DASK_SCHEDULER_ADDR')
# Configs for Result subclass
RESULT_SUBCLASS = config.get('prefect', 'RESULT_SUBCLASS')
AZURE_RESULT_CONTAINER = config.get('prefect', 'AZURE_RESULT_CONTAINER')
S3_RESULT_BUCKET = config.get('prefect', 'S3_RESULT_BUCKET')
LOCAL_RESULT_DIR = config.get('prefect', 'LOCAL_RESULT_DIR')


# Prefect configs

# Get python requirements
with open('./requirements/requirements-flow.txt') as f:
    PYTHON_DEPENDENCIES = [x.strip()for x in f.readlines()]

# Storage
storage_kwargs = {
    'dockerfile': './Dockerfile',
    'registry_url': REGISTRY_URL,
    'stored_as_script': True,
    'python_dependencies': PYTHON_DEPENDENCIES,
}
storage = Docker(**storage_kwargs)

# Executer
executor = DaskExecutor(address=DASK_SCHEDULER_ADDR)

# Result
if RESULT_SUBCLASS == 'azure':
    result = AzureResult(container=AZURE_RESULT_CONTAINER)
elif RESULT_SUBCLASS == 's3':
    result = S3Result(bucket=S3_RESULT_BUCKET)
else:
    result = LocalResult(dir=LOCAL_RESULT_DIR)


# Set Flow storage
e2e_pipeline.storage = storage
mapreduce_wordcount.storage = storage


# Set Flow Executer
e2e_pipeline.executor = executor
mapreduce_wordcount.executor = executor


# Set Flow Result
e2e_pipeline.result = result
mapreduce_wordcount.result = result


if __name__ == "__main__":
    pass
