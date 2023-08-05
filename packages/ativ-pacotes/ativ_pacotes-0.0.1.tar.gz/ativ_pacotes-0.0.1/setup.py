from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='ativ_pacotes',
      version='0.0.1',
      license='MIT License',
      author='Arthur Queiroz',
      long_description=readme,
      long_description_content_type="text/markdown",
      author_email='arthur21070032@aluno.cesupa.br',
      keywords='ativ pacotes',
      description=u'Repositório para atividade de sala, contendo módulos consulta; armazenamento; interacao',
      packages=['ativ_pacotes'],)
