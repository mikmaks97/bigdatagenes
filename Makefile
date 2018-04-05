SECRETS_FILE=genedata/config/secrets.json

init: venv/bin/activate
venv/bin/activate: requirements.txt
	test -d proj_venv || virtualenv proj_venv; \
	source proj_venv/bin/activate; \
	pip install -Ur requirements.txt; \

