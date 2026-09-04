Core capabilities

Playwright analysis



Analyzes Playwright JSON reports and extracts:



total tests

passed tests

failed tests

flaky tests

failure details

GitHub defect intelligence



Fetches historical GitHub issues and exposes defect information through MCP.



RAG-based similar defect search



Historical defect data is indexed in ChromaDB.



A new failure can be compared semantically against previous defects to find potentially related incidents.



AI-assisted failure triage



Combines:



Test failure

&#x20;   ↓

GitHub defects

&#x20;   ↓

Historical defect embeddings

&#x20;   ↓

Similarity search

&#x20;   ↓

Triage result



This provides contextual information instead of relying only on the current stack trace.



Distributed regression reporting



Kubernetes Jobs can execute regression workers in parallel and produce execution reports that can be aggregated into a unified report.



Executive QA summary



The reporting layer calculates:



total execution count

pass/fail count

flaky count

pass rate

failed test names



and generates an executive-level summary.



MCP tools

Tool	Purpose

health\_check	Server health check

playwright\_test\_summary	Analyze Playwright JSON results

github\_defect\_fetcher	Fetch GitHub defects

ingest\_historical\_defects	Load historical defects into ChromaDB

similar\_defect\_search	Find semantically similar defects

triage\_test\_failure	Combine defects + RAG for failure triage

regression\_execution\_summary	Generate regression execution summary

Technology stack

Layer	Technology

UI Automation	Playwright + TypeScript

AI Tool Interface	Model Context Protocol

MCP Server	Python + FastMCP

Vector Store	ChromaDB

Defect Source	GitHub Issues

Testing	Pytest

CI/CD	GitHub Actions

Containerization	Docker

Registry	Docker Hub

Orchestration	Kubernetes

Cloud	AWS EKS

Runtime	Python 3.13

CI/CD flow

Developer

&#x20;  ↓

GitHub Push

&#x20;  ↓

GitHub Actions

&#x20;  ├── Python tests

&#x20;  └── Playwright tests

&#x20;         ↓

&#x20;     Docker Build

&#x20;         ↓

&#x20;     Docker Hub



The Docker publishing workflow creates:



lethalfore/qa-intelligence-mcp:latest

lethalfore/qa-intelligence-mcp:<commit-sha>

AWS deployment



The MCP server is deployed to:



AWS

└── EKS

&#x20;   └── qa-intelligence-mcp Deployment

&#x20;       └── qa-intelligence-service

&#x20;           └── MCP server :8000



The Kubernetes Service currently uses:



Type: ClusterIP

Port: 8000



The service is intentionally internal to the cluster rather than publicly exposed.



The deployed container listens on:



0.0.0.0:8000

Kubernetes

Deployment



The MCP server runs as a Kubernetes Deployment.



Deployment

&#x20;   ↓

Pod

&#x20;   ↓

FastMCP / Uvicorn

Parallel regression jobs



The repository also contains a Kubernetes Job configuration with:



completions: 4

parallelism: 4



This demonstrates the orchestration model for parallel regression workers.



Current limitation: the Kubernetes regression Job is a lightweight execution simulation rather than the final production Playwright worker implementation. The architecture is designed to support real containerized Playwright workers.



Reporting architecture



The reporting pipeline is:



Regression Reports

&#x20;     ↓

Report Aggregator

&#x20;     ↓

merged-report.json

&#x20;     ↓

Regression Summary MCP Tool

&#x20;     ↓

Executive QA Summary



Example metrics:



Total:      50

Passed:     47

Failed:      3

Pass Rate: 94%

Local development

Python environment

python -m venv .venv



Windows:



.venv\\Scripts\\activate



Install dependencies:



pip install -r requirements.txt



Run tests:



pytest -q

Playwright

cd playwright-demo

npm ci

npx playwright install

npx playwright test

MCP server



From the repository root:



python server.py



The MCP server runs using Streamable HTTP on:



http://127.0.0.1:8000

Docker



Build:



docker build -t qa-intelligence-mcp:latest .



For the EKS x86\_64 worker architecture:



docker buildx build \\

&#x20; --platform linux/amd64 \\

&#x20; -t lethalfore/qa-intelligence-mcp:1.1.0 \\

&#x20; --push .

Kubernetes deployment

kubectl apply -f k8s/deployment.yaml



Verify:



kubectl get pods

kubectl get svc



View logs:



