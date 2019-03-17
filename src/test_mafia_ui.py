from unittest import TestCase
import mafia_api.ui_api.ui as ui

class TestUi(TestCase):

    def test_to_int(self):
        result = ui.to_int("500")
        self.assertEqual(result, 500)
        result = ui.to_int("abcd")
        self.assertEqual(result, -1)

    def test_get_emails_form(self):
        self.assertRaises(ValueError, ui.get_emails_form, "0ABCD")
        self.assertRaises(ValueError, ui.get_emails_form, "-5")

    def test_get_players_number(self):
        self.assertRaises(IOError, ui.get_players_number)
