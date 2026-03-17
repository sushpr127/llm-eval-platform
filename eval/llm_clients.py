import os
import time
from dotenv import load_dotenv
from google import genai
from groq import Groq

load_dotenv()

gemini_client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODELS = {
    "gemini-2.0-flash": "gemini",
    "llama-3.1-8b-instant": "groq"
}

def call_gemini(question: str, context: str) -> tuple[str, int]:
    prompt = f"""Use the following context to answer the question accurately.

Context: {context}

Question: {question}

Answer:"""
    start = time.time()
    response = gemini_client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    latency_ms = int((time.time() - start) * 1000)
    return response.text.strip(), latency_ms

def call_groq(question: str, context: str) -> tuple[str, int]:
    prompt = f"""Use the following context to answer the question accurately.

Context: {context}

Question: {question}

Answer:"""
    start = time.time()
    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    latency_ms = int((time.time() - start) * 1000)
    return response.choices[0].message.content.strip(), latency_ms

def call_model(model_name: str, question: str, context: str) -> tuple[str, int]:
    if model_name == "gemini-2.0-flash":
        return call_gemini(question, context)
    elif model_name == "llama-3.1-8b-instant":
        return call_groq(question, context)
    else:
        raise ValueError(f"Unknown model: {model_name}")
