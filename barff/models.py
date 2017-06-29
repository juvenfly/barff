import csv
import os
import shlex
import sys
from builtins import input

import pandas as pd

from barff.exceptions import ValidationError
from barff.maps import PANDAS_TO_ARFF
from barff.utils import create_delimited_row, quote_if_space


class ArffConverter(object):

    def __init__(self, input_file, output_file, relation=None, field_map=None):
        """
        Initialize instance variables
        :param input_file: path to input file as str
        :param output_file: path to output file as str
        :param relation: relation as str
        :param header_map: path to map of JSON file mapping csv headers to pandas dtypes
        """
        self.input_file = input_file
        self.data_frame = None
        self.output_file = open(output_file, 'w+')
        self.relation = relation if relation else 'undefined relation'
        self.field_map = field_map

    def main(self):
        self.create_data_frame()

        self.collect_comments()

        self.output_file.write('@RELATION {} \n\n'.format(quote_if_space(self.relation)))

        output_header = self.convert_header()

        for line in output_header:
            self.output_file.write(line)

        self.output_file.write('\n@DATA\n')

        for row in self.output_rows():
            self.output_file.write(row)

        self.output_file.close()

    def map_column_to_arff_class(self, column):
        """
        Converts 'bool' data type to arff format
        :param column: column in pandas dataframe
        :return: arff class format
        """
        unique_vals = [str(val) for val in self.data_frame[column].unique() if not isinstance(val, str) or val]
        result = '{' + ','.join(unique_vals) + '}'

        return result


class CsvToArffConverter(ArffConverter):

    def collect_comments(self):
        """
        Collects comments from the command line and writes them to the output file.
        """
        line_number = 0
        while True:
            line_number += 1
            comment = input("Please input comment line {} or 'X' to continue: ".format(line_number))
            if comment.lower() in ['x', "'x'"]:
                break
            comment = '% {}\n'.format(comment)
            self.output_file.write(comment)

        self.output_file.write('%\n')

    def convert_header(self):
        """
        Converts header from data_frame to arff
        :return: list of lines
        """
        arff_header = []

        for column in self.data_frame.columns:
            attribute_name = column
            pd_dtype = str(self.data_frame[attribute_name].dtype)

            arff_dtype = self.map_data_types(pd_dtype, column)

            line = '@ATTRIBUTE {} {}\n'.format(quote_if_space(attribute_name), arff_dtype)
            arff_header.append(line)

        return arff_header

    def map_data_types(self, pd_dtype, column):
        """
        Converts a pandas data type to the corresponding arff data type
        :param pd_dtype: pandas data type as string
        :param column: name of column in pandas dataframe
        :return: arff data type as string
        """
        try:
            arff_dtype = PANDAS_TO_ARFF[pd_dtype]
        except KeyError:
            if pd_dtype == 'bool':
                arff_dtype = self.map_column_to_arff_class(column)
            else:
                raise

        return arff_dtype

    def output_rows(self):
        """
        Generator that yields arff rows from pandas dataframe
        :return: arff row
        """
        for pd_row in self.data_frame.values:
            row = create_delimited_row(pd_row, delimiter=',')
            yield row

    def create_data_frame(self):
        self.data_frame = pd.read_csv(self.input_file, dtype=self.field_map)


class ArffToCsvConverter(ArffConverter):

    def main(self):
        self.create_data_frame()
        self.data_frame.to_csv(self.output_file, index=False, quoting=csv.QUOTE_NONE, escapechar='\\')

    def convert_header(self):
        csv_header = []
        arff_file = open(self.input_file, 'rU')
        for line in arff_file:
            if line.startswith('@ATTRIBUTE'):
                header_val = shlex.split(line)[1]
                csv_header.append(header_val)
            if line.startswith('@DATA'):
                break
        arff_file.close()
        return csv_header

    def create_data_frame(self):
        header = self.convert_header()
        arff_data = open(self.input_file, 'rU')
        while True:
            line = arff_data.next()
            if '@DATA' in line:
                break
        data = [line.replace('\n', '').split(',') for line in arff_data]
        self.data_frame = pd.DataFrame(columns=header, data=data)
        arff_data.close()


def csv_to_arff(csv_file, output_file, relation=None, field_map=None):
    converter = CsvToArffConverter(csv_file, output_file, relation, field_map)
    converter.main()


def arff_to_csv(arff_file, output_file):
    converter = ArffToCsvConverter(arff_file, output_file)
    converter.main()


class ArffValidator(object):

    def __init__(self, arff_file, input_file):
        self.arff_file = open(arff_file, 'rU')
        self.input_file = open(input_file, 'rU')
        self.file_extension = os.path.splitext(input_file)[1].lower()

    def prepare_files(self):

        for line in self.arff_file:
            if not line.startswith('@DATA'):
                self.arff_file.readline()

        if self.file_extension == '.csv':
            self.input_file.next()

    def validate(self):
        for line in self.input_file:
            arff_line = self.arff_file.readline()
            if line != arff_line:
                msg = 'Line mismatch between input:\n{}\nand ARFF output:\n{}'.format(line, arff_line)
                raise ValidationError(msg)
        sys.stdout('Validation complete. Files match.')

        self.arff_file.close()
        self.input_file.close()
