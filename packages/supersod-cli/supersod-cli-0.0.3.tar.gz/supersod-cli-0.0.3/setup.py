from setuptools import setup, find_packages

setup(
    name='supersodcli',
    version='0.0.3',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'requests',
        'keyring'
    ],
    entry_points={
        'console_scripts': [
            'supersod = src.supersodcli:cli',
        ],
    },
)