# YASP

Yet another Apertium stream parser

## Usage

```
>>> from pprint import pprint
>>> import yasp
>>> pprint(yasp.stream.parse('^prpers<prn><subj><p1><mf><sg>$ ^saw<vblex><pres>$ ^a<det><ind><sg>$ ^cat<n><sg>$'))
[('LEXICAL-UNIT',
  [(('FLAG', ''),
    ('LING-FORM', 'prpers'),
    ('INVARIABLE-PART', []),
    ('TAGS', ['prn', 'subj', 'p1', 'mf', 'sg']),
    ('INVARIABLE-PART', []))]),
 ('UNPARSED', ' '),
 ('LEXICAL-UNIT',
  [(('FLAG', ''),
    ('LING-FORM', 'saw'),
    ('INVARIABLE-PART', []),
    ('TAGS', ['vblex', 'pres']),
    ('INVARIABLE-PART', []))]),
 ('UNPARSED', ' '),
 ('LEXICAL-UNIT',
  [(('FLAG', ''),
    ('LING-FORM', 'a'),
    ('INVARIABLE-PART', []),
    ('TAGS', ['det', 'ind', 'sg']),
    ('INVARIABLE-PART', []))]),
 ('UNPARSED', ' '),
 ('LEXICAL-UNIT',
  [(('FLAG', ''),
    ('LING-FORM', 'cat'),
    ('INVARIABLE-PART', []),
    ('TAGS', ['n', 'sg']),
    ('INVARIABLE-PART', []))])]
>>> 
```
