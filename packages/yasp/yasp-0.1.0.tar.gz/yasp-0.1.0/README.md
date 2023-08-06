# YASP

Yet another Apertium stream parser

## Usage

```
>>> from pprint import pprint
>>> import yasp
>>> pprint(yasp.stream.parse('^prpers<prn><subj><p1><mf><sg>$ ^saw<vblex><pres>$ ^a<det><ind><sg>$ ^cat<n><sg>$'))
[('LEXICAL-UNIT',
  [{'FLAG': '',
    'INVARIABLE-PART0': [],
    'INVARIABLE-PART1': [],
    'LING-FORM': 'prpers',
    'TAGS': ['prn', 'subj', 'p1', 'mf', 'sg']}]),
 ('UNPARSED', ' '),
 ('LEXICAL-UNIT',
  [{'FLAG': '',
    'INVARIABLE-PART0': [],
    'INVARIABLE-PART1': [],
    'LING-FORM': 'saw',
    'TAGS': ['vblex', 'pres']}]),
 ('UNPARSED', ' '),
 ('LEXICAL-UNIT',
  [{'FLAG': '',
    'INVARIABLE-PART0': [],
    'INVARIABLE-PART1': [],
    'LING-FORM': 'a',
    'TAGS': ['det', 'ind', 'sg']}]),
 ('UNPARSED', ' '),
 ('LEXICAL-UNIT',
  [{'FLAG': '',
    'INVARIABLE-PART0': [],
    'INVARIABLE-PART1': [],
    'LING-FORM': 'cat',
    'TAGS': ['n', 'sg']}])]
>>> 
```
