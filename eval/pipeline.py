import os
import json
import time
from tqdm import tqdm
from dotenv import load_dotenv
from deepeval.test_case import LLMTestCase
from eval.llm_clients import call_model, MODELS
from eval.metrics import get_metrics
from eval.db_logger import log_eval_run

load_dotenv()

DATASET_PATH = "data/datasets/eval_dataset.jsonl"
MAX_SAMPLES_PER_DOMAIN = 20  # 20 x 3 domains x 2 models = 120 eval runs total

def load_dataset(max_per_domain=MAX_SAMPLES_PER_DOMAIN):
    samples = []
    domain_counts = {}
    with open(DATASET_PATH) as f:
        for line in f:
            sample = json.loads(line)
            domain = sample["domain"]
            if domain_counts.get(domain, 0) < max_per_domain:
                samples.append(sample)
                domain_counts[domain] = domain_counts.get(domain, 0) + 1
    print(f"Loaded {len(samples)} samples: {domain_counts}")
    return samples

def score_sample(answer, question, context, ground_truth):
    metrics = get_metrics()
    test_case = LLMTestCase(
        input=question,
        actual_output=answer,
        expected_output=ground_truth,
        context=[context],
        retrieval_context=[context]
    )

    scores = {}
    for metric_name, metric in metrics.items():
        try:
            metric.measure(test_case)
            scores[metric_name] = round(metric.score, 4)
        except Exception as e:
            print(f"    Metric {metric_name} failed: {e}")
            scores[metric_name] = None

    return scores

def run_pipeline():
    samples = load_dataset()
    results_summary = {}

    for model_name in MODELS.keys():
        print(f"\n{'='*50}")
        print(f"Evaluating model: {model_name}")
        print(f"{'='*50}")

        model_scores = {
            "faithfulness": [],
            "answer_relevancy": [],
            "hallucination": [],
            "toxicity": []
        }

        for sample in tqdm(samples):
            try:
                answer, latency_ms = call_model(
                    model_name,
                    sample["question"],
                    sample["context"]
                )

                scores = score_sample(
                    answer,
                    sample["question"],
                    sample["context"],
                    sample["ground_truth"]
                )

                log_eval_run(
                    model_name=model_name,
                    domain=sample["domain"],
                    question=sample["question"],
                    answer=answer,
                    contexts=[sample["context"]],
                    ground_truth=sample["ground_truth"],
                    faithfulness=scores.get("faithfulness"),
                    answer_relevancy=scores.get("answer_relevancy"),
                    context_precision=None,
                    hallucination_rate=scores.get("hallucination"),
                    toxicity=scores.get("toxicity"),
                    safety_score=None,
                    latency_ms=latency_ms
                )

                for k, v in scores.items():
                    if v is not None:
                        model_scores[k].append(v)

                time.sleep(0.5)

            except Exception as e:
                print(f"\n  Error on sample: {e}")
                continue

        avg = lambda lst: round(sum(lst)/len(lst), 4) if lst else None
        results_summary[model_name] = {
            "faithfulness":     avg(model_scores["faithfulness"]),
            "answer_relevancy": avg(model_scores["answer_relevancy"]),
            "hallucination":    avg(model_scores["hallucination"]),
            "toxicity":         avg(model_scores["toxicity"]),
            "samples_evaluated": len(samples)
        }

    print(f"\n{'='*50}")
    print("FINAL RESULTS")
    print(f"{'='*50}")
    for model, scores in results_summary.items():
        print(f"\n{model}:")
        for metric, score in scores.items():
            print(f"  {metric}: {score}")

    with open("data/datasets/eval_results.json", "w") as f:
        json.dump(results_summary, f, indent=2)
    print("\nResults saved to data/datasets/eval_results.json")

if __name__ == "__main__":
    run_pipeline()
