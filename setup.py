from setuptools import setup

setup(
    name='snapshotanalyzer-fagner',
    version='0.1',
    author="Fagner Fonseca",
    description="Snapshotanalyzer is a tool to manage AWS EC2 snapshots",
    license="GPLv3+",
    packages=['shotty'],
    url="https://github.com/fdonascimento/snapshotanalyzer-fagner",
    install_requires=[
        'click',
        'boto3'
    ],
    entry_points='''
        [console_scripts]
        shotty=shotty.shotty:cli
    ''',
)
