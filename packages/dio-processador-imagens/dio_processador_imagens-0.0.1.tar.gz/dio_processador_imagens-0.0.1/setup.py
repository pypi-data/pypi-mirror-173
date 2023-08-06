from setuptools import setup, find_packages

with open("README.md", "r") as f:
    descricao_pagina = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name= "dio_processador_imagens",
    version= "0.0.1",
    author= "Agner_Lana",
    description="Pacote simples de processamento de imagens",
    long_description= descricao_pagina,
    long_description_content_type= "text/markdown",
    url="https://github.com/agnerlana/descomplicando_processamento_imagens.git",
    packages= find_packages(),
    install_requires= requirements,
    python_requires=">=3.5",
)