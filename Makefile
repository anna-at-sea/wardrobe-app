dev:
	uv run python3 manage.py runserver

lint:
	uv run ruff check && uv run isort honduras_shop_aggregator/

makemigrations:
	uv run python3 manage.py makemigrations

migrate:
	uv run python3 manage.py migrate