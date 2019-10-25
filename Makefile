init:
    pip install -r requirements.txt

test:
    py.test tests

run:
    python webapp.py

.PHONY: init run