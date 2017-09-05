import gzip
import collections
import json
import os

__vocabulary_search_paths=[
    os.path.dirname(os.path.realpath(__file__)) + '/vocabularies/{}',
    '{}',
    os.getcwd() + '/{}',
    os.getenv('HOME') + '/.fakr/{}',
]

def write(fp, data: collections.Sequence) -> None:
    jsoned=json.dumps(data).encode()
    gzipped=gzip.compress(bytes(jsoned))

    fp.write(gzipped)


def read(fp) -> collections.Sequence:
    gzipped=fp.read()
    jsoned=gzip.decompress(gzipped).decode()

    return json.loads(jsoned)


def search(file: str) -> str:
    for p in __vocabulary_search_paths:
        guess=os.path.realpath(p.format(file))
        if os.path.isfile(guess):
            return guess

    return file
