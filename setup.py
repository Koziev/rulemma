import io
import setuptools

with io.open("README.md", mode="r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="rulemma",
    version="0.0.17",
    author="Ilya Koziev",
    author_email="inkoziev@gmail.com",
    description="Lemmatization library for Russian language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Koziev/rulemma",
    packages=setuptools.find_packages(),
    package_data={'rulemma': ['*.dat']},
    include_package_data=True,
)
