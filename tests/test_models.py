import os
from unittest import TestCase

from barff.models import ArffValidator
from barff.exceptions import ValidationError


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
        failure_cases = [
            ([], []),
        ]

        success_cases = [
            ([], []),
        ]
