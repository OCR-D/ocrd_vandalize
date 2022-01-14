# pypi name of the package
PKG_NAME = ocrd_vandalize

# BEGIN-EVAL makefile-parser --make-help Makefile

help:
	@echo ""
	@echo "  Targets"
	@echo ""
	@echo "    deps         pip install -r requirements.txt"
	@echo "    deps-test    pip install -r requirements-test.txt"
	@echo "    install      pip install ."
	@echo "    install-dev  pip install -e ."
	@echo "    uninstall    pip uninstall $(PKG_NAME)"
	@echo "    assets       Fetch test assets"
	@echo "    test         Run tests"
	@echo ""
	@echo "  Variables"
	@echo ""
	@echo "    PKG_NAME  pypi name of the package"

# END-EVAL

# pip install -r requirements.txt
deps:
	pip install -r requirements.txt

# pip install -r requirements-test.txt
deps-test:
	pip install -r requirements-test.txt


# pip install .
install:
	pip install .

# pip install -e .
install-dev:
	pip install -e .

# pip uninstall $(PKG_NAME)
uninstall:
	pip uninstall $(PKG_NAME)

# Fetch test assets
assets: test/assets

repo/assets:
	git submodule update --init

# Run tests
test: repo/assets
	#rm -rf tests/assets
	cp -r repo/assets/data tests/assets
	pytest tests

.PHONY: assets deps deps-test install install-dev test uninstall
