dev:
	uv run python3 manage.py runserver

lint:
	uv run ruff check && uv run isort wardrobe_app/

makemigrations:
	uv run python3 manage.py makemigrations

migrate:
	uv run python3 manage.py migrate

test:
	uv run pytest