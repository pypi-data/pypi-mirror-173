from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='lucasex1',
    version='0.0.1',
    url='https://github.com',
    license='MIT License',
    author='Lucas Tavares de Jesus Borges',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='lucas21070029@aluno.cesupa.br',
    keywords='Pacote',
    description='Pacote python para exibir número de 1 a 9',
    packages=['lucasex1'],)