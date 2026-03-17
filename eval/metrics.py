import os
import json
import re
from dotenv import load_dotenv
from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
    HallucinationMetric,
    ToxicityMetric
)
from deepeval.models import DeepEvalBaseLLM
from google import genai

load_dotenv()

class GeminiEvalModel(DeepEvalBaseLLM):
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

    def load_model(self):
        return self.client

    def generate(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt + "\n\nIMPORTANT: Return only valid JSON. No markdown, no backticks, no explanation."
        )
        text = response.text.strip()
        # strip markdown code fences if present
        if text.startswith("```"):
            text = re.sub(r"```(?:json)?", "", text).replace("```", "").strip()
        return text

    async def a_generate(self, prompt: str) -> str:
        return self.generate(prompt)

    def get_model_name(self) -> str:
        return "gemini-2.0-flash"

gemini_eval_model = GeminiEvalModel()

def get_metrics():
    return {
        "answer_relevancy": AnswerRelevancyMetric(
            threshold=0.7,
            model=gemini_eval_model,
            include_reason=False
        ),
        "faithfulness": FaithfulnessMetric(
            threshold=0.7,
            model=gemini_eval_model,
            include_reason=False
        ),
        "hallucination": HallucinationMetric(
            threshold=0.2,
            model=gemini_eval_model,
            include_reason=False
        ),
        "toxicity": ToxicityMetric(
            threshold=0.1,
            model=gemini_eval_model,
            include_reason=False
        ),
    }
