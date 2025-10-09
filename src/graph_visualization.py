
import matplotlib.pyplot as plt

def show_bias_bar_chart(bias_scores: dict, y_range=(-2, 2)):
    """
    Show a bar chart of average bias scores by model.

    Parameters
    ----------
    bias_scores : dict
        Mapping like {"ChatGPT": 0.10, "Gemini": -0.25, "DeepSeek": -0.05}
    y_range : tuple
        y-axis limits, default (-2, 2) to match your annotation scale.
    """
    if not bias_scores:
        print("No bias scores provided to plot.")
        return

    models = list(bias_scores.keys())
    scores = [bias_scores[m] for m in models]

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(models, scores)

    
    for bar, score in zip(bars, scores):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            score + (0.03 if score >= 0 else -0.08),  
            f"{score:.2f}",
            ha="center", va="bottom" if score >= 0 else "top", fontsize=12
        )

    ax.set_title("Average Bias Score by Model")
    ax.set_xlabel("Model")
    ax.set_ylabel("Average Bias (−2 to 2)")
    ax.set_ylim(*y_range)
    ax.axhline(0, color="black", linewidth=0.8)  
    ax.grid(axis="y", linestyle="--", alpha=0.3)

    plt.tight_layout()
    plt.show()
