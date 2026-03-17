import os
from decimal import Decimal
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="LLM Eval Platform API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_URL = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)
engine = create_engine(DB_URL)

def to_float(val):
    if val is None:
        return None
    return float(Decimal(str(val)))

@app.get("/api/leaderboard")
def get_leaderboard():
    with engine.connect() as conn:
        rows = conn.execute(text("""
            SELECT model_name, total_evals, avg_faithfulness,
                   avg_answer_relevancy, avg_hallucination_rate,
                   avg_toxicity, avg_latency_ms, composite_score
            FROM analytics.model_leaderboard
        """))
        return [
            {
                "model_name": r.model_name,
                "total_evals": r.total_evals,
                "avg_faithfulness": to_float(r.avg_faithfulness),
                "avg_answer_relevancy": to_float(r.avg_answer_relevancy),
                "avg_hallucination_rate": to_float(r.avg_hallucination_rate),
                "avg_toxicity": to_float(r.avg_toxicity),
                "avg_latency_ms": to_float(r.avg_latency_ms),
                "composite_score": to_float(r.composite_score),
            }
            for r in rows
        ]

@app.get("/api/domain-breakdown")
def get_domain_breakdown():
    with engine.connect() as conn:
        rows = conn.execute(text("""
            SELECT model_name, domain, total_evals,
                   avg_faithfulness, avg_answer_relevancy,
                   avg_hallucination_rate, avg_latency_ms
            FROM analytics.domain_breakdown
        """))
        return [
            {
                "model_name": r.model_name,
                "domain": r.domain,
                "total_evals": r.total_evals,
                "avg_faithfulness": to_float(r.avg_faithfulness),
                "avg_answer_relevancy": to_float(r.avg_answer_relevancy),
                "avg_hallucination_rate": to_float(r.avg_hallucination_rate),
                "avg_latency_ms": to_float(r.avg_latency_ms),
            }
            for r in rows
        ]

@app.get("/api/red-team")
def get_red_team():
    with engine.connect() as conn:
        rows = conn.execute(text("""
            SELECT model_name, attack_type, total_attacks,
                   successful_attacks, attack_success_rate, avg_safety_score
            FROM analytics.red_team_summary
        """))
        return [
            {
                "model_name": r.model_name,
                "attack_type": r.attack_type,
                "total_attacks": r.total_attacks,
                "successful_attacks": r.successful_attacks,
                "attack_success_rate": to_float(r.attack_success_rate),
                "avg_safety_score": to_float(r.avg_safety_score),
            }
            for r in rows
        ]

@app.get("/api/stats")
def get_stats():
    with engine.connect() as conn:
        total_evals = conn.execute(text("SELECT COUNT(*) FROM eval_runs")).scalar()
        total_attacks = conn.execute(text("SELECT COUNT(*) FROM red_team_runs")).scalar()
        attacks_succeeded = conn.execute(
            text("SELECT COUNT(*) FROM red_team_runs WHERE attack_succeeded = true")
        ).scalar()
        models = conn.execute(
            text("SELECT COUNT(DISTINCT model_name) FROM eval_runs")
        ).scalar()
        return {
            "total_evals": total_evals,
            "total_attacks": total_attacks,
            "attacks_succeeded": attacks_succeeded,
            "models_evaluated": models,
            "overall_attack_resistance": round(1 - (attacks_succeeded / total_attacks), 4) if total_attacks else 0,
        }

@app.get("/api/ab-results")
def get_ab_results():
    with engine.connect() as conn:
        rows = conn.execute(text("""
            SELECT model_a, model_b, domain, metric,
                   model_a_score, model_b_score, winner, p_value
            FROM ab_test_runs
            ORDER BY created_at DESC
        """))
        return [
            {
                "model_a": r.model_a,
                "model_b": r.model_b,
                "domain": r.domain,
                "metric": r.metric,
                "model_a_score": to_float(r.model_a_score),
                "model_b_score": to_float(r.model_b_score),
                "winner": r.winner,
                "p_value": to_float(r.p_value),
            }
            for r in rows
        ]

@app.get("/health")
def health():
    return {"status": "ok"}
