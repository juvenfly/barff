# flake8: noqa
import numpy as np

PANDAS_TO_ARFF = {
    'float64':      'NUMERIC',
    'int64':        'NUMERIC',
    'object':       'STRING',
    'datetime64':   'DATE',
}

CSV_TO_PANDAS = {
    'full name': str,
    'gender': str,
    'email': str,
    'phone': str,
    'is_cool': np.bool,
    'birthday': str,
}