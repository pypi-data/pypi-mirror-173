import io
from setuptools import setup, find_packages

from bci_ml import __version__

def read(file_path):
    with io.open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


readme = read('README.rst')
requirements = read('requirements.txt')


setup(
    # metadata
    name='bci-ml',
    version=__version__,
    license='MIT',
    author='Intelligent Systems',
    author_email="mlalgorithms@gmail.com",
    description='lib for signal decoding, python package',
    long_description=readme,
    url='https://github.com/intsystems/bci-ml',

    # options
    packages=find_packages(),
    install_requires=requirements,
)
