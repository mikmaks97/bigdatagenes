from setuptools import setup
setup(
    name = 'patient_info',
    version = '1.0',
    packages = ['patient_info'],
    entry_points = {
        'console_scripts': [
            'patient_info = patient_info.__main__:main'
        ]
    })
