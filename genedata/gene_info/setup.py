from setuptools import setup
setup(
    name = 'gene_info',
    version = '1.0',
    packages = ['gene_info'],
    entry_points = {
        'console_scripts': [
            'gene_info = gene_info.__main__:main'
        ]
    })
