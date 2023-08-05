from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='pacoteLegal',
    version='0.0.1',
    url='https://github.com/FabioNeves00/python-terminal-crud',
    license='MIT License',
    author='Fabio Costa de Oliveira Neves Filho',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='fabinhoneves09@gmail.com',
    keywords='Pacote',
    description='Pacote python crud de usuarios',
    packages=['pacoteLegal'],
    install_requires=['json', 'pathlib', 'typing'])
