from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="Imagem_processing_package",
    version="0.0.1",
    author="Marcio_Cabral",
    author_email="cabralfarma@hotmail.com",
    description="Pacote de processamentos de Imagens",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CABRALFARMA",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)