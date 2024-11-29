from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sas-prices-py",
    version="0.1.2",
    author="Alex Choi",
    author_email="alexchoidev@gmail.com",
    description="Python package for fetching SAS flight prices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alexechoi/sas-py",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.32.3",
        "aiohttp>=3.11.7",
        "brotli>=1.1.0",
    ],
)