from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="image_processing_mmc",
    version="0.0.4",
    author="monicacaetano",
    author_email="monica02caetano@gmail.com",
    description="Image Processing Package using Skimage",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/monicacaetano/image_processing_dio_unimed.git",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)