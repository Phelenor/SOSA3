import math
import unittest
from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from main import OperationsManager, login_success, main


class OperationsManagerTests(TestCase):

    def setUp(self):
        self.ops_manager = OperationsManager(float('nan'), float('nan'))

    def test_perform_division(self):
        self.ops_manager.a = 10
        self.ops_manager.b = 5

        result = self.ops_manager.perform_division()

        self.assertEqual(result, 2)

    def test_perform_division_with_zero(self):
        self.ops_manager.a = 10
        self.ops_manager.b = 0

        try:
            result = self.ops_manager.perform_division()
        except ZeroDivisionError:
            result = 0

        self.assertTrue(math.isnan(result))

    def test_perform_division_with_decimals(self):
        self.ops_manager.a = 10
        self.ops_manager.b = 6

        result = self.ops_manager.perform_division()

        self.assertAlmostEqual(result, 10 / 6)


class LoginTests(unittest.TestCase):

    @patch('builtins.input', side_effect=["root"])
    @patch('getpass.getpass', return_value="nope")
    def test_unsuccessful_login(self, mock_getpass, mock_input):
        with patch('sys.stdout', new=StringIO()) as mock_output:
            main()
            self.assertEqual(mock_output.getvalue(), "Wrong username or password!\n")

    @patch('builtins.input', side_effect=["root", "5", "2", "5 + 2"])
    @patch('getpass.getpass', return_value="123")
    def test_successful_login(self, mock_getpass, mock_input):
        with patch('sys.stdout', new=StringIO()) as mock_output:
            main()
            self.assertEqual(mock_output.getvalue(), "Login success!\n2.5\nResult:  7\n")


class LoginSuccessTests(unittest.TestCase):

    @patch('builtins.input', side_effect=["10", "5", "2 + 2"])
    def test_login_success(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as mock_output:
            login_success()

            output = mock_output.getvalue()

            self.assertIn("2.0", output)
            self.assertIn("Result:  4", output)

    @patch('builtins.input', side_effect=["10", "0", "2 / 2"])
    def test_login_success_divide_by_zero(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as mock_output:
            login_success()
            self.assertEqual(mock_output.getvalue(), "nan\nResult:  1.0\n")

    @patch('builtins.input', side_effect=["invalid", "5"])
    def test_login_success_invalid_number_input(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as mock_output:
            with self.assertRaises(ValueError):
                login_success()


if __name__ == '__main__':
    unittest.main()
