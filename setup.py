from setuptools import setup

setup(
    name='tezos-playground',
    version='0.1',
    py_modules=['src'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        tezos-playground=src.clients.conseilpy.cli:cli
    ''',
)
