# integration_test.py
import unittest
from unittest.mock import MagicMock
from first_component import create_list, save_to_database
from second_component import perform_math_operation_and_create_list

class TestIntegration(unittest.TestCase):

    def test_integration_scenario(self):
        # Mock the external dependency (database)
        mock_database = MagicMock()

        # Test case: Call the second component, which internally uses the first component
        perform_math_operation_and_create_list(database=mock_database)

        # Assert that the create_list function from the first component was called
        mock_database.save.assert_called_once()
        create_list.assert_called_once()

if __name__ == "__main__":
    unittest.main()