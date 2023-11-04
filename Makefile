run:
	./run.sh

lizard:
	lizard app -o quality.html

test: FORCE
	python -m unittest discover -s test/unit -p '*_test.py'

FORCE:
