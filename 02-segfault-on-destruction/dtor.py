import ledger
session = ledger.Session()
j = session.read_journal_from_string("""
2017-11-23 example
    acct1  1 USD
    acct2
""")

for post in j.query(""):
    pass
print("Done.")
