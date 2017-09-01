import gzip
import collections
import json


def write(fp, data: collections.Sequence) -> None:
    jsoned=json.dumps(data).encode()
    gzipped=gzip.compress(bytes(jsoned))

    fp.write(gzipped)


def read(fp) -> collections.Sequence:
    gzipped=fp.read()
    jsoned=gzip.decompress(gzipped).decode()

    return json.loads(jsoned)
