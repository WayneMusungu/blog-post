import unittest
from blogpost.models import Quote

class TestQuote(unittest.TestCase):
    def setUp(self):
        """
        Set up method that will run before every Test
        """
        self.random_quote = Quote('Bruce', 'You can do it')

    def test_instance(self):
        self.assertTrue(isinstance(self.random_quote, Quote))

    def test_init(self):
        self.assertEqual(self.random_quote.author, 'Bruce')
        self.assertEqual(self.random_quote.quote,'You can do it')