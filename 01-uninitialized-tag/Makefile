
.PHONY: repro
repro:
	ledger --version
	./repro repro1.ledger
	./repro repro2.ledger
	cat repro1.ledger repro2.ledger > repro.ledger
	./repro repro.ledger
