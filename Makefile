all:

tests:
	nose2

sdist:
	python setup.py sdist

upload-test: sdist
	twine upload -si DEEFD827 --skip-existing -r pypitest dist/*

upload-rel: sdist
	twine upload -si DEEFD827 --skip-existing -r pypi dist/*

force: