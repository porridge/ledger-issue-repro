
.PHONY: repro
repro:
	ledger --version
	./repro repro.ledger
	./repro repro.ledger --invert
	./repro repro.ledger --collapse
	./repro repro.ledger --invert --collapse
