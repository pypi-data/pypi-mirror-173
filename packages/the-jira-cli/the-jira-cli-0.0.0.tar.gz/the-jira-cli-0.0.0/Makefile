setup:
	# Create python virtualenv & source it
	# Run this source command after running `make setup`
	# source .venv/bin/activate
	python3 -m venv .venv

environment:
	cp .example.env .env

install-requirements:
	pip3 install -r requirements.txt --require-virtualenv


clean:
	find . | grep -E "(__pycache__|\.pyc|\.pyo$\)" | xargs rm -rf
	rm -rf ./*.egg-info
	rm -rf ./dist
	rm -rf ./build

test:
	echo "Testing"

build:
	python3 -m build

install-editable:
	pip install --editable .

publish-test:
	python3 -m twine upload --repository testpypi dist/*

publish:
	python3 -m twine upload dist/*
