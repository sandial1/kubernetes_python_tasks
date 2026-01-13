# Kubernetes Python Tasks

## Overview
This project provides Python utilities and tasks for managing Kubernetes clusters and workloads.

## Exercises
- Dictionary class - dictionary.py
- How much will you spend? - spending.py
- Nth-char word - nth_char.py

## Observations
0. To solve these katas I adopted a simple mindset: these are elementary and such what I need is to stablish a framework that can solve the issue, test it and expand on it which lead me to stablishing an uv pyrthon project with pytest and ruff as basis to dive deep in the tasks.
1. Every task assumes ideal conditions so validation, logging and error handling can be added to extend the functionality of these algorithms.
2. These tasks are basically extract and transform operations which are part of the data preparation steps and as such pipelined and scaled.
3. Following the idea that these are ETL substitute funtions we could create a container based workload which to scale them and automate them in a single project pipeline.


## Requirements & setup
1. Clone the repository
2. Install dependencies: `uv install`

## Usage
```bash
# Example usage
uv run pytest
```

## Project Structure
```
kubernetes_python_tasks/
├── README.md
├── src/
├───├─ exercises/
└───├─ tests/
```

## Requirements
- Python 3.11+
- uv 0.7.12

## License
MIT