from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='passwordman',
    version='0.0.0',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        ''
    ],
    entry_points='''
    [console_scripts]
    passwordman=passwordman:main
    ''',
    include_package_data=True,
)