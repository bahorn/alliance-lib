check: test mypy pylint

test:
	pytest

mypy:
	mypy alliancelib

pylint:
	pylint alliancelib --disable=R0801

