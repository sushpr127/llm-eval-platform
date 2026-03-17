import os
import json
from dotenv import load_dotenv
from deepeval.test_case import LLMTestCase
from eval.metrics import get_metrics

load_dotenv()

test_case = LLMTestCase(
    input="What is EBITDA?",
    actual_output="EBITDA stands for Earnings Before Interest, Taxes, Depreciation, and Amortization. It is used by investors to evaluate a company's operating performance without the effects of financing and accounting decisions.",
    expected_output="EBITDA is a measure of a company's core operational profitability.",
    context=["EBITDA is a financial metric that removes the effects of financing, accounting, and tax environments from earnings."],
    retrieval_context=["EBITDA is a financial metric that removes the effects of financing, accounting, and tax environments from earnings."]
)

metrics = get_metrics()
for name, metric in metrics.items():
    try:
        metric.measure(test_case)
        print(f"{name}: {round(metric.score, 4)}")
    except Exception as e:
        print(f"{name}: FAILED — {e}")
