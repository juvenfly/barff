import csv

import pandas as pd

from maps import PANDAS_TO_ARFF


class ArffConverter(object):
    def __init__(self):
        self.data_frame = None
        self.writer = None

    def main(self):
        self.data_frame = pd.read_csv('./tests/test_input.csv')
        output_file = open('./tmp/output.arff', 'w+')
        self.writer = csv.writer(output_file, delimiter=',', quotechar='', escapechar='\\', quoting=csv.QUOTE_NONE)

        self.collect_comments()

        self.writer.writerow(['@RELATION "test_relation"'])
        self.writer.writerow([])

        arff_header = self.convert_header()

        for line in arff_header:
            self.writer.writerow(line)

        self.writer.writerow([])
        self.writer.writerow(['@DATA'])

        for row in self.arff_rows():
            self.writer.writerow(row)

        output_file.close()

    def collect_comments(self):
        """
        Collects comments from the command line and writes them to the output file.
        """
        line_number = 0
        while True:
            line_number += 1
            comment = raw_input("Please input comment line {} or 'X' to continue: ".format(line_number))
            if comment.lower() in ['x', "'x'"]:
                break
            comment = ['% {}'.format(comment)]
            self.writer.writerow(comment)

        self.writer.writerow(['%'])

    def convert_header(self):
        """
        Converts header from data_frame to arff
        :param data_frame: pandas data_frame
        :param output_file: arff output file
        :return: list of lines
        """
        arff_header = []

        for column in self.data_frame.columns:
            attribute_name = column
            pd_dtype = str(self.data_frame[attribute_name].dtype)

            arff_dtype = self.map_data_types(pd_dtype, column)

            line = ['@ATTRIBUTE {} {}'.format(attribute_name, arff_dtype)]
            arff_header.append(line)

        return arff_header

    def map_data_types(self, pd_dtype, column):
        """
        Converts a pandas data type to the corresponding arff data type
        :param pd_dtype: pandas data type as string
        :return: arff data type as string
        """
        try:
            arff_dtype = PANDAS_TO_ARFF[pd_dtype]
        except KeyError:
            if pd_dtype == 'bool':
                # TODO: Implement this
                arff_dtype = self.map_column_to_arff_class(column)
            else:
                raise

        return arff_dtype

    def map_column_to_arff_class(self, column):
        """
        Converts 'bool' data type to arff format
        :return: arff class format
        """
        return "NOT YET IMPLEMENTED"

    def arff_rows(self):
        """
        Generator that yields arff rows from pandas dataframe
        :param data_frame: pandas dataframe
        :return: arff row
        """
        for pd_row in self.data_frame.values:
            row = [str(item) for item in pd_row if not isinstance(item, str) or item]
            yield row

if __name__ == '__main__':
    converter = ArffConverter()
    converter.main()
