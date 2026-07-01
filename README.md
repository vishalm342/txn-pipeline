# AI-Powered Transaction Processing Pipeline

Backend API for ingesting a dirty CSV of financial transactions, processing it asynchronously through a job queue, detecting anomalies, enriching uncategorised rows with an LLM, and exposing results through polling endpoints.

## Overview

This project implements a backend transaction-processing pipeline based on the assignment brief. The system accepts a CSV upload, creates a processing job, cleans and normalises the data, flags anomalies, generates a structured summary, and returns results via API endpoints [file:23].

## Features

- CSV upload and job creation
- Job status tracking
- Data cleaning and normalisation
- Duplicate removal
- Anomaly detection
- LLM-based category enrichment
- LLM-generated narrative summary
- PostgreSQL persistence
- Redis + Celery background processing
- Docker Compose setup for one-command startup [file:23]

## Tech Stack

- **FastAPI** — API framework [file:23]
- **PostgreSQL** — relational database [file:23]
- **Celery + Redis** — async job queue [file:23]
- **Pandas** — CSV cleaning and transformation
- **Gemini / OpenAI / Ollama** — LLM integration option [file:23]
- **Docker + Docker Compose** — local orchestration [file:23]

## Project Structure

```text
.
├── app
│   ├── api
│   ├── core
│   ├── db
│   ├── models
│   ├── schemas
│   ├── services
│   └── worker
├── data
├── cleaner.py
├── init_db.py
├── requirements.txt
└── README.md
```

## Processing Pipeline

When a job is processed, the pipeline performs these steps in order [file:23]:

1. Clean and normalise the CSV
2. Remove exact duplicates
3. Fill missing categories with `Uncategorised`
4. Detect anomalies:
   - amount greater than 3x account median
   - USD used with domestic-only merchants such as Swiggy, Ola, or IRCTC [file:23]
5. Classify uncategorised transactions using an LLM
6. Generate a final JSON narrative summary using an LLM [file:23]

## Current Progress

Implemented so far:

- Project structure
- FastAPI app bootstrap
- Config and DB session setup
- SQLAlchemy models:
  - `Job`
  - `Transaction`
  - `JobSummary`
- CSV cleaning logic
- Anomaly detection logic

## Data Cleaning Rules

The cleaning step currently handles the following rules from the brief [file:23]:

- Normalise mixed date formats to ISO 8601
- Strip currency symbols from amount fields
- Uppercase `currency` and `status`
- Fill blank `category` with `Uncategorised`
- Remove exact duplicate rows [file:23]

## Anomaly Detection Rules

The following anomaly rules are implemented from the assignment spec [file:23]:

- Flag transactions where amount exceeds 3x the account median
- Flag rows where currency is `USD` but merchant is a domestic-only brand such as Swiggy, Ola, or IRCTC [file:23]

## Setup

### 1. Clone the repository

```bash
git clone <YOUR_REPO_URL>
cd txn-pipeline
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create environment file

Create a `.env` file in the project root:

```env
APP_NAME=Alemeno Transaction Pipeline
APP_ENV=dev
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/alemeno_db
REDIS_URL=redis://localhost:6379/0
GEMINI_API_KEY=your_api_key_here
```

### 5. Start PostgreSQL locally

Example quick local Docker run:

```bash
docker run --name alemeno-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=alemeno_db \
  -p 5432:5432 \
  -d postgres:15
```

### 6. Create database tables

```bash
python init_db.py
```

### 7. Start the API server

```bash
uvicorn app.main:app --reload
```

API should now be available at:

- `http://127.0.0.1:8000`
- Swagger docs: `http://127.0.0.1:8000/docs`

## API Endpoints

The assignment requires these endpoints [file:23]:

- `POST /jobs/upload`
- `GET /jobs/{job_id}/status`
- `GET /jobs/{job_id}/results`
- `GET /jobs` [file:23]

## Example cURL Requests

### Health / Root

```bash
curl http://127.0.0.1:8000/
```

### Upload CSV

```bash
curl -X POST "http://127.0.0.1:8000/jobs/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@transactions.csv"
```

### Get Job Status

```bash
curl "http://127.0.0.1:8000/jobs/1/status"
```

### Get Job Results

```bash
curl "http://127.0.0.1:8000/jobs/1/results"
```

### List Jobs

```bash
curl "http://127.0.0.1:8000/jobs"
```

### Filter Jobs by Status

```bash
curl "http://127.0.0.1:8000/jobs?status=completed"
```

## Database Models

### Job

Tracks each uploaded CSV processing request [file:23].

Fields:
- `id`
- `filename`
- `status`
- `row_count_raw`
- `row_count_clean`
- `created_at`
- `completed_at`
- `error_message` [file:23]

### Transaction

Stores cleaned transaction rows linked to a job [file:23].

Fields include:
- `job_id`
- `txn_id`
- `date`
- `merchant`
- `amount`
- `currency`
- `status`
- `category`
- `account_id`
- `is_anomaly`
- `anomaly_reason`
- `llm_category`
- `llm_raw_response`
- `llm_failed` [file:23]

### JobSummary

Stores the final processed summary for one job [file:23].

Fields include:
- `job_id`
- `total_spend_inr`
- `total_spend_usd`
- `top_merchants`
- `anomaly_count`
- `narrative`
- `risk_level` [file:23]

## Notes

- This repository is being built incrementally from the assignment brief.
- Some API routes and async queue wiring may still be under implementation depending on the current commit.
- The intended final setup is a one-command `docker compose up` workflow as required in the assignment [file:23].

## Next Improvements

- Wire Celery worker to `POST /jobs/upload`
- Store cleaned rows into PostgreSQL
- Add status and results endpoints
- Add LLM category classification
- Add LLM narrative summary
- Add retry logic with exponential backoff
- Add full Docker Compose orchestration [file:23]