Word Frequency Counter
==============================

What Is This?
-------------

This is a simple Python module which will extract content from web page and show most frequent word counts. The module is simple to understand, well-documented so any developer can use as a base and extend features.


How To Use This
---------------

1. Prerequesit to use this module is Python 3 to be installed on machine.
2. Clone this module from URL `https://github.com/rupeshtare/Word-Frequency-Counter.git`
3. Run `pip install -r requires_install.txt` to install dependencies
4. Import class `WordFrequencyCounter` from `word_frequency_counter.py` in your python code as below.
```python
from word_frequency_counter import WordFrequencyCounter
```
5. Create object of the class by passing expected input parameters as below.
```python
>>> obj = WordFrequencyCounter(
        url="https://www.314e.com/",
        most_frequent=10,
        url_level=4,
        word_frequency=[1,2,3,4]
)
```
* `url` is the URL name from which we want to extract data. this is required parameter while creating object
* `most_frequent`is the number of most frequent data. Default set to 10
* `url_level` Level of urls from given url we want to extract. Default set to 0
* `word_frequency` Number of consecutive frequent words which we want to check. We need to pass as list of number to this parameter. Default set to 1


6. Extract data from object using `get_data` method, Which will give you dictionary contains key `e.g. 1 ` as word frequency and value as ordered dict with word `e.g. This ` and count `e.g. 3 ` as below.
```python
>>> obj.get_data()
# output
{
    1: OrderedDict([('This', 3), ('is', 3), ('URL2', 3)]),
    2: OrderedDict([('This is', 3), ('is URL2', 3), ('URL2 This', 2)]),
    3: OrderedDict([('This is URL2', 3), ('is URL2 This', 2), ('URL2 This is', 2)]),
    4: OrderedDict([('This is URL2 This', 2), ('is URL2 This is', 2), ('URL2 This is URL2', 2)])
}
```

Testing
-------
This module is covered with 100% test coverage.

1. Install the dependencies with `pip install -r requires_install.txt`
2. Run the command `python .\test_suite.py`
```shell
>>>  python .\test_suite.py
.......
----------------------------------------------------------------------
Ran 7 tests in 0.005s

OK
```