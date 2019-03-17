"""Automated unit tests for mafia ui"""
from unittest import TestCase
import mafia_api.ui_api.ui as ui

class TestUi(TestCase):
    """Class for testing mafia ui, extends TestCase class"""
    def test_to_int(self):
        """Tests to_int function in mafia ui"""
        result = ui.to_int("500")
        self.assertEqual(result, 500)
        result = ui.to_int("abcd")
        self.assertEqual(result, -1)

    def test_get_emails_form(self):
        """Tests get_emails_form function in mafia ui"""
        self.assertRaises(ValueError, ui.get_emails_form, "0ABCD")
        self.assertRaises(ValueError, ui.get_emails_form, "-5")
        self.assertRaises(IOError, ui.get_emails_form, 6)

    def test_get_players_number(self):
        """Tests get_players_number function in mafia ui"""
        self.assertRaises(IOError, ui.get_players_number)
