from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="process-image",
    version="0.0.2",
    author="Thiago",
    description="Image Processing Package using skimage",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thiagodruvis/Descomplicando_a_criacao_de_pacotes_de_processamento_de_imagens_em_Python",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)
