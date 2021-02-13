fix:
	autoflake --exclude=".venv/" --remove-all-unused-imports --remove-unused-variables .
	isort --skip=".venv/" -sl! -m 3 .
	black --exclude=".venv/" .
	flake8 --exclude=".venv/" .
	mypy .
