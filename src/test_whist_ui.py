"""Automated unit tests for whist ui"""
from unittest import TestCase
import whist_api.ui_api.ui as ui

class TestUi(TestCase):
    """Class for testing whist ui, extends TestCase class"""
    def test_to_int(self):
        """Tests to_int function in whist ui"""
        result = ui.to_int("500")
        self.assertEqual(result, 500)
        result = ui.to_int("abcd")
        self.assertEqual(result, -1)

    def test_get_names_form(self):
        """Tests get_names_form function in whist ui"""
        self.assertRaises(ValueError, ui.get_names_form, "0ABCD")
        self.assertRaises(ValueError, ui.get_names_form, "-5")
        self.assertRaises(IOError, ui.get_names_form, 6)

    def test_get_players_number(self):
        """Tests get_players_number is whist ui"""
        self.assertRaises(IOError, ui.get_players_number)