kubectl logs deployment/qa-intelligence-mcp



Expected:



Uvicorn running on http://0.0.0.0:8000

Design decisions

Why MCP?



MCP provides a standard tool interface between an AI client and QA capabilities such as:



test analysis

defect retrieval

semantic search

triage

reporting



This keeps QA capabilities as explicit tools instead of embedding every workflow inside one large AI prompt.



Why RAG?



Current failures need historical context.



RAG allows the platform to retrieve relevant previous defects before producing a triage result.



Why ChromaDB?



The project needs a lightweight local vector store for semantic retrieval without introducing a large infrastructure dependency.



Why Kubernetes?



Kubernetes provides:



container orchestration

declarative deployment

service discovery

workload parallelism

horizontal scaling options

Why EKS?



EKS demonstrates that the same containerized workload can move from local Kubernetes to a managed cloud Kubernetes environment.



Current limitations



This project intentionally focuses on architecture and core engineering patterns rather than claiming production completeness.



Current limitations include:



Kubernetes regression workers are currently simulated.

Report aggregation is implemented but not yet fully wired into a persistent distributed artifact store.

Executive summary generation currently consumes the merged report rather than being triggered automatically by every EKS regression execution.

The EKS service is internal (ClusterIP) and is not exposed as a public endpoint.

AI output should be treated as engineering assistance and validated against deterministic test and defect data.

Engineering principles



The platform follows a hybrid approach:



Deterministic automation

&#x20;       +

AI-assisted analysis

&#x20;       +

Historical context

&#x20;       =

Higher-quality engineering feedback



AI is applied where it adds value, especially in investigation, classification, and contextual analysis.



Deterministic test execution remains the source of truth.



Repository structure

qa-intelligence-mcp/

│

├── .github/

│   └── workflows/

│       ├── ci.yml

│       └── docker-publish.yml

│

├── aggregator/

│   └── merge\_reports.py

│

├── k8s/

│   ├── deployment.yaml

│   └── job.yaml

│

├── playwright-demo/

│   ├── tests/

│   ├── package.json

│   └── playwright.config.ts

│

├── sample-data/

│

├── src/

│   └── qa\_mcp\_server/

│       └── tools/

│           ├── github.py

│           ├── playwright.py

│           ├── rag.py

│           ├── report\_analyzer.py

│           └── triage.py

│

├── tests/

│

├── Dockerfile

├── requirements.txt

├── pytest.ini

├── server.py

└── README.md

Portfolio highlights



This project demonstrates practical experience across:



QA automation engineering

Playwright

Python

MCP

RAG

vector search

AI-assisted failure triage

GitHub integration

distributed test execution concepts

Docker

Kubernetes

GitHub Actions

Docker Hub

AWS EKS

cloud-native test platform architecture



Save and close.



\### 2. Create architecture document



Run:



```cmd

mkdir docs

notepad docs\\architecture.md



Paste:



\# QA Intelligence Architecture



\## 1. System overview



QA Intelligence is designed as a layered test engineering platform.



```text

&#x20;                   ┌─────────────────────┐

&#x20;                   │       GitHub        │

&#x20;                   │ Source + Defects    │

&#x20;                   └──────────┬──────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌─────────────────────┐

&#x20;                   │   GitHub Actions    │

&#x20;                   │ CI + Docker Publish  │

&#x20;                   └──────────┬──────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌─────────────────────┐

&#x20;                   │     Docker Hub      │

&#x20;                   │ Container Registry  │

&#x20;                   └──────────┬──────────┘

&#x20;                              │

&#x20;                              ▼

&#x20;                   ┌─────────────────────┐

&#x20;                   │      AWS EKS        │

&#x20;                   │ Kubernetes Runtime  │

&#x20;                   └──────────┬──────────┘

&#x20;                              │

&#x20;                    ┌─────────┴─────────┐

&#x20;                    ▼                   ▼

&#x20;             ┌──────────────┐   ┌──────────────┐

&#x20;             │ MCP Service  │   │ Regression   │

&#x20;             │   :8000      │   │    Jobs      │

&#x20;             └──────┬───────┘   └──────┬───────┘

&#x20;                    │                  │

&#x20;                    ▼                  ▼

&#x20;             ┌──────────────┐   ┌──────────────┐

&#x20;             │ MCP Tools    │   │ Test Reports │

&#x20;             └──────┬───────┘   └──────┬───────┘

&#x20;                    │                  │

