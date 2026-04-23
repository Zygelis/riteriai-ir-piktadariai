import json
import os
import matplotlib.pyplot as plt
import pandas as pd

# Load data
with open("evaluation_results/benchmark_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

models = data["models"]
benchmarks = data["benchmarks"]

# Output directory
output_dir = "evaluation_results/plots"
os.makedirs(output_dir, exist_ok=True)

# Color map per model (consistent across plots)
colors = {
    "Qwen3 4B": "#1f77b4",
    "Llama 3.2 3B": "#ff7f0e",
    "Gemma 3 4B": "#2ca02c",
    "Gemma 3n E4B": "#d62728",
    "Ministral 3 3B": "#9467bd",
}

# Convert to DataFrame
df = pd.DataFrame(benchmarks, index=models)

# Helper: add value labels
def add_labels(ax):
    for bar in ax.patches:
        height = bar.get_height()
        ax.annotate(
            f"{height}",
            (bar.get_x() + bar.get_width() / 2, height),
            ha="center",
            va="bottom",
            fontsize=9,
            xytext=(0, 3),
            textcoords="offset points",
        )

# 4 separate graphs (one per benchmark)
for benchmark in df.columns:
    plt.figure(figsize=(14, 10))
    ax = plt.bar(
        models,
        df[benchmark],
        color=[colors[m] for m in models],
    )
    plt.title(f"{benchmark} Results")
    plt.ylabel(benchmark)
    plt.xlabel("Model")
    plt.xticks(rotation=30, ha="right")
    add_labels(plt.gca())
    plt.tight_layout()
    filename = os.path.join(output_dir, f"{benchmark.replace(' ', '_').replace('/', '_')}.png")
    plt.savefig(filename, dpi=300)
    #plt.show()

# Combined graph
plt.figure(figsize=(14, 10))
df.plot(kind="bar", color=[colors[m] for m in models])
plt.title("All Benchmarks by Model")
plt.ylabel("Score")
plt.xlabel("Model")
plt.xticks(rotation=30, ha="right")
plt.legend(title="Benchmark", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "all_benchmarks.png"), dpi=300)
#plt.show()