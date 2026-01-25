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
- 260116_1334: I finally managed to get the Kubernetes deployment working... it truly game me the go around:
1. The first and mayor problem I had was context: I have Docker Desktop and Rancher Desktop on my pc and both have their own managed docker and docker compose binaries which conflicted in either permissions or visible namespaces everytime I tried to deploy k8s... as such I had to investigate a bit how to actually change the context and environment for these binaries without breaking them as I want to keep them. This issue with all of this? Kubernetes needed to build and make visible/add to namespace the images of the containers that I was using and that was simply impossible without fixing this issue.
2. The second issue? uv is awesome but adds a complexity layer to dockerfile authoring. Doubly so as most LLM documentation for dockerfiles is for raw python and pip which means that I had to dig a bit to solve any issue. Gemini was actually a better information font in this step than Github Copilot so that is something to keep in mind.
3. There is an issue that cropped up once I got a working deployment and its that for some reason there is a lag between the api and database and i think it is because multiple replicas flood the database and it locks temporarily but I would need to dig into it...
~~TODO~~: Investigate this issue: Replace MariaDB for its operator and then see if that solves the issue.
260121_1908: I managed to get the operator working and it did not resolve the underlying issue: configuration. It turns out that Kubernetes health checks overwhelmed both the api and the database (more the first than the second actually) and as such I need to work more on strenghtening my bases to actually understand what makes a good Kubernetes config in a live environment. Another point that comes from relying on AI to get a basic setup working is the fact that the underlaying environmental vairables? out of sync as the AI forgets that it set something in one part of the other and since I did not stablish a firm convention then it created its own at every step confusing things like databse credentials and connection strings... something to keep in mind for future work.
260124_2359: I need to polish the base API as it seems to be the main hangup here:
- Discard the dictionary intermediary.
- Replace SQLAlchemy calls for SQLModel which is more inline with FastAPI principles.

## Lessons and reflection
There are many things that I can reflect while  going through this experience:
1. Debugging Kubernetes is complex but the first place to look is always the logs of the component you suspect is the issue and go upwards in hierarchy.
2. Configuration drift is easy as many manifesto.yml resources work with their own individual variables that sometimes need to match to pass a configuration from one component to another... I will need to experiment more with helm as it seems to be the current solution to this problem.
3. Just for the record a minor thing: is more or less convention to store the manifesto files of the kubernetes configuration files in a directory like `k8s/` so that its easier to reference for `kubectl apply`.
4. `kubectl apply` command has too ways to be used:
   1. With the flag `-f k8s/` which applies the configuration files to the cluster in an alphabetical way which sometimes causes conflicts.
   2. With the flag `-k k8s/` instead is something called **Kustomize** which prompts the system to look for a file called *kustomization.yaml* which allows us to customize how Kubernetes provision resources and in what order to facilitate proper configuration for resources that require prerequisites to exist before they spin themselves.
5. Kubernetes is a tool that facilitates operations and system stability at the cost of increasing the complexity of the system and adding a few network and distributed system considerations that may or may not be necessary depending on your requirements. Nevertheless, the advantages when properly used heavily outweigh the complexity and makes management simpler once properly setup and observed.
6. One of those considerations that we need to take in to account is the simple fact that Kubernetes itself is part of the equation and it will hit all containers and pods constantly as part of its evaluation of health and liveliness of the system and that is something to keep in mind; especially so, for python applications that are single threaded and can be overwhelmed by it causing it to hang.

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