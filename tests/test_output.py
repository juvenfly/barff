from unittest import TestCase

from barff.main import ArffConverter


class TestOutputFile(TestCase):

    def setUp(self):
        self.arff_converter = ArffConverter()
        self.csv_file = open('./tests/test_input.csv', 'rU')
        self.expected_arff_file = open('./tests/expected_output.arff')
        self.actual_arff_file = None # TODO: Implement this

    def tearDown(self):
        self.csv_file.close()
        self.expected_arff_file.close()
        self.actual_arff_file.close()

    def test_arff_comments(self):
        for actual_line in self.actual_arff_file:
            expected_line = self.expected_arff_file.readline()
            self.assertEqual(actual_line, expected_line)

    def test_arff_header(self):
        csv_header = self.csv_file.readline()

        for line in self.actual_arff_file:
            if line.startswith('@ATTRIBUTE'):
                header_val = line.split(' ')[1]
                csv_header.pop(csv_header.index(header_val))
                self.assertIn(header_val, csv_header)

            if line.startswith('@DATA'):
                break

        self.assertEqual(len(csv_header), 0)

    def test_arff_data(self):
        self.csv_file.next()
        for csv_line in self.csv_file:
            arff_line = self.actual_arff_file.readline()
            self.assertEqual(csv_line, arff_line)
