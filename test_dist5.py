# import unittest
# from unittest.mock import patch, mock_open
# from dist5 import upload_file, download_file, get_saveas_filename, get_open_filename

# class TestFileFunctions(unittest.TestCase):

#     def setUp(self):
#         # Set up any necessary test data or configuration here
#         pass

#     def tearDown(self):
#         # Clean up after each test if needed
#         pass

#     @patch('os.path.basename', return_value='test_source.txt')
#     @patch('builtins.open', new_callable=mock_open())
#     @patch('tkinter.Listbox.curselection', return_value=(0,))
#     @patch('tkinter.Listbox.get', return_value='test_file.txt')
#     @patch('your_module_filename.get_saveas_filename', return_value='test_destination.txt')
#     def test_download_file_successful(self, mock_saveas_filename, mock_get, mock_curselection, mock_open_func, mock_open_filename):
#         # Call the download_file function
#         download_file()

#         # Assert your expectations here

#     @patch('builtins.open', new_callable=mock_open())
#     @patch('tkinter.Listbox.get', return_value='test_source.txt')
#     @patch('your_module_filename.get_open_filename', return_value='test_source.txt')
#     def test_upload_file_successful(self, mock_get_open_filename, mock_get_listbox, mock_open_func):
#         # Call the upload_file function
#         upload_file()

#         # Assert your expectations here

# if __name__ == '__main__':
#     unittest.main()

import unittest

# Function to add two numbers
def add_numbers(a, b):
    return a + b

# Function to multiply two numbers
def multiply_numbers(a, b):
    return a * b

# Unit tests for the functions
class TestMathFunctions(unittest.TestCase):

    def test_add_numbers(self):
        result = add_numbers(2, 3)
        self.assertEqual(result, 5)

        result = add_numbers(-1, 5)
        self.assertEqual(result, 4)

        result = add_numbers(0, 0)
        self.assertEqual(result, 0)

    def test_multiply_numbers(self):
        result = multiply_numbers(2, 3)
        self.assertEqual(result, 6)

        result = multiply_numbers(-1, 5)
        self.assertEqual(result, -5)

        result = multiply_numbers(0, 5)
        self.assertEqual(result, 0)

if __name__ == '__main__':
    unittest.main()
