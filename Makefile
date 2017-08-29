all:

tests:
	python -m nose2 -v --log-capture test

coverage:
	python -m nose2 -v --log-capture --with-coverage --coverage fakr -s test

sdist:
	python setup.py sdist

upload-test: sdist
	twine upload -si DEEFD827 --skip-existing -r pypitest dist/*

upload-rel: sdist
	twine upload -si DEEFD827 --skip-existing -r pypi dist/*

force: