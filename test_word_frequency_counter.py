# -*- coding: utf-8 -*-
"""
Unittests for dtweb/utils/date_filter.py
"""

import requests
import unittest

from bs4 import BeautifulSoup
from collections import OrderedDict
from unittest import mock

from word_frequency_counter import WordFrequencyCounter


class TestWordFrequencyCounter(unittest.TestCase):
    """
    Tests for WordFrequencyCounter class
    """

    def setUp(self):
        self.wfc = WordFrequencyCounter(url="https://www.314e.com/")

    def test__filter_data(self):
        """
        Method to test filter data.
        """
        data = "This\tis\ra test \ndata"
        expected_data = "This is a test  data"
        self.assertEqual(self.wfc._filter_data(data), expected_data)

    def test__extract_tag_from_content(self):
        """
        Method to test remove tag from content
        """
        data = BeautifulSoup('<p>This is a slimy text and <i> I am slimer</i></p>', features="html.parser")
        self.assertEqual(self.wfc._extract_tag_from_content(data, tag="i"), data.i)

    
    def test__extract_tag_from_content_with_unavailable_tag(self):
        """
        Method to test remove tag from content if that given tag is not present
        """
        data = BeautifulSoup('<p>This is a slimy text and <i> I am slimer</i></p>', features="html.parser")
        self.assertEqual(self.wfc._extract_tag_from_content(data, tag="body"), data)

    def test__extract_data(self):
        """
        Method to test extract data from given content
        """
        data = BeautifulSoup('<p>This is a slimy text and <i> I am slimer</i></p>', features="html.parser")
        self.wfc._extract_data(data)
        expected_data = ['This', 'is', 'a', 'slimy', 'text', 'and', 'I', 'am', 'slimer']
        self.assertListEqual(self.wfc.data, expected_data)
    
    @mock.patch.object(WordFrequencyCounter, "_parse_url")
    def test__extract_url(self, mock__parse_url):
        """
        Method to test extract all urls from given content
        """
        mock__parse_url.return_value = None
        data = BeautifulSoup('<p><a href="https://www.314e.com/a">This</a> is a slimy text and <a href="https://www.314e.com/b">URL2</a></p>', features="html.parser")
        self.wfc._extract_url(data, url_level=0)
        self.assertEqual(mock__parse_url.call_count, 2)

    @mock.patch.object(requests, "get")
    def test__parse_url(self, mock_get):
        """
        Method to test parse url
        """
        self.wfc.url_level = 1
        mock_get.return_value.content = '<p><a href="https://www.314e.com/a">This</a> is <a href="https://www.314e.com/b">URL2</a></p>'
        self.wfc._parse_url(url="https://www.314e.com/", url_level=0)
        expected_url = ['https://www.314e.com/', 'https://www.314e.com/a', 'https://www.314e.com/b']
        expected_data = ['This', 'is', 'URL2'] * 3
        self.assertListEqual(self.wfc.urls, expected_url)
        self.assertListEqual(self.wfc.data, expected_data)

    @mock.patch.object(WordFrequencyCounter, "_parse_url")
    def test_get_data(self, mock__parse_url):
        """
        Method to test maximum occurances for given word frequency
        """
        self.wfc.data = ['This', 'is', 'URL2'] * 3
        output = {1: OrderedDict([('This', 3), ('is', 3), ('URL2', 3)])}
        self.assertDictEqual(self.wfc.get_data(), output)

        # test for 2, 3 and 4 contineous frequent words
        self.wfc.word_frequency = [2,3,4]
        output = {
            2: OrderedDict([('This is', 3), ('is URL2', 3), ('URL2 This', 2)]),
            3: OrderedDict([('This is URL2', 3), ('is URL2 This', 2), ('URL2 This is', 2)]),
            4: OrderedDict([('This is URL2 This', 2), ('is URL2 This is', 2), ('URL2 This is URL2', 2)])
        }
        self.assertDictEqual(self.wfc.get_data(), output)