&#x20;         ┌──────────┼──────────┐       ▼

&#x20;         ▼          ▼          ▼   ┌──────────────┐

&#x20;     GitHub      ChromaDB    Test   │ Aggregator  │

&#x20;     Defects       RAG      Reports └──────┬───────┘

&#x20;         │          │                     │

&#x20;         └────┬─────┘                     ▼

&#x20;              ▼                    ┌──────────────┐

&#x20;       Failure Triage              │ QA Summary   │

&#x20;                                   └──────────────┘

2\. MCP layer



The MCP server exposes QA capabilities as discrete tools.



FastMCP

&#x20;├── health\_check

&#x20;├── playwright\_test\_summary

&#x20;├── github\_defect\_fetcher

&#x20;├── ingest\_historical\_defects

&#x20;├── similar\_defect\_search

&#x20;├── triage\_test\_failure

&#x20;└── regression\_execution\_summary



This provides a clean interface between AI clients and QA engineering capabilities.



3\. Failure triage flow

Failure

&#x20;  │

&#x20;  ▼

triage\_test\_failure

&#x20;  │

&#x20;  ├──────────────► GitHub defect retrieval

&#x20;  │

&#x20;  └──────────────► ChromaDB semantic search

&#x20;                          │

&#x20;                          ▼

&#x20;                   Similar historical

&#x20;                        defects

&#x20;                          │

&#x20;                          ▼

&#x20;                      Triage result



The important design principle is that the AI-assisted workflow receives retrieved engineering context instead of relying only on a raw failure message.



4\. Reporting flow

Parallel execution

&#x20;      │

&#x20;      ▼

Individual reports

&#x20;      │

&#x20;      ▼

merge\_reports.py

&#x20;      │

&#x20;      ▼

merged-report.json

&#x20;      │

&#x20;      ▼

regression\_execution\_summary

&#x20;      │

&#x20;      ▼

Executive QA summary

5\. Kubernetes responsibilities

Deployment



The Deployment manages the long-running MCP server.



Deployment

&#x20;  ↓

Pod

&#x20;  ↓

FastMCP

&#x20;  ↓

Uvicorn :8000

Service



The Service provides stable internal access:



qa-intelligence-service:8000



It currently uses ClusterIP, keeping the MCP server private to the cluster network.



Job



The regression Job models parallel test execution:



Job

&#x20;├── worker 1

&#x20;├── worker 2

&#x20;├── worker 3

&#x20;└── worker 4



The current Job implementation is a simulation of parallel workers and is intentionally separated from the long-running MCP Deployment.



6\. Deployment flow

git push

&#x20;  ↓

GitHub Actions

&#x20;  ├── Python tests

&#x20;  └── Playwright tests

&#x20;  ↓

Docker build

&#x20;  ↓

Docker Hub

&#x20;  ↓

EKS deployment

&#x20;  ↓

Kubernetes Pod

&#x20;  ↓

MCP server



The application image is built for linux/amd64 because the current EKS worker uses the x86\_64 architecture.



7\. Architecture trade-offs

MCP vs direct application endpoints



MCP was selected because the platform is designed around AI-accessible QA tools.



A REST API would still be useful for traditional service integrations, but MCP provides a tool-oriented interface suitable for AI clients.



ChromaDB vs managed vector database



ChromaDB keeps the project lightweight and easy to run locally.



A production implementation could use a managed or distributed vector database when scale, availability, and operational requirements increase.



Kubernetes Job vs Deployment



The MCP server is long-lived, so it uses a Deployment.



Regression execution is finite work, so Jobs are a better Kubernetes abstraction.



EKS vs local Kubernetes



Local Kubernetes is useful for development and validation.



EKS demonstrates operation in a managed cloud Kubernetes environment while keeping the application container portable.



8\. Reliability considerations



The architecture separates:



deterministic test execution

historical data retrieval

AI-assisted analysis

reporting



This is intentional.



A failure in the AI layer should not change whether a deterministic test actually passed or failed.



AI output is therefore an additional engineering signal rather than the primary source of truth.



9\. Future evolution



Potential production extensions include:



Persistent artifact storage

&#x20;       ↓

Real Playwright worker containers

&#x20;       ↓

Event-driven regression orchestration

&#x20;       ↓

Autoscaling

&#x20;       ↓

Observability

&#x20;       ↓

AI evaluation / tracing



These are architectural extensions rather than requirements for the current project.

