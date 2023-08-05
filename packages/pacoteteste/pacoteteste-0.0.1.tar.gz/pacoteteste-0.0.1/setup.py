from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='pacoteteste',
    version='0.0.1',
    url='https://github.com',
    license='MIT License',
    author='Ricardo Vigliano',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='',
    keywords='Pacote',
    description='',
    packages=['pacoteteste'],)