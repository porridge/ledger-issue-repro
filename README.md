# Weird things that I encountered with ledger

This is a staging area where I experiment with and iterate on reproduction
cases for unexpected behavior I found in ledger.

- [01-uninitialized-tag](01-uninitialized-tag) - [tags become spontaneously corrupted](https://github.com/ledger/ledger/issues/1993) - see also other branches that iterate on this case
- [02-segfault-on-destruction](02-segfault-on-destruction) - [Python program crashes on exit](https://bugs.debian.org/1024389)
