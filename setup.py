from setuptools import setup, find_packages

import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='pyhe',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    package_data={
    'pyhe': [
        'gasideal.csv',
        'hformation.csv'
        ],
    },
    version='0.4',
    description='Python model to simulate heat engines',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/fabiofortkamp/pyhe',
    author='Fábio Fortkamp',
    author_email='fabio@fabiofortkamp.com',
    python_requires='>=3.6, <4',
    install_requires=[
        'CoolProp==6.4.1',
        'matplotlib==3.3.4',
        'numpy==1.19.5',
        'pandas==1.1.5',
        'scipy==1.4.1'
    ],
        extras_require={  # Optional
        'dev': ['ipython==7.13.0'],
        'test': ['pytest==6.2.5'],
    },
)