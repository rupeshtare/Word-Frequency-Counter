# -*- coding: utf-8 -*-
"""
This module is used to parse word frequency from given url.
"""

import requests

from bs4 import BeautifulSoup, Tag
from collections import Counter, OrderedDict
from nltk import ngrams


class WordFrequencyCounter:
    """
    Class of Word Frequency Counter
    """

    def __init__(self, url, most_frequent=10, url_level=0, word_frequency=(1,)):
        """
        Constructor to initialise the object with given data.
        Args:
            url(str): Url name to parse.
            most_frequent(int): Number of  most frequent occurances. Default is 1.
            url_level(int): Number of maximum urls url_level. Default value is 0.
            word_frequency(tuple/list): How many word frequency we want to check. Default is 1 & 2 word frequency.
        """
        self.url = url
        self.most_frequent = most_frequent
        self.url_level = url_level
        self.word_frequency = word_frequency
        # To keep track of parsed urls
        self.urls = []        
        # To hold data of parsed urls
        self.data = []

    @staticmethod
    def _filter_data(data):
        """
        This method is used to filter given data.
        Args:
            data(str): 
        Returns: 
            returns filtered string
        """
        replace_chars = {"\t":" ", "\r":" ", "\n":" "}

        for i,j in replace_chars.items():
            data = data.replace(i,j)

        return data

    @staticmethod
    def _extract_tag_from_content(content, tag="body"):    
        """
        Method to extract given tag from given content
        Args:
            content(object): Content is beautifulsoap object
            tag(str): Tag which need to remove
        """
        body_tag = getattr(content, tag)
        
        if body_tag:
            return body_tag
        
        return content

    def _extract_data(self, content):
        """
        Extract data from given content.
        Args:
            content(object): Content is beautifulsoap object
        """
        content = self._extract_tag_from_content(content)

        for i in content.children:
            
            # if content has Tag type then only extract data from content
            if type(i) == Tag:
                text = self._filter_data(i.get_text())
                
                self.data.extend([t for t in text.split(" ") if t])

    def _extract_url(self, content, url_level):
        """
        Method to extract all the urls from given content.
        Once we extract all the urls it check for external url and ignore those and again call parse url for internal urls.
        Args:
            content(object): Content is beautifulsoap object
            url_level(int): Number of url level
        """
        tags = content.find_all('a')

        #iterate over all urls of current page
        for tag in tags:
            url = tag.get('href')
            
            # if url contains base url and url is not parsed already then parse the url
            if url.startswith(self.url) and url not in self.urls:
                self._parse_url(url, url_level)

    def _parse_url(self, url, url_level):
        """
        Method to parse given url and extract data.
        If url_level is less than expected url level then it extracts the url from given content,
        and again it will parse those urls
        Args:
            url(str): Url name to parse.
            url_level(int): Number of maximum url level
        """        
        # Reset to blank before parsing url
        if url_level == 0 and self.urls is None:
            self.urls = []
            self.data = []

        # To keep track of parsed url's. Create list with requested urls. 
        self.urls.append(url)
        
        response = requests.get(url)

        content = BeautifulSoup(response.content, 'html.parser')

        # If content is not none then extract data
        if content:
            self._extract_data(content)
        
        # If expected url_level is greater than current url level then extract other urls and parse those
        if self.url_level > url_level:
            url_level += 1
            self._extract_url(content, url_level)


    def get_data(self):
        """
        Method to return maximum occurances for given word frequency.
        """        
        self._parse_url(self.url, url_level=0)

        output = {}

        # if extracted data is present then check count for given word frequency
        if self.data:
            for w in self.word_frequency:
                output[w] = OrderedDict((" ".join(i[0]), i[1]) for i in Counter(list(ngrams(self.data, w))).most_common(self.most_frequent))
        
        return output
