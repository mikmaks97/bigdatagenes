# Tips for development

To access the settings in *config.ini* run scripts from the project root:<br>
`python3 -m genedata.gene_interaction.gene_interaction.query_neo4j`<br>
This will run *neo4j.py* as a module, and you can then access *genedata/config/config.py*<br>
with `from genedata.config import config` inside *neo4j.py*.

Do this for all your scripts too. The absolute imports prevent lots of headaches.

**Make sure to create ___init__.py_ in every folder that you want to be a package** (basically every folder)
