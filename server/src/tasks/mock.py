import itertools
import requests

from prefect import task


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


if __name__ == "__main__":
    pass
