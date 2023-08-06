from setuptools import setup, find_packages

with open("README.md","r") as f:
    page_description = f.read()

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="combustivel",
    version="0.0.1",
    author="Samuel",
    author_email="samufabiano@yahoo.com.br",
    desription="Calcular a quantidade de litros gastos em uma viagem",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    install_requires=requirements,
python_requires='>=3.8',
)