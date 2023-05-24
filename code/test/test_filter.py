import os
import sys
import unittest
import pandas as pd
from unittest.mock import patch, mock_open
from fuzzywuzzy import fuzz

# Get the absolute path to the directory containing filter_data.py
filter_data_directory = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))), 'code/pipe')
sys.path.insert(0, filter_data_directory)

from filter_data import filter_by_document_type, filter_by_keyword, filter_by_topic, filter_by_date_range


class TestFilterFunctions(unittest.TestCase):
    @patch('pandas.read_csv')
    def test_filter_by_document_type(self, mock_read_csv):
        # Setup
        df = pd.DataFrame({
            'Document Type': ['Journals', 'Letters', 'Autobiographies'],
            'Text Only Transcript': ['Text 1', 'Text 2', 'Text 3']
        })
        mock_read_csv.return_value = df

        # Call function
        filtered_df = filter_by_document_type(df, 'Journals')

        # Asserts
        mock_read_csv.assert_not_called()  # Ensure read_csv is not called within the function
        self.assertEqual(filtered_df.shape[0], 1)  # The filtered DataFrame should have 1 row
        self.assertEqual(filtered_df.iloc[0]['Document Type'], 'Journals')  # The row should have the correct document type

    @patch('pandas.read_csv')
    def test_filter_by_keyword(self, mock_read_csv):
        # Setup
        df = pd.DataFrame({
            'Document Type': ['Journals', 'Letters', 'Autobiographies'],
            'Text Only Transcript': ['Fish', 'Prophet', 'Family']
        })
        mock_read_csv.return_value = df

        # Call function
        filtered_df = filter_by_keyword(df, 'truth', threshold=80)

        # Asserts
        mock_read_csv.assert_not_called()
        self.assertEqual(filtered_df.shape[0], 0)  # There should be no matching rows
        self.assertTrue(filtered_df.empty)  # The filtered DataFrame should be empty

    @patch('pandas.read_csv')
    def test_filter_by_topic(self, mock_read_csv):
        # Setup
        df = pd.DataFrame({
            'Document Type': ['Journals', 'Letters', 'Autobiographies'],
            'Topics': ['Doctrine and Covenants', 'History', 'Doctrine']
        })
        mock_read_csv.return_value = df

        # Call function
        filtered_df = filter_by_topic(df, 'Doctrine and Covenants')

        # Asserts
        mock_read_csv.assert_not_called()
        self.assertEqual(filtered_df.shape[0], 1)  # The filtered DataFrame should have 1 row
        self.assertEqual(filtered_df.iloc[0]['Topics'], 'Doctrine and Covenants')  # The row should have the correct topic

    @patch('pandas.read_csv')
    def test_filter_by_keyword(self, mock_read_csv):
        # Setup
        df = pd.DataFrame({
            'Document Type': ['Journals', 'Letters', 'Autobiographies'],
            'Text Only Transcript': ['Fish', 'Prophet', 'Family']
        })
        mock_read_csv.return_value = df

        # Call function
        filtered_df = filter_by_keyword(df, 'truth', threshold=80)

        # Asserts
        mock_read_csv.assert_not_called()
        self.assertEqual(filtered_df.shape[0], 0)  # There should be no matching rows
        self.assertTrue(filtered_df.empty)  # The filtered DataFrame should be empty

if __name__ == '__main__':
    unittest.main()
