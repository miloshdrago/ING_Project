#!/usr/bin/env python3
"""
Test case for the `TransactionGenerator` class. This class is supposed to generate
a sample distribution of transactions according to a timespan.

@author Tycho Atsma <tycho.atsma@gmail.com>
@file   tests/TransactionGenerator.py
"""

# dependencies
import unittest
from src.TransactionGenerator import TransactionGenerator

class TransactionGeneratorTestCase(unittest.TestCase):

    def test_minutely(self):
        gen = TransactionGenerator()
        minutely = gen.minutely()

        # should be a list
        self.assertTrue(isinstance(minutely, list))

        # should be the lenght of a minute in seconds
        self.assertEqual(len(minutely), 60)
    
    def test_hourly(self):
        gen = TransactionGenerator()
        hourly = gen.hourly()

        # should be a list
        self.assertTrue(isinstance(hourly, list))

        # should be the lenght of an hour in minutes
        self.assertEqual(len(hourly), 60)

    def test_daily(self):
        gen = TransactionGenerator()
        daily = gen.daily()

        # should be a list
        self.assertTrue(isinstance(daily, list))

        # should be the lenght of a day in hours
        self.assertEqual(len(daily), 24)

    def test_weekly(self):
        gen = TransactionGenerator()
        weekly = gen.weekly()

        # should be a list
        self.assertTrue(isinstance(weekly, list))

        # should be the lenght of a week in days
        self.assertEqual(len(weekly), 7)

# run test as main
if __name__ == "__main__":
    unittest.main()