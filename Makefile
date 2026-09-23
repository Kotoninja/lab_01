test:
	uv run pytest .

coverage:
	uv run coverage run -m pytest .
	uv run coverage report
	uv run coverage html
