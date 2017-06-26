import numpy as np

import barff

csv_file = './tests/test_input.csv'
output_file = './tmp/output.arff'
relation='test relation'
field_map = {
    'full name': str,
    'gender': str,
    'email': str,
    'phone': str,
    'is_cool': np.bool,
    'birthday': str,
}

barff.convert_csv(csv_file, output_file, relation, field_map)
