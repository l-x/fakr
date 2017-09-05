BUILD_DIR=build
DIST_DIR=dist
TEST_DIR=test
VOCABULARIES_DIR=vocabularies
PACKAGE_DIR=fakr
VOCABULARY_BUILD_DIR=$(PACKAGE_DIR)

VOCABULARIES := $(addprefix $(VOCABULARY_BUILD_DIR)/, $(shell ls -d $(VOCABULARIES_DIR)/*.fakr))

all:

$(VOCABULARY_BUILD_DIR):
	@mkdir -p $@

tests:
	python -m nose2 -v --log-capture $(TEST_DIR)

coverage:
	python -m nose2 -v --log-capture --with-coverage --coverage $(PACKAGE_DIR) -s $(TEST_DIR)

dist: clean
	python setup.py sdist bdist_wheel

upload-test: dist
	twine upload -si DEEFD827 --skip-existing -r pypitest $(DIST_DIR)/*

upload-rel: dist
	twine upload -si DEEFD827 --skip-existing -r pypi $(DIST_DIR)/*

.PHONY:
clean:
	rm -rf $(DIST_DIR) $(BUILD_DIR) __pycache__ .coverage fakr.egg-info

.SECONDEXPANSION:
$(VOCABULARIES): $(VOCABULARIES_DIR)/$$(@F)/*.csv | $(VOCABULARY_BUILD_DIR)
	python -c 'from fakr.vocabulary_builder import main; main()' "$@" -t $^

vocabularies: $(VOCABULARIES)

