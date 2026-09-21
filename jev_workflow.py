# SPDX-License-Identifier: GPL-3.0-only
import argparse
import json
from pathlib import Path
from jev_client import Client, JevError, MODEL, choice, selected
import app

def request_data():
    return {"left": "Cancel my monthly subscription.", "right": "Please stop renewing my plan each month."}, choice(
        "Do these two training texts express the same intent and constraints? Review for leakage before any train/eval split.",
        {"duplicate": "Same intent and constraints, even with different wording", "distinct": "Materially different intent or constraints", "review": "Insufficient evidence"})

def run(client):
    state, questions = request_data()
    response = client.evaluate(state, questions)
    return {"semantic_review": selected(response, "review"),
            "lexical_similarity": app.similarity(state["left"], state["right"]),
            "usage": [response["usage"]], "mutates_split": False,
            "limitation": "Synthetic pair, advisory review only. No split edits or training. Human-confirmed duplicate groups must precede splitting."}

def main():
    parser = argparse.ArgumentParser(description="Preview the synthetic Jev request; --live explicitly opts into paid calls.")
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--env-file", type=Path)
    args = parser.parse_args()
    if not args.live:
        state, questions = request_data()
        print(json.dumps({"mode": "dry-run-no-network", "model": MODEL, "state": state, "questions": questions}, indent=2))
        return
    if args.env_file is None:
        parser.error("--live requires --env-file with the shared budget ledger")
    try:
        client = Client(args.env_file)
        result = run(client)
        print(json.dumps({"mode": "live-model-on-synthetic-data", "model": MODEL, **result, "budget": client.budget.summary()}, indent=2))
    except JevError as exc:
        parser.exit(1, str(exc) + "\n")

if __name__ == "__main__":
    main()
