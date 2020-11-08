import unittest
from test_word_frequency_counter import TestWordFrequencyCounter

suite = unittest.TestLoader().loadTestsFromTestCase(TestWordFrequencyCounter)
unittest.TextTestRunner(verbosity=1).run(suite)