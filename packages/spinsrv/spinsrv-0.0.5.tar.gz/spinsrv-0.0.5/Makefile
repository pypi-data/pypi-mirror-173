build:
	python3 -m build
deploy:
	python3 -m twine upload dist/*
install:
	pip install -e .
fmt:
	python -m black .
test:
	python tests/smoke_test.py
