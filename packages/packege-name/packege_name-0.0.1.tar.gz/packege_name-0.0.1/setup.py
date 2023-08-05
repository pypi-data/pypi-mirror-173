from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    page_description = f.read()

with open('requirements.txt', 'r') as f:
        requirements = f.read().splitlines()

setup(
    name='packege_name', # aqui é colocado o nome do pacote
    version='0.0.1', # aqui é colocado a versão do pacote, este formato deve ser o recomendado pela pep8
    author= 'caio777', # aqui é colocado o nome do autor do pacote
    author_email='caio777alberto7@gmail.com', # aqui é colocado o e-mail do autor
    description='My short description', # aqui é colocado uma pequena descrição do pacote
    long_description=page_description, # aqui é colocado uma descrição completa do pacote
    long_description_content_type='text/markdown', # passando o tipo de conteúdo que tem em long description
    url='https://github.com/caio-alberto/image_processing.git', # aqui é colocado o link do repositório onde está o pacote
    packages=find_packages(), # aqui é especificado todos os módulos e submódulos do projeto
    install_requires=requirements, # usado quando há dependencias de outros pacotes
    python_requires='>=3.8' # identifica qual versão do python o pacote pode ser executado
)
