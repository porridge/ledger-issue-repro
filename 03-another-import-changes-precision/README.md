# What this does

The `repro.py` script loads a journal consisting of a single three-posting transaction, and prints various attributes of the postings in the transaction.

It turns out that the output differs depending on whether the GTK library is also loaded an when.

The `repro.sh` script runs `repro.py` in three configurations, where the gtk module is loaded:
- not at all
- before the journal is loaded
- after the journal is loaded an queried, but before output is produced

# Output

```
$ ./repro.sh 2>/dev/null 
not loading gtk at all
query() returned 2 postings, for accounts: ['acct1', 'acct2']
account prec. d.prec. is_zero   number()                                                  truncated()                                                        str()                                                       repr()
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 acct1     5       5   False   29.43383                      29,43383 COMM {173,80 USD} [2000/01/01]                      29,43383 COMM {173,80 USD} [2000/01/01]                      29,43383 COMM {173,80 USD} [2000/01/01]
 acct2     2       2   False    -5115.6                                                 -5115,60 USD                                                 -5115,60 USD                                                 -5115,60 USD
  rest     7       2    True   0.000346                                                     0,00 USD                                                     0,00 USD                                                 0,000346 USD
loading gtk before journal load
query() returned 3 postings, for accounts: ['acct1', 'acct2', 'rest']
account prec. d.prec. is_zero   number()                                                  truncated()                                                        str()                                                       repr()
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 acct1     5       5   False   29,43383      29,43383 COMM {173,800000000000000000 USD} [2000/01/01]      29,43383 COMM {173,800000000000000000 USD} [2000/01/01]      29,43383 COMM {173,800000000000000000 USD} [2000/01/01]
 acct2     2       2   False   -5115,60                                                  -255,78 USD                                                 -5115,60 USD                                                 -5115,60 USD
  rest     7       2   False  0,0003460                                                     1,73 USD                                                     0,00 USD                                                0,0003460 USD
loading gtk after query
query() returned 2 postings, for accounts: ['acct1', 'acct2']
account prec. d.prec. is_zero   number()                                                  truncated()                                                        str()                                                       repr()
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 acct1     5       5   False   29,43383      29,43383 COMM {173,800000000000000000 USD} [2000/01/01]      29,43383 COMM {173,800000000000000000 USD} [2000/01/01]      29,43383 COMM {173,800000000000000000 USD} [2000/01/01]
 acct2     2       2   False   -5115,60                                                  -255,78 USD                                                 -5115,60 USD                                                 -5115,60 USD
  rest     7       2   False  0,0003460                                                     1,73 USD                                                     0,00 USD                                                0,0003460 USD
```

# Observations

## Not influenced by presence of GTK:

- `precision` is always:
  * 5 for `acct1`
  * 2 for `acct2`
  * 7 for `rest` 
- `display_precision` is always:
  * 5 for `acct1`
  * 2 for `acct2`
  * 2 for `rest` 

## Changes in behaviour

 Attribute |                              no gtk      |           loaded after query       |                       loaded before query
 ---- | ---- | ---- | ---- 
 number of postings returned by query |    2                          |     2                        |             3 (includes the `rest` one)
 `is_zero` for the `rest` account posting | True                      |     False                     |                False
 precision of `{price}` for `acct1`  |          2                     |         18                   |                     18
 `number()` decimal point character |               dot               |            comma             |                        comma
 `number()` precision               |       up to last non-zero digit  |   equal to precision        |               equal to precision
 `truncated()` of `acct2` posting       |    same as on input  |             1/20th of input             |               1/20th of input
 `truncated()` of `rest` posting      |   0,00              |          1,73 USD (1/100th of price, 1c prec.) |    1,73 USD (1/100th of price, up to 1c)
 precision of `repr()`            |           a least 2   |                     equal to `precision`          |             equal to `precision`


## Other remarks

When GTK is loaded before loading journal, the behaviour is the same as when
gtk is loaded after loading journal (but before `query()`).

Because of the `is_zero` difference, dividing the `rest` posting by itself
results in a division by zero error, depending on whether GTK is loaded or not.
