import numpy as np

from barff.main import ArffConverter

field_map = {
    'full name': str,
    'gender': str,
    'email': str,
    'phone': str,
    'is_cool': np.bool,
    'birthday': str,
}


arff_converter = ArffConverter(
    input_file='./tests/test_input.csv',
    output_file='./tmp/output.arff',
    relation='test relation',
    field_map=field_map
)

arff_converter.main()
