from setuptools import setup
setup(
    name = 'gene_interaction',
    version = '1.0',
    packages = ['gene_interaction'],
    entry_points = {
        'console_scripts': [
            'gene_interaction = gene_interaction.__main__:main'
        ]
    })
