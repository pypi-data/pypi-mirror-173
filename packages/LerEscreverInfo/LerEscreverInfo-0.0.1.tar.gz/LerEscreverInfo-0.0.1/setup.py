from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='LerEscreverInfo',
      version='0.0.1',
      url='',
      license='MIT License',
      author='Pedro Benitah Vieira Sanchez de Melo',
      long_description=readme,
      long_description_content_type="text/markdown",
      author_email='pedrobenitah@gmail.com',
      keywords='Pacote',
      description='Pacote python para cadastrar e ler informações como o nome, o CPF e o endereco',
      packages=['LerEscreverInfo'],
      install_requires=[''], )
