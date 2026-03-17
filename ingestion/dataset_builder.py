import os
import json
import uuid
import time
from tqdm import tqdm
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
MODEL = "gemini-2.0-flash"

DOMAINS = {
    "financial_analysis": {
        "description": "Questions about financial concepts, ratios, accounting, investing, and market analysis",
        "examples": ["What is EBITDA?", "How do you calculate P/E ratio?", "What is dollar cost averaging?"]
    },
    "technical_documentation": {
        "description": "Questions about software engineering, APIs, databases, cloud infrastructure, and dev tools",
        "examples": ["What is a REST API?", "How does indexing work in PostgreSQL?", "What is a Docker container?"]
    },
    "customer_support": {
        "description": "Questions a customer might ask about a SaaS product — billing, account issues, features, troubleshooting",
        "examples": ["How do I reset my password?", "Can I export my data?", "Why was I charged twice?"]
    }
}

QUESTIONS_PER_DOMAIN = 70

def generate_questions(domain_name, domain_info, n):
    prompt = f"""Generate {n} realistic, diverse questions for the domain: {domain_info['description']}

Examples of the style: {', '.join(domain_info['examples'])}

Rules:
- Each question must be distinct — no repeats or near-duplicates
- Vary difficulty: mix simple, intermediate, and complex questions
- Make them sound like real users asking, not textbook questions
- Return ONLY a JSON array of strings, no markdown, no explanation

Example format:
["Question 1?", "Question 2?", "Question 3?"]"""

    response = client.models.generate_content(model=MODEL, contents=prompt)
    text = response.text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text.strip())

def generate_answer_and_context(question, domain_name):
    prompt = f"""You are an expert in {domain_name.replace('_', ' ')}.

Question: {question}

Provide:
1. A thorough, accurate answer (3-5 sentences)
2. A supporting context passage (2-3 sentences of background knowledge that supports the answer)

Return ONLY valid JSON in this exact format, no markdown:
{{
  "answer": "your answer here",
  "context": "supporting context here"
}}"""

    response = client.models.generate_content(model=MODEL, contents=prompt)
    text = response.text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text.strip())

def build_dataset():
    os.makedirs("data/datasets", exist_ok=True)
    all_samples = []

    for domain_name, domain_info in DOMAINS.items():
        print(f"\nGenerating questions for: {domain_name}")
        questions = generate_questions(domain_name, domain_info, QUESTIONS_PER_DOMAIN)
        print(f"Got {len(questions)} questions — now generating answers...")

        for question in tqdm(questions):
            try:
                qa = generate_answer_and_context(question, domain_name)
                sample = {
                    "id": str(uuid.uuid4()),
                    "domain": domain_name,
                    "question": question,
                    "ground_truth": qa["answer"],
                    "context": qa["context"]
                }
                all_samples.append(sample)
                time.sleep(0.5)
            except Exception as e:
                print(f"  Skipping question due to error: {e}")
                continue

    output_path = "data/datasets/eval_dataset.jsonl"
    with open(output_path, "w") as f:
        for sample in all_samples:
            f.write(json.dumps(sample) + "\n")

    print(f"\nDataset saved: {output_path}")
    print(f"Total samples: {len(all_samples)}")

    summary = {}
    for domain in DOMAINS:
        summary[domain] = sum(1 for s in all_samples if s["domain"] == domain)
    summary["total"] = len(all_samples)

    with open("data/datasets/dataset_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print(f"Summary: {summary}")

if __name__ == "__main__":
    build_dataset()
