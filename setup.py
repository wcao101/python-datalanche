from setuptools import setup, find_packages

required = ['requests == 1.2']

setup(
    author='Datalanche, Inc.',
    name='datalanche',
    version='0.1.0',
    description='Official Python client for Datalanche\'s REST API.',
    long_description=open('README.md').read(),
    url='https://github.com/datalanche/python-datalanche',
    license=open('LICENSE').read(),
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ),
    keywords=['datalanche'],
    packages=find_packages(),
    install_requires=required
)
