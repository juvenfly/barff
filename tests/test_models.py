import os
from mock import MagicMock
from unittest import TestCase

import pandas as pd

from barff.models import ToArffConverter, ArffValidator, compare_values
from barff.exceptions import ValidationError


class TestToArffConverter(TestCase):

    def setUp(self):
        self.converter = ToArffConverter(
            input_file='./tests/test_input.csv',
            output_file='./tmp/test_output.arff',
        )

    def tearDown(self):
        os.remove(self.converter.output_file.name)
        self.converter = None

    def test_instance_vars(self):
        self.assertTrue(os.path.samefile(self.converter.input_file, './tests/test_input.csv'))
        self.assertTrue(os.path.samefile(self.converter.output_file.name, './tmp/test_output.arff'))
        self.assertEqual(self.converter.relation, 'undefined relation')
        self.assertIsNone(self.converter.field_map)
        self.assertFalse(self.converter.validate)

    def test_main(self):
        self.converter.create_data_frame = MagicMock()
        self.converter.collect_comments = MagicMock()
        self.converter.convert_header = MagicMock()
        self.converter.output_rows = MagicMock()

        self.converter.main()
        self.converter.create_data_frame.assert_called()
        self.converter.collect_comments.assert_called()
        self.converter.convert_header.assert_called()
        self.converter.output_rows.assert_called()

    def test_column_to_arff_class(self):
        # TODO: Add more class test cases to test_input.csv
        self.converter.data_frame = pd.DataFrame(['M', 'F', 'F', 'M'], columns=['gender'])
        outcomes = {
            'gender': '{M,F}',
        }

        for column in outcomes:
            expected_result = outcomes[column]
            result = self.converter.map_column_to_arff_class(column)
            self.assertEqual(result, expected_result)


class TestArffValidator(TestCase):

    def setUp(self):
        self.validator = ArffValidator(arff_file='./tests/expected_output.arff', input_file='./tests/test_input.csv')

    def tearDown(self):
        self.validator = None

    def test_instance_vars(self):
        self.assertTrue(os.path.samefile(self.validator.arff_file.name, './tests/expected_output.arff'))
        self.assertTrue(os.path.samefile(self.validator.input_file.name, './tests/test_input.csv'))
        self.assertEqual(self.validator.file_extension, '.csv')

    def test_prepare_files(self):
        self.validator.prepare_files()
        expected_arff_line = '"Testly McTesterson",M,foo@bar.baz,1234567,TRUE,1984-05-22\n'
        self.assertEqual(self.validator.arff_file.next(), expected_arff_line)

        expected_csv_line = 'Testly McTesterson,M,foo@bar.baz,1234567,True,1984-05-22\n'
        self.assertEqual(self.validator.input_file.next(), expected_csv_line)

    def test_validate(self):
        self.assertTrue(self.validator.validate())

        self.bad_validator = ArffValidator('./tests/bad_output.arff', './tests/test_input.csv')
        self.assertRaises(ValidationError, self.bad_validator.validate)

    def test_compare_values(self):
        # TODO: Find & add more edge cases
        failure_cases = [
            {
                'input_line': ['entry with space', 'good_val', 'good_val'],
                'arff_line': ['entry with space', 'good_val', 'good_val'],
            },
            {
                'input_line': ['entry with space', 'none', 'good_val'],
                'arff_line': ['"entry with space"', 'none', 'good_val'],
            }
        ]

        success_cases = [
            {
                'input_line': ['entry with space', 'good_val', 'none'],
                'arff_line': ['"entry with space"', 'good_val', '?'],
            },
        ]

        for case in failure_cases:
            self.assertRaises(ValidationError, compare_values, line=case['input_line'], arff_line=case['arff_line'])

        for case in success_cases:
            try:
                compare_values(line=case['input_line'], arff_line=case['arff_line'])
            except ValidationError:
                self.fail('compare_values() raised ValidationError unexpectedly!')
