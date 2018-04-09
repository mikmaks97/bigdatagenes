#Installation instructions

1. `git clone https://github.com/mikmaks97/bigdatagenes`
2. `make init` in project root (make sure path to project does not contain spaces!)
3. Create local Neo4J, Cassandra, PostgreSQL, and Dynamo databases
4. Set line `enable_user_defined_functions = true` in *cassandra.yaml* in local Cassandra folder
4. Copy data to *data/* directory in project repo or in the case of Neo4J import data to graph folder
5. Change default settings for databases in *config.ini*
6. `source proj_venv/bin/activate` in repo root
7. `python manage.py runserver` and go to (http://localhost:8000) inside *genedata* folder for web interface
8. `make cli` and go to *genedata/cli* for CLIs

