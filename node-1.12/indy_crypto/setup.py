
from setuptools import setup

setup(
    name='indy_crypto',
    version='0.5.1',
    url='https://github.com/cam-parra/python-ursa',
    description='python wrapper for ursa universal crypto library',
    license='Apache-2.0',
    author='Cam Parra, Vyacheslav Gudkov',
    author_email='camilo.parra@evernym.com, vyacheslav.gudkov@dsr-company.com',
    packages=['indy_crypto'],
    install_requires=['pytest'],
    tests_require=['pytest']
)
