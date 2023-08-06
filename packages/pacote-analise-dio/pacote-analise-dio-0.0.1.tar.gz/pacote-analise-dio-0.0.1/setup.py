from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="pacote-analise-dio",
    version="0.0.1",
    author="Renan Faria",
    author_email="renanfariadsn@gmail.com",
    description="Pacote para manipulação, análise e visualização de um conjunto de dados específico.",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Diamenor/projeto-dio-pacotes",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)
