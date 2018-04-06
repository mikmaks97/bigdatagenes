from setuptools import setup
setup(
    name = 'gene_interaction_analysis',
    version = '1.0',
    packages = ['gene_interaction'],
    entry_points = {
        'console_scripts': [
            'gene_interaction_analysis = gene_interaction.__main__:main'
        ]
    })
