all:

sdist:
	python setup.py sdist

upload-test: sdist
	twine upload --skip-existing -r pypitest dist/*

upload-rel: sdist
	twine upload --skip-existing -r pypi dist/*

force: