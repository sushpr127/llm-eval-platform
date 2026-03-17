import os
import uuid
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DB_URL = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)

engine = create_engine(DB_URL)

def log_eval_run(
    model_name, domain, question, answer, contexts,
    ground_truth, faithfulness, answer_relevancy,
    context_precision, hallucination_rate, toxicity,
    safety_score, latency_ms
):
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO eval_runs (
                run_id, model_name, domain, question, answer, contexts,
                ground_truth, faithfulness, answer_relevancy, context_precision,
                hallucination_rate, toxicity, safety_score, latency_ms
            ) VALUES (
                :run_id, :model_name, :domain, :question, :answer, :contexts,
                :ground_truth, :faithfulness, :answer_relevancy, :context_precision,
                :hallucination_rate, :toxicity, :safety_score, :latency_ms
            )
        """), {
            "run_id": str(uuid.uuid4()),
            "model_name": model_name,
            "domain": domain,
            "question": question,
            "answer": answer,
            "contexts": contexts,
            "ground_truth": ground_truth,
            "faithfulness": faithfulness,
            "answer_relevancy": answer_relevancy,
            "context_precision": context_precision,
            "hallucination_rate": hallucination_rate,
            "toxicity": toxicity,
            "safety_score": safety_score,
            "latency_ms": latency_ms
        })
        conn.commit()
