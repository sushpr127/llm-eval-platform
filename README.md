# LLM Evaluation & Observability Platform

A production eval framework that benchmarks, monitors, and red-teams LLM applications.

## Models Evaluated
- Gemini 2.0 Flash
- GPT-4o Mini
- Llama 3.1 8B (via Groq)

## Stack
Ragas · DeepEval · LangSmith · FastAPI · PostgreSQL · dbt · React · GitHub Actions

## Setup
```bash
cp .env.example .env
# Fill in your API keys in .env
docker-compose up postgres -d
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```
