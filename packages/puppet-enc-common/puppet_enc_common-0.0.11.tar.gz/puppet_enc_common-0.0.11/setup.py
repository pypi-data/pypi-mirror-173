from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='puppet_enc_common',
    version='0.0.11',
    description='Puppet ENC Common Elements',
    #py_modules=['puppet_enc_common_database', 'puppet_enc_common_constants'],
    #package_dir={'': 'puppet_enc_common'},
    packages=find_packages(),
    install_requires=[
        "peewee",
        "Werkzeug",
        "Flask-Login"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Flask",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3"
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/graham-m-smith/puppet-enc-common-python-module",
    maintainer="Graham Smith",
    maintainer_email="github@gmsnet.co.uk",
    license='MIT'
)