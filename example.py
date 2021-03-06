import barff
import numpy as np

csv_file = './tests/test_input.csv'
output_file = './tmp/output.arff'
relation = 'test relation'
field_map = {
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

barff.csv_to_arff(csv_file, output_file, relation, field_map)
barff.arff_to_csv(output_file, './tmp/csv_output.csv')
