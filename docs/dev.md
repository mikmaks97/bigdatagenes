# Tips for development

To access the settings in *config.ini* you use the `get_setting` in *config/config.py*.<br>
To access this module in any script of the project just use these three beautiful lines:<br>
```python
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'config')))
import config
```
Then you can just use `config.get_setting`.<br><br>

That disgusting line of code just says to go two directories up and then append /config,<br>
so if the path of the script is proj_root/folder/folder/file the new path becomes<br>
proj_root/config. That is then appended to the system PATH variable. You should<br>
alter the number of *..* depending on how deep your file is.<br><Br>

**Make sure to create ___init__.py_ in every folder that you want to be a package** (basically every folder)<br>
Also, follow the project structure for your parts like I did for the *gene_interaction* folder:
- The root *gene_interaction* folder has *setup.py* in it (which you can just copy an change a bit)
- *__main__.py* is in the inner *gene_interaction* folder and is the main CLI file.
- You can run `pip install -e .` while in the outer folder to install your package!
I added a section in the Makefile, which installs my package and copies it over to a new CLI folder.<br>
You can add your package installation lines to it.<br>
I really hope that my files help you at least a bit. But, damn, let's focus on making the DBs.


