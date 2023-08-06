from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="img_processing",
    version="0.0.4",
    author="Felipe Ferreira Porto",
    author_email="felipe.porto@fatec.sp.gov.br",
    description="Project created by Felipe and supported by https://github.com/tiemi for her students in DIO.",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/felipefporto",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)