# flake8: noqa
from datetime import datetime

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
        'arff_dtype': '{M,F}',
    },
    'email': {
        'pandas_dtype': str,
        'arff_dtype': 'STRING',
    },
    'phone': {
        'pandas_dtype': str,
        'arff_dtype': 'NUMERIC',
    },
    'is_cool': {
        'pandas_dtype': np.bool,
        'arff_dtype': '{TRUE,FALSE}',
    },
    'birthday': {
        'pandas_dtype': str,
        'arff_dtype': 'DATE "yyyy-MM-dd"',
    },
}

ARFF_FIELD_MAPS = {
    'falsey':   [0, '0', 'f', 'false', 'n', 'no'],
    'truthy':   [1, '1', 't', 'true', 'y', 'yes'],
    'none':     [None, 'none', 'null', 'nan', '?'],
}

ARFF_DATA_TYPES = {
    'builtins': {
        (str, unicode, ):   'STRING',
        (int, long, ):      'NUMERIC',
        (float, ):          'REAL',
        (datetime, ):       'DATE',
    },
    'np_dtypes': {
        (np.int, ):     'NUMERIC',
        (np.float, ):   'REAL',
        (np.bool, ):    '<nominal-specification',
    },
}
