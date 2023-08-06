from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="Processando_Imagens",
    version="0.0.5",
    author="Jair Pereira",
    author_email="juniorpsilva@msn.com",
    description="Pacote de processamento de imagem usando Skimage",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jair-pc/Dio_Processamento_de_imagens_em_Python",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)