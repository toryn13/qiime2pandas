from setuptools import setup, find_packages

setup(
    name='qiime2pandas',
    version='0.1.0',
    description='A package to work with QIIME2 files and pandas',
    author='Toryn Poolman',
    author_email='t.poolman@ucl.ac.uk',
    url='https://github.com/toryn13/qiime2pandas',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
