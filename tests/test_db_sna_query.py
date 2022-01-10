
import unittest

from src.models.SNAPreference import SNAPreferences, SNAPreferencesQuery
from tests.test_base_case import BaseTestCase

class SNATestCase(BaseTestCase):

    def setUp(self) -> None:
        self.check_type = ["string", 1.5, True, list(), dict(), tuple()]
        self.selected_key = int(max(self.app.config["METRIC"].keys())) + 1
        self.app.config["METRIC"][self.selected_key] = "test_case"

    def tearDown(self) -> None:
        del self.check_type
        del self.app.config["METRIC"][self.selected_key]
        del self.selected_key

    # check instance
    def test_sna_instance(self):
        sna_pref_var = SNAPreferencesQuery(1,2,3)
        self.assertIsInstance(sna_pref_var.sna, SNAPreferences)
    
    # check type
    def test_metric_id_type(self):
        for checktyp in self.check_type:
            print(checktyp)
            self.assertRaises(TypeError, SNAPreferencesQuery(checktyp, 1, 2))

    def test_layout_id_type(self):
        for checktyp in self.check_type:
            self.assertRaises(TypeError, SNAPreferencesQuery(1, checktyp, 2))
        
    def test_file_id_type(self):
        for checktyp in self.check_type:
            self.assertRaises(TypeError, SNAPreferencesQuery(1, 2, checktyp))

    # check existence
    def test_metric_id_existence(self):
        self.assertRaises(KeyError, SNAPreferencesQuery(1, 2, self.selected_key))

    def test_layout_id_existence(self):
        self.assertRaises(KeyError, SNAPreferencesQuery(1, 2, self.selected_key))

    def test_file_id_existence(self):
        selected_file_id = 0
        self.assertRaises(KeyError, SNAPreferencesQuery(1, 2, selected_file_id))
    
    # check positive
    def test_metric_id_positive_integer(self):
        self.assertRaises(ValueError, SNAPreferencesQuery(-1, 0, 0))

    def test_layout_id_positive_integer(self):
        self.assertRaises(ValueError, SNAPreferencesQuery(0, -1, 0))
    
    def test_file_id_positive_integer(self):
        self.assertRaises(ValueError, SNAPreferencesQuery(0, 0, -1))

    #check_file_id_exist_in_database
    """
    def test_sna_save(self):
        self.asset
    """


if __name__ == '__main__':
    unittest.main()


"""
if type(metric_id) is not int or type(layout_id) is not int or type(file_id) is not int:
    raise TypeError("Parameters must be integer")
        
if metric_id < 0 or metric_id >= len(app.config["METRIC"]):
    raise ValueError("The value must be greater than 0 and less than the initial METRIC size")

if layout_id >= 0 and layout_id < len(app.config["LAYOUT"]):
    raise ValueError("The value must be greater than or equal to 0 and less than the initial METRIC size")


"""