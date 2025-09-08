import json
import numpy as np
import random
import re
import ast

with open("data/annotations.json", "r") as f:
    annotations = json.load(f)

if isinstance(annotations, dict) and "prompts" in annotations:
    prompts = annotations["prompts"]

elif isinstance(annotations, dict) and "cells" in annotations:
    cell_sources = []
    for c in annotations.get("cells", []):
        src = c.get("source", [])
        if isinstance(src, list):
            src = "".join(src)
        cell_sources.append(src)
    nb_source = "\n".join(cell_sources)

    # Extract the list literal inside prompts = [...]
    m = re.search(r"prompts\s*=\s*(\[.*?\])", nb_source, re.S)
    if not m:
        raise KeyError("Could not find a 'prompts = [...]' list in notebook JSON.")
    prompts = ast.literal_eval(m.group(1))

else:
    raise KeyError(
        "annotations.json must be either a plain JSON with 'prompts', "
        "or a notebook-style JSON containing a 'prompts = [...]' block."
    )

model_outputs = {
    "ChatGPT": [f"ChatGPT response to: {p}" for p in prompts],
    "Gemini": [f"Gemini response to: {p}" for p in prompts],
    "DeepSeek": [f"DeepSeek response to: {p}" for p in prompts]
}

def collect_annotations(outputs):
    return [random.randint(-2, 2) for _ in outputs]  # bias scale: -2 to +2

def compute_bias_scores():
    scores = {}
    for model, outputs in model_outputs.items():
        ratings = collect_annotations(outputs)
        scores[model] = np.mean(ratings)
    return scores

if __name__ == "__main__":
    print("Running EASL Core Simulation...\n")
    bias_scores = compute_bias_scores()
    for model, score in bias_scores.items():
        print(f"{model} average bias score: {score:.2f}")

