import unittest

from app.main.service.pycountry_service import country_to_isocode

country_isocode = [('France', 'FR'), ('United States of America', 'US'), ('United States', 'US'), ('Botswana', 'BW')]

class MyTestCase(unittest.TestCase):
    def test_country_to_isocode_return_isocode(self):
        for country_name, isocode in country_isocode:
            with self.subTest():
                self.assertEqual(isocode, country_to_isocode(country_name))

    def test_unknown_country_to_isocode_return_none(self):
        self.assertIsNone(country_to_isocode('unknown country'))

if __name__ == '__main__':
    unittest.main()
