"""Generate aggregate survey data and slide-ready SVG charts.

Usage: uv run --with matplotlib scripts/generate_survey_charts.py survey.csv
"""

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


QUESTIONS = {
    "c": "How confident are you contributing to CPython in C?",
    "rust": "How confident would you be contributing to CPython in Rust, assuming a PyO3-like Rust API?",
    "interest": "I am interested in contributing to CPython in Rust.",
}
RATINGS = [1, 2, 3, 4, 5]
INK = "#6b5b50"
ACCENT = "#995936"


def aggregate(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = set(QUESTIONS.values()) - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing survey questions: {sorted(missing)}")
        rows = [row for row in reader if any(row.values())]

    results = {}
    for key, question in QUESTIONS.items():
        values = [row[question].strip() for row in rows if row[question].strip()]
        if any(value not in {str(rating) for rating in RATINGS} for value in values):
            raise ValueError(f"Unexpected rating in question: {question}")
        counts = Counter(map(int, values))
        total = len(values)
        if not total:
            raise ValueError(f"No answers for question: {question}")
        upper = counts[4] + counts[5]
        results[key] = {
            "question": question,
            "response_count": total,
            "missing_count": len(rows) - total,
            "counts": [counts[rating] for rating in RATINGS],
            "rated_4_or_5": upper,
            "rated_4_or_5_percent": round(100 * upper / total, 1),
        }
    return {
        "source": path.name,
        "population": "CPython core team members who responded",
        "respondent_count": len(rows),
        "rating_values": RATINGS,
        "verbal_scale_anchors": None,
        "questions": results,
    }


def chart(result, path, title, color, xlabel, *, wide=False):
    fig, ax = plt.subplots(figsize=(7.2, 3.45) if wide else (5.1, 3.1))
    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)
    fig.subplots_adjust(left=0.13, right=0.98, bottom=0.22, top=0.85 if title else 0.96)
    bars = ax.bar(RATINGS, result["counts"], color=color, width=0.64, zorder=3)
    ax.bar_label(bars, padding=5, fontsize=17, color=INK)
    ax.set_xticks(RATINGS)
    # The confidence charts share the same scale; interest uses it too.
    ax.set_ylim(0, 16.5)
    ax.set_yticks([0, 5, 10, 15])
    ax.set_xlim(0.4, 5.6)
    ax.set_xlabel(xlabel, fontsize=14, labelpad=9, color=INK)
    ax.set_ylabel("Responses", fontsize=14, labelpad=9, color=INK)
    ax.tick_params(axis="both", labelsize=15, colors=INK, length=0, pad=6)
    ax.yaxis.grid(True, color="#e9d9c8", linewidth=0.8, zorder=0)
    for side in ["top", "right", "left"]:
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color("#cdb39d")
    if title:
        ax.set_title(title, fontsize=20, color=ACCENT, pad=14, fontweight="medium")
    fig.savefig(path, transparent=True, metadata={
        "Date": None,
        "Title": result["question"],
        "Description": f"n={result['response_count']}; counts for ratings 1–5: {result['counts']}",
    })
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path)
    parser.add_argument("--output-root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    data = aggregate(args.csv)
    images = args.output_root / "public/images"
    data_dir = args.output_root / "data"
    images.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)
    (data_dir / "core-team-survey-2026.json").write_text(json.dumps(data, indent=2) + "\n")
    plt.rcParams.update({"font.family": "Lato", "svg.fonttype": "path", "svg.hashsalt": "cpython-core-survey-2026"})
    for key, title, color in [("c", "C", "#d78f58"), ("rust", "Rust · PyO3-like API", "#b76a43")]:
        chart(data["questions"][key], images / f"core-team-confidence-{key}.svg", title, color, "Confidence rating")
    chart(data["questions"]["interest"], images / "core-team-rust-interest.svg", None, "#c5794b", "Interest rating", wide=True)
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
