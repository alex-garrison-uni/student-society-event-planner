This repository contains Group 28's code and documentation for the ECM1414 Coursework.

To install development enviroment:  
```bash
uv sync --inexact
uv pip install -e .
source .venv/bin/activate
```

How to run:  
```bash
python3 main.py INPUT_FILE

# e.g running with the small input file
python3 main.py input_small.txt
```

How to run tests:  
```bash
uv run pytest
```