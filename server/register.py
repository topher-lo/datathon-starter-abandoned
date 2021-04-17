"""Registers flows to be managed by the Prefect Backend.
"""

import logging

from configparser import ConfigParser
from typing import List
from prefect import Flow

from prefect.storage import Docker
from prefect.executors import DaskExecutor
from prefect.executors import LocalExecutor

from prefect.engine.results import AzureResult
from prefect.engine.results import S3Result
from prefect.engine.results import LocalResult

from server.src.flows.data import e2e_pipeline
from server.src.flows.mock import mapreduce_wordcount


# CONFIGS

# Get configs
config = ConfigParser(allow_no_value=True)
config.read('setup.cfg')
config.read('configs/pipeline.ini')

# Project name
PROJECT_NAME = config.get('metadata', 'name')
# URL to Docker registry to store Flow scripts
REGISTRY_URL = config.get('prefect.storage', 'REGISTRY_URL')
# Dask scheduler address to be used in DaskExecutor
DASK_SCHEDULER_ADDR = config.get('prefect.executor', 'DASK_SCHEDULER_ADDR')
# Configs for Result subclass
RESULT_SUBCLASS = config.get('prefect.result', 'RESULT_SUBCLASS')
AZURE_RESULT_CONTAINER = config.get('prefect.result', 'AZURE_RESULT_CONTAINER')
S3_RESULT_BUCKET = config.get('prefect.result', 'S3_RESULT_BUCKET')
LOCAL_RESULT_DIR = config.get('prefect.result', 'LOCAL_RESULT_DIR')


# FLOWS CONFIGURATION

# Get python requirements
PYTHON_DEPENDENCIES = [
    line for line in config.get('options.extras_require', 'flows').splitlines()
]

# Storage
storage_kwargs = {
    'dockerfile': './Dockerfile',
    'registry_url': REGISTRY_URL,
    'stored_as_script': True,
    'python_dependencies': PYTHON_DEPENDENCIES,
}
storage = Docker(**storage_kwargs)

# Executer
dask_executor = DaskExecutor(address=DASK_SCHEDULER_ADDR)
local_executor = LocalExecutor()

# Result
if RESULT_SUBCLASS == 'azure':
    result = AzureResult(container=AZURE_RESULT_CONTAINER)
elif RESULT_SUBCLASS == 's3':
    result = S3Result(bucket=S3_RESULT_BUCKET)
else:
    result = LocalResult(dir=LOCAL_RESULT_DIR)


# Set flow storage
e2e_pipeline.storage = storage
mapreduce_wordcount.storage = storage


# Set flow executer
e2e_pipeline.executor = local_executor
mapreduce_wordcount.executor = dask_executor


# Set flow result
e2e_pipeline.result = result
mapreduce_wordcount.result = result


# Declare flows
FLOWS = [
    e2e_pipeline,
    mapreduce_wordcount
]


# Build flows
def build_flows(flows: List[Flow],
                project_name: str = PROJECT_NAME):
    for flow in flows:
        logging.info(flow.name)
        flow.validate()
        flow.register(project_name=project_name,
                      idempotency_key=flow.serialized_hash())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    build_flows(flows=FLOWS)
