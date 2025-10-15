import matplotlib
matplotlib.use("Agg")  
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def _build_bar_figure(bias_scores: dict, y_range=(-2, 2)):
    models = list(bias_scores.keys())
    scores = [bias_scores[m] for m in models]

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(models, scores)

    for bar, score in zip(bars, scores):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            score + (0.03 if score >= 0 else -0.08),
            f"{score:.2f}",
            ha="center",
            va="bottom" if score >= 0 else "top",
            fontsize=12
        )

    ax.set_title("Average Bias Score by Model")
    ax.set_xlabel("Model")
    ax.set_ylabel("Average Bias (−2 to 2)")
    ax.set_ylim(*y_range)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    fig.tight_layout()
    return fig


def show_bias_bar_chart(bias_scores: dict, y_range=(-2, 2)):
    fig = _build_bar_figure(bias_scores, y_range)
    
    plt.close(fig)


def make_bias_bar_chart_png(bias_scores: dict, y_range=(-2, 2)) -> str:
    fig = _build_bar_figure(bias_scores, y_range)
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=160)
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("ascii")
