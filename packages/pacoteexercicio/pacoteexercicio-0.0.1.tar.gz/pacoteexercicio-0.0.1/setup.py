from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='pacoteexercicio',
    version='0.0.1',
    url='https://github.com/marcos-de-sousa/pacotepypi',
    license='MIT License',
    author='João cardoso',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='jvcq13@gmail.com',
    keywords='Pacote',
    description='Pacote python',
    packages=['pacoteexercicio'],
    install_requires=['numpy'],)