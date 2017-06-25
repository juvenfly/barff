import os
from mock import MagicMock
from unittest import TestCase

from barff.main import ArffConverter

comments = ['this is a comment', 'this is also a comment']


class TestOutputFile(TestCase):

    def setUp(self):
        self.arff_converter = ArffConverter('./tests/test_input.csv', './tmp/output.arff')
        self.arff_converter.collect_comments = MagicMock()
        self.expected_arff_file = open('./tests/expected_output.arff')
        self.arff_converter.main()
        self.input_file = open('./tests/test_input.csv', 'rU')
        self.output_file = open('./tmp/output.arff')

    def tearDown(self):
        self.input_file.close()
        self.output_file.close()
        os.remove(self.arff_converter.output_file.name)

    def test_arff_comments(self):
        for actual_line in self.output_file:
            expected_line = self.expected_arff_file.readline()
            self.assertEqual(actual_line, expected_line)

    def test_arff_header(self):
        csv_header = self.input_file.readline().replace('\n', '').split(',')
        print csv_header

        for line in self.output_file:
            if line.startswith('@ATTRIBUTE'):
                header_val = line.split(' ')[1]
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
            arff_line = self.output_file.readline()
            self.assertEqual(csv_line, arff_line)
