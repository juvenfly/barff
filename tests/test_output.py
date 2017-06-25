import os
from mock import MagicMock
from unittest import TestCase

from barff.main import ArffConverter

comments = ['this is a comment', 'this is also a comment']


class TestOutputFile(TestCase):

    def setUp(self):
        self.arff_converter = ArffConverter('./tests/test_input.csv')
        self.arff_converter.collect_comments = MagicMock()
        self.csv_file = open('./tests/test_input.csv', 'rU')
        self.expected_arff_file = open('./tests/expected_output.arff')
        self.arff_converter.main()
        self.actual_arff_file = open('./tmp/output.arff')

    def tearDown(self):
        self.csv_file.close()
        self.expected_arff_file.close()
        os.remove(self.actual_arff_file.name)

    def test_arff_comments(self):
        for actual_line in self.actual_arff_file:
            expected_line = self.expected_arff_file.readline()
            self.assertEqual(actual_line, expected_line)

    def test_arff_header(self):
        csv_header = self.csv_file.readline().replace('\n', '').split(',')

        for line in self.actual_arff_file:
            if line.startswith('@ATTRIBUTE'):
                header_val = line.split(' ')[1]
                self.assertIn(header_val, csv_header)
                csv_header.pop(csv_header.index(header_val))

            if line.startswith('@DATA'):
                break

        self.assertEqual(len(csv_header), 0)

    def test_arff_data(self):
        self.csv_file.next()
        arff_line = self.actual_arff_file.readline()

        while not arff_line.startswith('@DATA'):
            arff_line = self.actual_arff_file.readline()

        for csv_line in self.csv_file:
            arff_line = self.actual_arff_file.readline()
            self.assertEqual(csv_line, arff_line)
