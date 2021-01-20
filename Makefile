
.PHONY: repro
repro:
	ledger --version
	cat repro1.ledger repro2.ledger > repro.ledger
	./repro repro1.ledger
	./repro repro2.ledger
	./repro repro.ledger
