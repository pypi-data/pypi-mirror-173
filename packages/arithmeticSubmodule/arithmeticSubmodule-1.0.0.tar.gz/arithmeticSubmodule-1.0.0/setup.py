from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Arithmetic operations package'
LONG_DESCRIPTION = 'Python package that includes sum, rest, mult and div operations'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="arithmeticSubmodule", 
        version='1.0.0',
        author="David Garrido",
        author_email="<youremail@email.com>",
        description='Arithmetic operations package',
        long_description='Python package that includes sum, rest, mult and div operations for two vectors',
        packages=find_packages(),
        install_requires=[],
        
        keywords=['python', 'arithmetic', 'vectors'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: Unix",
        ]
)