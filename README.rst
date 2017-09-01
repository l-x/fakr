.. image:: https://beerpay.io/l-x/fakr/badge.svg?style=beer
   :target: https://beerpay.io/l-x/fakr

.. image:: https://badges.gitter.im/random-data-fakrs/Lobby.svg
    :target: https://gitter.im/random-data-fakrs/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-

.. image:: https://travis-ci.org/l-x/fakr.svg?branch=master
    :target: https://travis-ci.org/l-x/fakr

.. image:: https://codecov.io/gh/l-x/fakr/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/l-x/fakr



Random data, fakrs!
===================

*fakr* reads a Jinja2 Template from ``stdin``, renders it using a vocabulary and writes the result to ``stdout``. It's as simple as that...

Installation
------------

``$ pip install fakr``

Basic Usage
-----------

``$ fakr --help``

Examples
--------

Generate a simple csv file with 100k rows

::

 $ echo "{{row}},{{row%100}},{{firstname}},{{lastname}},{{email}}" \
   | fakr --count 100000``


Use a file for complex template

::

  $ cat examples/templates/vcard.tpl \
    | fakr --count 1000


Make a http request using curl:

::

  $ echo "company={{company|urlencode}}&city={{city|urlencode}}"  \
    | fakr -c1 \
    | curl httpbin.org/post -d @-



Write data to a redis server:

::

  $ echo 'firstname \"{{firstname}}\" lastname \"{{lastname}}\" email \"{{email}}\"' \
    | fakr \
    | xargs -i redis-cli HMSET {}``


Templates
---------

The templates you use for data generation are plain `Jinja2 Templates`_. See their reference for detailed information.

There are a few custom filters, functions and variables for use with fakr:

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

Fixed (vocabulary independent) variables:

- ``row``: The row (starting from 0) of the current dataset
- ``id``: The id or sequence number of the current dataset
- ``guid``: The representation of the ``id`` in a uuid-like fashion


.. _`Jinja2 Templates`: http://jinja.pocoo.org/docs/2.9/templates/
.. _`Unidecode`: https://pypi.python.org/pypi/Unidecode