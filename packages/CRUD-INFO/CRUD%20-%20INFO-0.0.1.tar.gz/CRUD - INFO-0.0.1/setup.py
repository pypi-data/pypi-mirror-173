from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='CRUD - INFO',
      version='0.0.1',
      url='https://github.com/Fabreba/Info_CRUD',
      license='MIT License',
      author='Fabricio Silva',
      long_description=readme,
      long_description_content_type="text/markdown",
      author_email='fabricioj49@gmail.com',
      keywords='Pacote',
      description='Pacote que recebe informacoes e printa ao usuario',
      packages=['CRUD_ID', 'CRUD_ID.Consulta', 'CRUD_ID.Interecao', 'CRUD_ID.Armazenamento'],
      install_requires=['os'], )
