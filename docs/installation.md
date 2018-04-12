# Installation instructions<br>

Dependencies: Python 2.7, pip(not v.9.0.1), virtualenv (with appropriate pip version)<br>
Python 2.7.13 and virtualenv 15.2.0 with pip 9.0.3 worked for me.<br>
If `pip -r requirements.txt` fails on `cassandra-driver` you can try `pip install cassandra-driver --install-option="--no-cython"`<br>
If it fails on `pandas`, run `pip install pandas` manually.<br>

1. `git clone https://github.com/mikmaks97/bigdatagenes`
2. `make init` in project root (make sure path to project does not contain spaces!)
3. Create local Neo4J, Cassandra, PostgreSQL, and Dynamo databases
4. Set line `enable_user_defined_functions = true` in *cassandra.yaml* in local Cassandra folder
4. Copy data to *data/* directory in project repo or in the case of Neo4J import data to graph folder
5. Change default settings for databases in *config.ini*
6. `source proj_venv/bin/activate` in repo root
7. `chmod +x run_web.sh` and `./run_web.sh` and go to http://localhost:8000 for web interface
8. `make cli` and go to *cli* for CLIs

