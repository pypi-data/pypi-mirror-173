from setuptools import setup, find_packages


setup(
    name='my_names2-krisss',
    version='1.0.0.0',
    description='Generate random names with length',
    long_description='long descr.',
    author='krisss993',
    author_email='kristopherp994@gmail.com',
    include_package_data=True,
    keywords='random names',
    packages=find_packages(),
    scripts=['my_names2.pac/my_names.py','bin/my_names2.bat'],
    install_requires=['names']
)