# Setup Guide

Setup virtual environment

```python -m venv venv```

Activate venv

```source venv/bin/activate```

Install dependencies

```pip install -r requirements.txt```

Run script

```python csv_reconciler.py -s ./input/source.csv -t ./input/target.csv -o output.csv```

# Checklist
| Task                         | Completed |
|------------------------------|-----------|
| Reconciler CLI               | [x] |
| Unit Test                    | [x] |
| CI                           | [x] |
| Web UI (Next JS + Fast API)  | [ ] |