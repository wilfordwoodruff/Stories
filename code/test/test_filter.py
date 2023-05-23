import os
import sys
import unittest
import pandas as pd
from unittest.mock import patch, mock_open

# Get the absolute path to the directory containing filter_data.py
filter_data_directory = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), 'code/pipe')
sys.path.insert(0, filter_data_directory)

from filter_data import filter_by_document_type, filter_by_keyword, filter_by_topic, filter_by_date_range


class TestFilterData(unittest.TestCase):
    @patch('pandas.read_csv')
    def test_filter_by_document_type(self, mock_read_csv):
        # Setup
        df = pd.DataFrame({
            'Document Type': ['Journals', 'Letters', None, 'Daybooks', 'Discourses']
        })
        mock_read_csv.return_value = df

        # Call function
        filtered_df = filter_by_document_type(df, 'Journals')

        # Asserts
        self.assertEqual(len(filtered_df), 1)
        self.assertEqual(filtered_df['Document Type'].iloc[0], 'Journals')

    @patch('pandas.read_csv')
    def test_filter_by_keyword(self, mock_read_csv):
        # Setup
        df = pd.DataFrame({
            'Text Only Transcript': ['Truth is always true', 'I love my dog', 'My car is red', None]
        })
        mock_read_csv.return_value = df

        # Call function
        filtered_df = filter_by_keyword(df, 'Truth')

        # Asserts
        self.assertEqual(len(filtered_df), 1)
        self.assertEqual(filtered_df['Text Only Transcript'].iloc[0], 'Truth is always true')

    @patch('pandas.read_csv')
    def test_filter_by_topic(self, mock_read_csv):
        # Setup
        df = pd.DataFrame({
            'Topics': ['Doctrine and Covenants|faith', 'repentance|forgiveness', None, 'Doctrine and Covenants|prophecy']
        })
        mock_read_csv.return_value = df

        # Call function
        filtered_df = filter_by_topic(df, 'Doctrine and Covenants')

        # Asserts
        self.assertEqual(len(filtered_df), 2)
        self.assertTrue('Doctrine and Covenants' in filtered_df['Topics'].iloc[0])
        self.assertTrue('Doctrine and Covenants' in filtered_df['Topics'].iloc[1])

    @patch('pandas.read_csv')
    def test_filter_by_date_range(self, mock_read_csv):
        # Setup
        df = pd.DataFrame({
            'Dates': ['1836-09-10', '1836-09-11', '1836-09-12', '1836-09-13']
        })
        mock_read_csv.return_value = df

        # Call function
        filtered_df = filter_by_date_range(df, '1836-09-10', '1836-09-12')

        # Asserts
        self.assertEqual(len(filtered_df), 3)
        self.assertEqual(filtered_df['Dates'].iloc[0], '1836-09-10')
        self.assertEqual(filtered_df['Dates'].iloc[1], '1836-09-11')
        self.assertEqual(filtered_df['Dates'].iloc[2], '1836-09-12')


if __name__ == '__main__':
    unittest.main()
