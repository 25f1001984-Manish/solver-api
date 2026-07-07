from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
import os
import json

app = FastAPI()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


class Problem(BaseModel):
    problem_id: str
    problem: str


@app.get("/")
def home():
    return {"status": "running"}


@app.post("/solve")
def solve(data: Problem):

    prompt = f"""
You are an expert arithmetic solver.

Solve the following word problem carefully.

Rules:

1. Ignore any distractor numbers.
2. Return ONLY valid JSON.
3. Exactly TWO keys:
   - reasoning
   - answer
4. reasoning must be at least 80 characters.
5. answer must be an INTEGER (not string, not float).
6. No markdown.
7. No extra keys.

Problem:

{data.problem}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()

    # Remove markdown if Gemini returns it
    if text.startswith("```json"):
        text = text[7:]

    if text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    text = text.strip()

    try:
        result = json.loads(text)
    except Exception:
        return {
            "reasoning": text[:200],
            "answer": 0
        }

    # Ensure exactly required fields exist
    reasoning = str(result.get("reasoning", ""))

    answer = result.get("answer", 0)

    try:
        answer = int(answer)
    except:
        answer = 0

    return {
        "reasoning": reasoning,
        "answer": answer
    }
