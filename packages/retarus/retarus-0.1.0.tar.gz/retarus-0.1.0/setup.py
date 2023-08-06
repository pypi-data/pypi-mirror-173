import os
from setuptools import setup

version_contents = {}


with open('README.md') as f:
    long_description = f.read()


here = os.path.abspath(os.path.dirname(__file__))
with open(f"{here}/retarus/version.py") as f:
    exec(f.read(), version_contents)

setup(
    name="retarus",
    version=version_contents['__version__'],
    packages=["retarus", "retarus.fax", "retarus.sms", "retarus.base"],
    description="The official client SDK for easy implementation of Retarus messaging services.",
    author="Retarus GmbH",
    author_email="michael.lichtenecker@retarus.de",
    url="https://github.com/retarus/retarus-python",
    install_requires=[
        "aiohttp",
        "aiohttp_retry",
        "pydantic",        
    ],
    long_description=long_description,
    long_description_content_type='text/markdown'
)