#!/usr/bin/python3
import locale
import argparse
import sys

import ledger

_transaction = """
2000-01-01 example
    acct1  29,43383 COMM @ 173,80 USD
    acct2  -5115,60 USD
    rest
"""


def main():
    args = get_args()

    if args.when_set_locale == "never":
        print("not setting locale at all")

    if args.when_set_locale == "at_start":
        print("setting locale before journal load")
        locale.setlocale(locale.LC_ALL, '')

    session, journal = load()
    postings = list(journal.query(""))

    if args.when_set_locale == "after_query":
        print("setting locale after query")
        locale.setlocale(locale.LC_ALL, '')

    print("query() returned %d postings, for accounts: %s" % (len(postings), [p.account.name for p in postings]))

    print_header()
    for subpost in postings[0].xact.posts():
       print_posting(subpost)
    sys.stdout.flush()


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("when_set_locale", choices=["never", "at_start", "after_query"], default="never")
    return parser.parse_args()


def load():
    session = ledger.Session()
    return session, session.read_journal_from_string(_transaction)


def print_header():
    h = []
    for width, label, _ in _formats:
        width = max(width, len(label))
        f = "%%%ds" % width
        h.append(f % label)
    h_str = " ".join(("account", " ".join(h)))
    print(h_str)
    print('-'*len(h_str))

def print_posting(p):
    print('%6s %s' % (p.account.name, format_amount(p.amount)))

def format_amount(amount):
    d = []
    for width, label, code in _formats:
        width = max(width, len(label))
        f = "%%%ds" % width
        val = code(amount)
        d.append(f % val)
    return " ".join(d)

_formats = [
  (2, "prec.", lambda a: a.precision),
  (2, "d.prec.", lambda a: a.display_precision),
  (2, "is_zero", lambda a: a.is_zero()),

  (10, "number()", lambda a: a.number()),
  (60, "truncated()", lambda a: a.truncated()),
  (60, "str()", lambda a: str(a)),
  (60, "repr()", lambda a: repr(a)),
]

main()
