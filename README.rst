.. image:: https://travis-ci.org/l-x/fakr.svg?branch=master
    :target: https://travis-ci.org/l-x/fakr

.. image:: https://codecov.io/gh/l-x/fakr/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/l-x/fakr

Random data, fakrs!
===================

Installation
------------

From pypi:

>>> pip install fakr

From repo:

>>> git clone https://github.com/l-x/fakr.git && pip install -e fakr/


Basic Usage
-----------

>>> fakr --help

>>> echo "{{row}},{{row%100}},{{firstname}},{{lastname}},{{email}}" | fakr --count 1000

>>> curl "https://raw.githubusercontent.com/l-x/fakr/master/examples/templates/vcard.tpl" | fakr -c 100000 > vcard.vcf


Templates
---------

The templates you use for data generation are plain `Jinja2 Templates`_. See their reference for detailed information.

There are a few custom filters and function for use with fakr:

Custom filters:

- ``ascii``: Converts the value to ascii (using Unidecode_) (i. e. ``{{lastname|ascii}}``)
- ``shuffle``: Shuffles the value randomly (i. e. ``{{lastname|shuffle}}``)
- ``chance``: Gives the value a chance from 0.0 to 1.0 to be returned (i. e. ``{{firstname|chance(0.9)}}`` - firstname will be 90% returned, 10% empty)
- ``rjust``: Right-justifies the value to the given with (i. e. ``{{company|rjust(40)}}``)
- ``ljust``: Left-justifies the value to the given with (i. e. ``{{company|ljust(40)}}``)
- ``center``: Centers the value in width (i. e. ``{{company|center(40)}}``)

Custom functions:

- ``translate``
- ``uuid4``: Returns a new UUIDv4 on every call (i. e. ``{{uuid4()}}``)
- ``unixtime``: Returns a the current unixtime as float in seconds, (i. e. ``{{unixtime()}}``)



.. _`Jinja2 Templates`: http://jinja.pocoo.org/docs/2.9/templates/
.. _`Unidecode`: https://pypi.python.org/pypi/Unidecode