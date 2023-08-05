from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='packpypi',
    version='0.0.1',
    url='http://github.com',
    license='MIT License',
    author='Pedro Vitor Raiol Comin',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='pedro21070007@aluno.cesupa.br',
    keywords='Pacote',
    description='Pacote python para estudar python',
    packages=['packpypi'], )