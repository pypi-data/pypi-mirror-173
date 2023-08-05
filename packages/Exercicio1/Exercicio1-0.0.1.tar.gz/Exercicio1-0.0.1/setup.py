from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='Exercicio1',
    version='0.0.1',
    url='https://github.com/',
    license='MIT License',
    author='Luiz Felipe Pina',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='pina1402@gmail.com',
    keywords='Pacote',
    description='pacote para armazenamento e consulta de dados',
    packages=['Exercicio1'],)