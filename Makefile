.PHONY: build test

PYTHON = python3
SPHINXOPTS =
SPHINXBUILD = sphinx-build
SPHINXPROJ = toad
DOCSDIR = docs
SOURCEDIR = $(DOCSDIR)/source
BUILDDIR = $(DOCSDIR)/build

build:
	$(PYTHON) setup.py build_ext --inplace

install:
	$(PYTHON) setup.py install --record files.txt

uninstall:
	cat files.txt | xargs rm -rf

test:
	$(PYTHON) -m pytest -x ./tests

publish: build
	$(PYTHON) setup.py sdist
	twine upload dist/*  -u $(TWINE_USER) -p $(TWINE_PASS)

publish_wheel: build
	$(PYTHON) setup.py bdist_wheel --universal
	twine upload dist/*  -u $(TWINE_USER) -p $(TWINE_PASS)

clean:
	@rm -rf build/ dist/ *.egg-info/

docs: build
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
