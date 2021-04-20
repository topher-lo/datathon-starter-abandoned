"""Registers flows to be managed by the Prefect Backend.
"""

import logging

from configparser import ConfigParser
from typing import List
from prefect import Flow

from prefect.run_configs import KubernetesRun
from prefect.storage import Docker
from prefect.executors import DaskExecutor
from prefect.executors import LocalExecutor

from prefect.engine.results import AzureResult
from prefect.engine.results import S3Result
from prefect.engine.results import LocalResult

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

# Run config
run_config = KubernetesRun()

# Storage
FLOWS_DIR_PATH = '/opt/server/src/flows'
storage_kwargs = {
    'dockerfile': 'server/Dockerfile',
    'registry_url': REGISTRY_URL,
    'stored_as_script': True,
}

# Executer
local_executor = LocalExecutor()
dask_executor = DaskExecutor(address=DASK_SCHEDULER_ADDR)

# Result
if RESULT_SUBCLASS == 'azure':
    result = AzureResult(container=AZURE_RESULT_CONTAINER)
elif RESULT_SUBCLASS == 's3':
    result = S3Result(bucket=S3_RESULT_BUCKET)
else:
    result = LocalResult(dir=LOCAL_RESULT_DIR)


# Set flow run configs
mapreduce_wordcount.run_config = run_config


# Set flow storage
mapreduce_wordcount.storage = Docker(
    path=f'{FLOWS_DIR_PATH}/mock.py',
    **storage_kwargs
)


# Set flow executor
mapreduce_wordcount.executor = dask_executor


# Set flow result
mapreduce_wordcount.result = result


# Declare flows
FLOWS = [
    mapreduce_wordcount
]


# Build flows
def build_flows(flows: List[Flow],
                project_name: str = PROJECT_NAME):
    for flow in flows:
        logging.info(flow.name)
        logging.info(flow.run_config)
        logging.info(flow.storage)
        logging.info(flow.executor)
        logging.info(flow.result)
        flow.validate()
        flow.register(project_name=project_name,
                      idempotency_key=flow.serialized_hash())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    build_flows(flows=FLOWS)
