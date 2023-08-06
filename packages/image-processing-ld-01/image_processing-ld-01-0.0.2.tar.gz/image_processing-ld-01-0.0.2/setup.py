from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="image_processing-ld-01",
    version="0.0.2",
    author="Lucas Dionisio",
    description="Package for image processing using Skimage",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lucasdionis10/dio-python-image-processing",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)