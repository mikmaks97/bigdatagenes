# Tips for development

To access settings in config.ini import config module (config/config.py) relative to
working module:<br>

<t>`from ..config import config`<br>

will import config module from config package, which is located in parent directory of called script.

For relative imports to work with parent directories run script from project root:<br>
`python3 -m genedata.<your_folder>.<your_module>`

instead of `python3 <your_module>.py`

Take note of the lack of .py when running as a module (aargh..)

**Make sure to create ___init__.py_ in any folder that you want to be a package**
