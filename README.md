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

## Project scope redefinement
The project was redefined as using the Katas codes as a basis stump to challenge ourselves to learn a new tool. 
I choose the following:
- Phase 1: FastAPI. Simple with its own Swagger docs
- Phase 2: Containeraze it. Make it run with docker compose with a PostreSQL database.
- Phase 3: Kubernetes deployment
- Phase 4: Grafana Operator
- Phase 5: Gatling it down

## Project development log
- 260115_1039: As of right now I have advanced up to Phase 3 with Claude as my vibe coding tool by progressively describing the final result that I want and polishing the edges on the code that it spits:
1. So far I have had to adjust build commands for uv (`uv pip install` vs `uv add & sync`)
2. docker-compose vs docker compose (v1 vs v2 respectively)
3. The initial code did not even use the Dictionary class for the API...
4. I revised my plan and decided to use Mariadb as my db to save some ram although it probably won't be noticeable in the long run.
- 260115_1438: I was working on solidifying some thing around and making sure it was testable and notice and issue that I am going to table for later: new_entry and delete routes are case insensitive which is not intended behaviour... I will tackled this issue after I manage to add the Grafana Operator to this solution.
TODO: Fix case insensitivity of the post and delete methods of the database.

## Requirements & setup
1. Clone the repository
2. Install dependencies: `uv install`
3. Test with: `uv run pytest`

## Usage
```bash
# Example usage
uv run pytest
docker compose up
docker compose up --build
docker compose down
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