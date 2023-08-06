from setuptools import setup, find_packages

long_description = open('./README.md')

setup(
    name='Vigilant',
    version='1.0.1',
    url='https://github.com/ZSendokame/Vigilant',
    license='MIT license',
    author='ZSendokame',
    description='Create and run tests easily.',
    long_description=long_description.read(),
    long_description_content_type='text/markdown',

    packages=(find_packages(include=['vigilant']))
)
