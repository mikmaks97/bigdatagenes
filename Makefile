SECRETS_FILE=genedata/config/secrets.json

init: venv/bin/activate
venv/bin/activate: requirements.txt
	test -d bigdatavenv || virtualenv bigdatavenv; \
	source bigdatavenv/bin/activate; \
	pip install -Ur requirements.txt; \

