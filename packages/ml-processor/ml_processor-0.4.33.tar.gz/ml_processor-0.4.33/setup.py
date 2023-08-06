
from setuptools import setup
import os



path = os.path.join(os.environ.get('HOME'), 'Desktop/package_dev/ml/README.rst')


with open(path, "r") as fh:
    long_description = fh.read()

setup(
    # name that will be imported, can be different from code file name
    name='ml_processor',

    version='0.4.33',

    description='Includes functions for performing econometrics tasks',

    # code file name without file extension
    # py_modules=['configuration', 'eda_analysis', 'encoders', 'jsonSerializer', 'model_training' 'outliers' 'snowflake_processor'],

    packages=['ml_processor'],

    # directory in which code file is stored
    package_dir={'':'src'},

    long_description=long_description,

    # long_description_content_type="text/markdown",

    long_description_content_type="text/x-rst",

    author="Geofrey Wanyama",

    author_email="wanyamag17@gmail.com",

    url="https://github.com/G-Geofrey/package_dev/tree/master/ml",

    zip_safe=False,

    classifers=[ 
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7", 
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
        ],

     install_requires=[
        'pandas>=1.4.2',
        'numpy>=1.17',
        'matplotlib>=3.5.1',
        'seaborn>=0.11.2',
        'sklearn>=1.0.2',
        'optbinning==0.15.1',
        'snowflake.sqlalchemy>=1.4.1',
        'sqlalchemy>=1.4.32',
        'cryptography>=3.4.8',
        'joblib>=1.1.0',
        'xgboost>=1.6.2',
        'statsmodels>=0.13.2',
        'hyperopt>=0.2.7',
        'scipy>=1.7.3'
    ]


    )