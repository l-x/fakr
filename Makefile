all:

tests:
	python -m nose2 -v --log-capture test

coverage:
	python -m nose2 -v --log-capture --with-coverage --coverage fakr -s test

dist:
	python setup.py sdist bdist_wheel

upload-test: dist
	twine upload -si DEEFD827 --skip-existing -r pypitest dist/*

upload-rel: dist
	twine upload -si DEEFD827 --skip-existing -r pypi dist/*

clean:
	rm -rf dist build __pycache__ .coverage fakr.egg-info 

force: