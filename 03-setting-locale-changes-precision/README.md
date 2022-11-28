# What this does

The `repro.py` script loads a journal consisting of the following single transaction that contains three postings.
Then it and prints various attributes of the postings in the transaction.

```
2000-01-01 example
    acct1  29,43383 COMM @ 173,80 USD
    acct2  -5115,60 USD
    rest
```

FWIW, (29,43383 * 173,80) equals 5115,599654.


It turns out that the values and even visibility of some postings differs depending on whether the locale is set, and when!

The `repro.sh` script runs `repro.py` in three configurations, where the locale is set:
- not at all
- before the journal is loaded
- after the journal is loaded an queried, but before output is produced

# Output

```
$ ./repro.sh 2>/dev/null 
not setting locale at all
query() returned 2 postings, for accounts: ['acct1', 'acct2']
account prec. d.prec. is_zero   number()                                                  truncated()                                                        str()                                                       repr()
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 acct1     5       5   False   29.43383                      29,43383 COMM {173,80 USD} [2000/01/01]                      29,43383 COMM {173,80 USD} [2000/01/01]                      29,43383 COMM {173,80 USD} [2000/01/01]
 acct2     2       2   False    -5115.6                                                 -5115,60 USD                                                 -5115,60 USD                                                 -5115,60 USD
  rest     7       2    True   0.000346                                                     0,00 USD                                                     0,00 USD                                                 0,000346 USD
setting locale before journal load
query() returned 3 postings, for accounts: ['acct1', 'acct2', 'rest']
account prec. d.prec. is_zero   number()                                                  truncated()                                                        str()                                                       repr()
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 acct1     5       5   False   29,43383      29,43383 COMM {173,800000000000000000 USD} [2000/01/01]      29,43383 COMM {173,800000000000000000 USD} [2000/01/01]      29,43383 COMM {173,800000000000000000 USD} [2000/01/01]
 acct2     2       2   False   -5115,60                                                  -255,78 USD                                                 -5115,60 USD                                                 -5115,60 USD
  rest     7       2   False  0,0003460                                                     1,73 USD                                                     0,00 USD                                                0,0003460 USD
setting locale after query
query() returned 2 postings, for accounts: ['acct1', 'acct2']
account prec. d.prec. is_zero   number()                                                  truncated()                                                        str()                                                       repr()
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 acct1     5       5   False   29,43383      29,43383 COMM {173,800000000000000000 USD} [2000/01/01]      29,43383 COMM {173,800000000000000000 USD} [2000/01/01]      29,43383 COMM {173,800000000000000000 USD} [2000/01/01]
 acct2     2       2   False   -5115,60                                                  -255,78 USD                                                 -5115,60 USD                                                 -5115,60 USD
  rest     7       2   False  0,0003460                                                     1,73 USD                                                     0,00 USD                                                0,0003460 USD
```

The above is with:
- amd64
- python3-ledger 3.2.1-8+b5
- python3        3.10.6-1
- locale `pl_PL.UTF-8`

# Observations

## Not influenced by presence or lack of set locale

- `precision` is always:
  * 5 for `acct1`
  * 2 for `acct2`
  * 7 for `rest` 
- `display_precision` is always:
  * 5 for `acct1`
  * 2 for `acct2`
  * 2 for `rest` 
- list of postings returned by calling `.xact.posts()` always has three elements, regardless of how many postings were returned by `query()`

## Changes in behaviour depending on if and when locale is set

 Attribute |                                      locale not set |           locale set after `query()`       |            locale set before `query()`
 ---- | ---- | ---- | ---- 
 number of postings returned by `journal.query()` |    2                          |     2                        |             3 (includes the `rest` one)
 `is_zero()` for the `rest` account posting | True                      |     False                     |                False
 precision of `{price}` for `acct1`  |          2                     |         18                   |                     18
 `number()` decimal point character |               dot               |            comma             |                        comma
 `number()` precision               |       up to last non-zero digit  |   equal to precision        |               equal to precision
 `truncated()` of `acct2` posting       |    same as on input  |             1/20th of input             |               1/20th of input
 `truncated()` of `rest` posting      |   0,00              |          1,73 USD (1/100th of price, 1c prec.) |    1,73 USD (1/100th of price, up to 1c)
 precision of `repr()`            |           a least 2   |                     equal to `precision`          |             equal to `precision`


## Other remarks

When locale is set before loading journal, the behaviour is the same as when
the locale is set after loading journal (but before `query()`).

Because of the `is_zero` difference, dividing the `rest` posting by itself
results in a division by zero error, depending on whether locale is set or not.
This is how I noticed this variance in the first place.

Setting the locale happens for example as a side effect of loading the GTK+ library.

### Locale-specific numeric and monetary parameters

See [docs](https://docs.python.org/3/library/locale.html#locale.localeconv) for description.

```
>>> pprint.pprint(locale.localeconv())
{'currency_symbol': '',
 'decimal_point': '.',
 'frac_digits': 127,
 'grouping': [],
 'int_curr_symbol': '',
 'int_frac_digits': 127,
 'mon_decimal_point': '',
 'mon_grouping': [],
 'mon_thousands_sep': '',
 'n_cs_precedes': 127,
 'n_sep_by_space': 127,
 'n_sign_posn': 127,
 'negative_sign': '',
 'p_cs_precedes': 127,
 'p_sep_by_space': 127,
 'p_sign_posn': 127,
 'positive_sign': '',
 'thousands_sep': ''}
>>> locale.setlocale(locale.LC_ALL, '')
'pl_PL.UTF-8'
>>> pprint.pprint(locale.localeconv())
{'currency_symbol': 'zł',
 'decimal_point': ',',
 'frac_digits': 2,
 'grouping': [3, 0],
 'int_curr_symbol': 'PLN ',
 'int_frac_digits': 2,
 'mon_decimal_point': ',',
 'mon_grouping': [3, 0],
 'mon_thousands_sep': '\u202f',
 'n_cs_precedes': 0,
 'n_sep_by_space': 1,
 'n_sign_posn': 1,
 'negative_sign': '-',
 'p_cs_precedes': 0,
 'p_sep_by_space': 1,
 'p_sign_posn': 1,
 'positive_sign': '',
 'thousands_sep': '\u202f'}
>>> 
```

## Thoughts and questions

I did read the [Journal File Format for Developers](https://www.ledger-cli.org/3.0/doc/ledger3.html#Journal-File-Format-for-Developers) section of the documentation, but some things are still a mystery:

1. Why does `query()` return a different set of postings depending on the locale, while `.xact.posts()` always returns three? I suspect this is because `query()` omits postings whose `is_zero()` returns `True`, while `.xact.posts()` always returns all postings?
2. Why is the result of `is_zero()` on a value of `0.000346` locale-dependent? I suspect that the locale-specified precision somehow influences that decision. However I cannot see anything in the output of `localeconv()` that could cause precision to go so high (`frac_digits` is just 2).
3. Why does the precision of the commodity price go as high as 18?
4. What is the meaning of the value returned by `truncated()`? It seems to make no sense at all for all but one posting in the locale-enabled cases.
