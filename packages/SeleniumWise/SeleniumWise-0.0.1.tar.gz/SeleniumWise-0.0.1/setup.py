from setuptools import setup


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="SeleniumWise",
    version="0.0.1",
    description="Selenium Wrapper",
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/zzirakadze/SeleniumWise.git",
    author="Zura Zirakadze",
    author_email="zirakadzez@gmail.com",
    keywords="selenium, python",
    license="MIT",
    packages=['SeleniumWise'],
    install_requires=['requirements.txt'],
    include_package_data=True,
)