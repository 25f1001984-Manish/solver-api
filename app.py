from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()


class Problem(BaseModel):
    problem_id: str
    problem: str


@app.post("/solve")
def solve(data: Problem):

    prompt = f"""
You are an expert math solver.

Solve the following arithmetic word problem.

Rules:

- Ignore irrelevant numbers.
- Return ONLY JSON.
- Exactly two keys:
    reasoning
    answer
- reasoning must be at least 80 characters.
- answer must be an integer (not string).

Problem:

{data.problem}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    import json

    return json.loads(response.output_text)
