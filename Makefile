all:
	@make api
install:
	@python3 -m venv venv
	( \
		source ./venv/bin/activate; \
		pip install -r requirements.txt; \
	)

api:
	( \
		source ./venv/bin/activate; \
		python run.py; \
	)
