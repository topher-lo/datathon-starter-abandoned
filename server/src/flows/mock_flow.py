"""This module implements a MapReduce wordcount program as a Flow
to test a distributed Prefect pipeline. This classic MapReduce program
was also chosen to demonstrate Prefect's Dask executor, which
`streamlit-e2e-boilerplate` deploys onto a Kubernetes cluster.

Note: this module is not meant to be an efficient solution to the word
counting problem. It is only meant to demonstrate distributed workflows
in Prefect.
"""

import itertools
import requests

from prefect import Parameter
from prefect import task
from prefect import Flow
from prefect import flatten


@task
def download_message(url):
    r = requests.get(url)
    message = r.text
    return message


@task
def split_message(message):
    return [line for line in message.splitlines()]


@task
def mapper(line):
    # Strip leading and trailing whitespace,
    # make lowercase, and split into tokens
    tokens = (line.strip()
                  .lower()
                  .split())
    # Return list of (token, 1) tuples
    return [(t.strip().lower(), 1) for t in tokens if t.isalpha()]


@task
def shuffler(token_tuples):
    # Sort tokens
    sorted_tokens = sorted(token_tuples, key=lambda x: x[0])
    # Partition tokens
    partitions = [(key, [value for _, value in group]) for key, group
                  in itertools.groupby(sorted_tokens, lambda x: x[0])]
    return partitions


@task
def reducer(partition):
    key, value = partition
    return (key, sum(value))


with Flow(name='mapreduce_wordcount') as mock_flow:

    url = Parameter('message', required=True)

    message = download_message(url)
    lines = split_message(message)
    token_tuples = mapper.map(lines)
    partitions = shuffler(flatten(token_tuples))
    token_counts = reducer.map(partitions)


if __name__ == "__main__":
    pass
