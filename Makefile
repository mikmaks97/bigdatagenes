SECRETS_FILE=genedata/config/secrets.json

init: venv/bin/activate
venv/bin/activate: requirements.txt
	test -d proj_venv || virtualenv proj_venv
	source proj_venv/bin/activate; \
	proj_venv/bin/pip install -Ur requirements.txt; \

cli:
	pip install -e genedata/gene_interaction/; \
	mkdir genedata/cli; \
	cp -R genedata/gene_interaction/gene_interaction_analysis.egg-info genedata/cli; \
	rm -rf genedata/gene_interaction/gene_interaction_analysis.egg-info

