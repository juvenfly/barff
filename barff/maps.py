# flake8: noqa
import numpy as np

PANDAS_TO_ARFF = {
    'float64':      'NUMERIC',
    'int64':        'NUMERIC',
    'object':       'STRING',
    'datetime64':   'DATE',
}

CSV_TO_PANDAS = {
    'full name': {
        'pandas_dtype': str,
        'arff_dtype': 'STRING',
    },
    'gender': {
        'pandas_dtype': str,
        'arff_dtype': 'STRING',
    },
    'email': {
        'pandas_dtype': str,
        'arff_dtype': 'STRING',
    },
    'phone': {
        'pandas_dtype': str,
        'arff_dtype': 'STRING',
    },
    'is_cool': {
        'pandas_dtype': np.bool,
        'arff_dtype': 'CLASS',
    },
    'birthday': {
        'pandas_dtype': str,
        'arff_dtype': 'STRING',
    },
}