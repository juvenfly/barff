import pandas as pd

from maps import PANDAS_TO_ARFF, CSV_TO_PANDAS


class ArffConverter(object):

    def __init__(self, input_file, output_file, relation, field_map=None):
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
        self.relation = relation
        self.field_map = field_map

    def main(self):
        self.data_frame = pd.read_csv(self.input_file, dtype=self.field_map)

        self.collect_comments()

        self.output_file.write('@RELATION {} \n\n'.format(quote_if_space(self.relation)))

        arff_header = self.convert_header()

        for line in arff_header:
            self.output_file.write(line)

        self.output_file.write('\n@DATA\n')

        for row in self.arff_rows():
            self.output_file.write(row)

        self.output_file.close()

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

    def map_column_to_arff_class(self, column):
        """
        Converts 'bool' data type to arff format
        :param column: column in pandas dataframe
        :return: arff class format
        """
        unique_vals = [str(val) for val in self.data_frame[column].unique() if not isinstance(val, str) or val]
        result = '{' + ','.join(unique_vals) + '}'

        return result

    def arff_rows(self):
        """
        Generator that yields arff rows from pandas dataframe
        :return: arff row
        """
        for pd_row in self.data_frame.values:
            vals = [str(item) for item in pd_row if not isinstance(item, str) or item]
            row = ','.join(vals) + '\n'
            row = [format_val(val) for val in row.split(',')]
            row = ','.join(row)
            yield row


def format_val(val):
    """
    Helper method that applies all formatting methods on a given val.
    :param val: raw value as string
    :return: formatted string
    """
    result = val
    result = quote_if_space(result)
    result = replace_nans(result)
    return result


def quote_if_space(val):
    """
    Adds double quotes around a string value if it contains a space.
    :param val: raw value as string
    :return: formatted string
    """
    result = val
    if ' ' in val:
        result = '"' + val + '"'
    return result


def replace_nans(val):
    """
    Replaces nan values with single question mark
    :param val: raw value as string
    :return: formatted string
    """
    # TODO: Ideally this should happen earlier, before pandas NaN is stringified and .lower()ed for safety's sake.
    result = val
    if val == 'nan':
        result = '?'
    return result


if __name__ == '__main__':
    converter = ArffConverter(
        input_file='./tests/test_input.csv',
        output_file='./tmp/output.arff',
        relation='test relation',
        field_map=CSV_TO_PANDAS,
    )
    converter.main()
