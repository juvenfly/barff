import shlex
import os
from mock import MagicMock, patch
from unittest import TestCase

from barff import utils
from barff.models import CsvToArffConverter
from barff.maps import CSV_TO_PANDAS


# TODO: There's a lot of redundancy here with test_models now.
class TestCsvToArffConverter(TestCase):

    def setUp(self):
        self.arff_converter = CsvToArffConverter(
            input_file='./tests/test_input.csv',
            output_file='./tmp/output.arff',
            relation='test relation',
            field_map=CSV_TO_PANDAS,
        )
        self.data_frame = self.arff_converter.data_frame

    @patch('barff.models.ToArffConverter.map_column_to_arff_class')
    def test_map_data_types(self, MockMeth):
        mock_meth = MockMeth()
        special_cases = ['bool']
        for case in special_cases:
            self.arff_converter.map_data_types(case, 'is_cool')
            mock_meth.assert_called

    def test_quote_if_space(self):
        expected_outcomes = {
            'abcd': 'abcd',
            ' defg': '" defg"',
            'hijk ': '"hijk "',
            'lm no': '"lm no"',
        }
        for val in expected_outcomes.keys():
            outcome = utils.quote_if_space(val)
            self.assertEqual(outcome, expected_outcomes[val])


class TestOutputFile(TestCase):

    def setUp(self):
        self.arff_converter = CsvToArffConverter(
            input_file='./tests/test_input.csv',
            output_file='./tmp/output.arff',
            relation='test relation',
            field_map=CSV_TO_PANDAS,
        )
        self.arff_converter.collect_comments = MagicMock()
        self.expected_arff_file = open('./tests/expected_output.arff')
        self.arff_converter.main()
        self.input_file = open('./tests/test_input.csv', 'rU')
        self.output_file = open('./tmp/output.arff')

    def tearDown(self):
        self.input_file.close()
        self.output_file.close()
        os.remove(self.arff_converter.output_file.name)

    def test_arff_header(self):
        csv_header = self.input_file.readline().replace('\n', '').split(',')

        for line in self.output_file:
            if line.startswith('@ATTRIBUTE'):
                header_val = shlex.split(line)[1]
                self.assertIn(header_val, csv_header)
                csv_header.pop(csv_header.index(header_val))

            if line.startswith('@DATA'):
                break

        self.assertEqual(len(csv_header), 0)

    def test_arff_data(self):
        self.input_file.next()
        arff_line = self.output_file.readline()

        while not arff_line.startswith('@DATA'):
            arff_line = self.output_file.readline()

        for csv_line in self.input_file:
            csv_line = csv_line.split(',')
            csv_line = [utils.quote_if_space(item) for item in csv_line]
            arff_line = self.output_file.readline().split(',')
            if '?' not in arff_line:
                self.assertEqual(csv_line, arff_line)
            else:
                # TODO: Implement special case testing
                pass
