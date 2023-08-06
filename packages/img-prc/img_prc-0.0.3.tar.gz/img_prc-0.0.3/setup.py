from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="img_prc",
    version="0.0.3",
    author="Adieverson Silva",
    author_email="adieverson.pro@gmail.com",
    description="Pacote feito para estudo 2",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AdieversonPro",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)