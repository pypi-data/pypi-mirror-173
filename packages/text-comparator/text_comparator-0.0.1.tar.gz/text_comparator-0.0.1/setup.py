from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="text_comparator",
    version="0.0.1",
    author="jennyfgrd",
    author_email="jenn.fnc@gmail.com",
    description="Com o uso de estatísticas do texto, o pacote identifica aspectos que funcionam como uma “assinatura” da autoria. Desse modo, por meio deste pacote, é possível detectar se dois textos dados foram escritos por uma mesma pessoa.",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jennywhyyy/package-text-comparator",
    packages=find_packages(),
    install_requires = requirements,
    python_requires='>=3.7',
)