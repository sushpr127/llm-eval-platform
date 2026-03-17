import os
import json
import sys
from decimal import Decimal
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DB_URL = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)
engine = create_engine(DB_URL)

MIN_FAITHFULNESS = float(os.getenv("MIN_FAITHFULNESS", 0.7))
MAX_HALLUCINATION = float(os.getenv("MAX_HALLUCINATION_RATE", 0.2))

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

def get_latest_scores():
    with engine.connect() as conn:
        rows = conn.execute(text("""
            SELECT
                model_name,
                round(avg(faithfulness)::numeric, 4)       as avg_faithfulness,
                round(avg(hallucination_rate)::numeric, 4) as avg_hallucination
            FROM eval_runs
            WHERE created_at >= NOW() - INTERVAL '24 hours'
            AND faithfulness IS NOT NULL
            GROUP BY model_name
        """))
        return [dict(row._mapping) for row in rows]

def run_ci_check():
    print("Running CI eval gate check...")
    scores = get_latest_scores()

    if not scores:
        print("No eval runs found in last 24 hours — skipping gate")
        sys.exit(0)

    failed = False
    results = []

    for row in scores:
        model = row["model_name"]
        faith = float(row["avg_faithfulness"])
        halluc = float(row["avg_hallucination"])

        faith_pass = faith >= MIN_FAITHFULNESS
        halluc_pass = halluc <= MAX_HALLUCINATION

        status = "PASS" if (faith_pass and halluc_pass) else "FAIL"
        if status == "FAIL":
            failed = True

        results.append({
            "model": model,
            "faithfulness": faith,
            "hallucination_rate": halluc,
            "faithfulness_check": "PASS" if faith_pass else f"FAIL (min {MIN_FAITHFULNESS})",
            "hallucination_check": "PASS" if halluc_pass else f"FAIL (max {MAX_HALLUCINATION})",
            "overall": status
        })

        print(f"\n{model}:")
        print(f"  Faithfulness:    {faith} → {'✅' if faith_pass else '❌'}")
        print(f"  Hallucination:   {halluc} → {'✅' if halluc_pass else '❌'}")
        print(f"  Status:          {status}")

    with open("data/datasets/ci_results.json", "w") as f:
        json.dump(results, f, indent=2, cls=DecimalEncoder)

    if failed:
        print("\n❌ CI GATE FAILED — one or more models below threshold")
        sys.exit(1)
    else:
        print("\n✅ CI GATE PASSED — all models within thresholds")
        sys.exit(0)

if __name__ == "__main__":
    run_ci_check()
