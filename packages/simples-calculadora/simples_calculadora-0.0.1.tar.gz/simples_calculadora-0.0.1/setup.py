from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="simples_calculadora",
    version="0.0.1",
    author="Diego Reis",
    author_email="d.felipe66@yahoo.com",
    description="Pacote de uma simples calculadora",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DiegoReis265/Repositorio-BootCamp-Geracao-Tech-Unimed-BH--Ciencia-de-Dados.git",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)