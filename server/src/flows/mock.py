"""This module implements a MapReduce wordcount program as a Flow
to test a distributed Prefect pipeline. This classic MapReduce program
was also chosen to demonstrate Prefect's Dask executor, which
`datathon-mlapp-starter` deploys onto a Kubernetes cluster.

Note: this module is not meant to be an efficient solution to the word
counting problem. It is only meant to demonstrate distributed workflows
in Prefect.
"""

from prefect import Parameter
from prefect import Flow
from prefect import flatten

from ..tasks.mock import download_message
from ..tasks.mock import split_message
from ..tasks.mock import mapper
from ..tasks.mock import shuffler
from ..tasks.mock import reducer


with Flow(name='mapreduce-wordcount') as mapreduce_wordcount:

    url = Parameter('url', required=True)

    message = download_message(url)
    lines = split_message(message)
    token_tuples = mapper.map(lines)
    partitions = shuffler(flatten(token_tuples))
    token_counts = reducer.map(partitions)


if __name__ == "__main__":
    pass
