from setuptools import find_packages, setup

with open("./README.md") as f:
    long_description = f.read()

setup(
    name="Bit2cAPI",
    version="0.0.1",
    author="Orel Kalaf",
    author_email="orelron98@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/orel98/Bit2cAPI",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
)
