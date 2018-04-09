from setuptools import setup
setup(
    name = 'gene_stats',
    version = '1.0',
    packages = ['gene_stats'],
    entry_points = {
        'console_scripts': [
            'gene_stats = gene_stats.__main__:main'
        ]
    })
