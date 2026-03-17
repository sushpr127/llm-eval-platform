import os
import json
import uuid
import numpy as np
from scipy import stats
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DB_URL = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)
engine = create_engine(DB_URL)

MODELS = ["gemini-2.0-flash", "llama-3.1-8b-instant"]
DOMAINS = ["financial_analysis", "technical_documentation", "customer_support"]
METRICS = ["faithfulness", "answer_relevancy", "hallucination_rate", "toxicity"]
BOOTSTRAP_ITERATIONS = 1000
SIGNIFICANCE_THRESHOLD = 0.05

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, (np.bool_,)):
            return bool(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)

def fetch_scores(model_name: str, domain: str, metric: str) -> list[float]:
    with engine.connect() as conn:
        rows = conn.execute(text(f"""
            SELECT {metric} FROM eval_runs
            WHERE model_name = :model
            AND domain = :domain
            AND {metric} IS NOT NULL
        """), {"model": model_name, "domain": domain})
        return [row[0] for row in rows]

def bootstrap_confidence_interval(scores: list[float], n_iterations=BOOTSTRAP_ITERATIONS):
    if not scores:
        return None, None
    arr = np.array(scores)
    means = [
        np.mean(np.random.choice(arr, size=len(arr), replace=True))
        for _ in range(n_iterations)
    ]
    lower = round(float(np.percentile(means, 2.5)), 4)
    upper = round(float(np.percentile(means, 97.5)), 4)
    return lower, upper

def compare_models(scores_a: list[float], scores_b: list[float]) -> tuple[float, bool]:
    if len(scores_a) < 2 or len(scores_b) < 2:
        return 1.0, False
    _, p_value = stats.mannwhitneyu(scores_a, scores_b, alternative="two-sided")
    is_significant = bool(p_value < SIGNIFICANCE_THRESHOLD)
    return round(float(p_value), 4), is_significant

def determine_winner(mean_a, mean_b, metric, is_significant):
    if not is_significant:
        return "tie (not significant)"
    if metric in ["hallucination_rate", "toxicity"]:
        return MODELS[0] if mean_a < mean_b else MODELS[1]
    else:
        return MODELS[0] if mean_a > mean_b else MODELS[1]

def log_ab_result(test_id, domain, metric, mean_a, mean_b, winner, p_value):
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO ab_test_runs (
                test_id, model_a, model_b, domain, metric,
                model_a_score, model_b_score, winner, p_value
            ) VALUES (
                :test_id, :model_a, :model_b, :domain, :metric,
                :model_a_score, :model_b_score, :winner, :p_value
            )
        """), {
            "test_id": str(test_id),
            "model_a": MODELS[0],
            "model_b": MODELS[1],
            "domain": domain,
            "metric": metric,
            "model_a_score": float(mean_a),
            "model_b_score": float(mean_b),
            "winner": winner,
            "p_value": float(p_value)
        })
        conn.commit()

def run_ab_tests():
    test_id = uuid.uuid4()
    report = {
        "test_id": str(test_id),
        "model_a": MODELS[0],
        "model_b": MODELS[1],
        "results": {}
    }

    overall_wins = {MODELS[0]: 0, MODELS[1]: 0, "tie (not significant)": 0}

    for domain in DOMAINS:
        print(f"\n{'='*50}")
        print(f"Domain: {domain}")
        print(f"{'='*50}")
        report["results"][domain] = {}

        for metric in METRICS:
            scores_a = fetch_scores(MODELS[0], domain, metric)
            scores_b = fetch_scores(MODELS[1], domain, metric)

            if not scores_a or not scores_b:
                print(f"  {metric}: insufficient data — skipping")
                continue

            mean_a = round(float(np.mean(scores_a)), 4)
            mean_b = round(float(np.mean(scores_b)), 4)

            ci_a_low, ci_a_high = bootstrap_confidence_interval(scores_a)
            ci_b_low, ci_b_high = bootstrap_confidence_interval(scores_b)

            p_value, is_significant = compare_models(scores_a, scores_b)
            winner = determine_winner(mean_a, mean_b, metric, is_significant)

            overall_wins[winner] = overall_wins.get(winner, 0) + 1

            log_ab_result(test_id, domain, metric, mean_a, mean_b, winner, p_value)

            result = {
                MODELS[0]: {
                    "mean": mean_a,
                    "ci_95": [ci_a_low, ci_a_high]
                },
                MODELS[1]: {
                    "mean": mean_b,
                    "ci_95": [ci_b_low, ci_b_high]
                },
                "p_value": p_value,
                "significant": is_significant,
                "winner": winner
            }
            report["results"][domain][metric] = result

            sig_label = "SIGNIFICANT" if is_significant else "not significant"
            print(f"\n  {metric}:")
            print(f"    {MODELS[0]}: {mean_a} (95% CI: {ci_a_low}–{ci_a_high})")
            print(f"    {MODELS[1]}: {mean_b} (95% CI: {ci_b_low}–{ci_b_high})")
            print(f"    p-value: {p_value} ({sig_label})")
            print(f"    Winner: {winner}")

    print(f"\n{'='*50}")
    print("OVERALL WINS")
    print(f"{'='*50}")
    for model, wins in overall_wins.items():
        print(f"  {model}: {wins} wins")

    report["overall_wins"] = {k: int(v) for k, v in overall_wins.items()}

    output_path = "data/datasets/ab_test_report.json"
    with open(output_path, "w") as f:
        json.dump(report, f, indent=2, cls=NumpyEncoder)
    print(f"\nFull report saved to {output_path}")

    return report

if __name__ == "__main__":
    run_ab_tests()
