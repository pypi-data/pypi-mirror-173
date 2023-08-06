"""Setup file with package config."""
from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["pandas", "numpy"]

setup(
    name="abc_classification",
    version="0.0.7",
    author="Ashot Melikbekyan",
    author_email="melikbekyan.ashot@yandex.ru",
    description="A package for ABC classification",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/MelikbekyanAshot/abc-classification",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
