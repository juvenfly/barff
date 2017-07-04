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

ARFF_FIELD_MAPS = {
    'contains_space': r'.*\s.*',
    'falsey':   [0, '0', 'f', 'false', 'n', 'no'],
    'truthy':   [1, '1', 't', 'true', 'y', 'yes'],
    'none':     [None, 'none', 'null', 'nan', '?'],
}
