from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="processingDIOImage",
    version="0.1",
    author="Lucas Borba",
    author_email="lucas_borba@outlook.com",
    description="My short description",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oliverborba/DIO_Pacotes_Python",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)