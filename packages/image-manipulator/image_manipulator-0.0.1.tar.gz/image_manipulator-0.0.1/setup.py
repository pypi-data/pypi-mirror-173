from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="image_manipulator",
    version="0.0.1",
    author="Alex Pivato",
    author_email="alexsnpivatoo@hotmail.com",
    description="pacote de manipulação de imagem",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aleeexp/Criando-um-pacote-no-PyPI",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.6',
)