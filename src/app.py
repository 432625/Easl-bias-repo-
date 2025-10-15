from flask import Flask, jsonify, request, send_file
from main import compute_bias_scores
from graph_visualization import make_bias_bar_chart_png

app = Flask(__name__, static_folder=".", static_url_path="")

@app.get("/")
def index():
    return send_file("index1.html")

@app.post("/analyze")
def analyze():
    try:
        
        payload = request.get_json(silent=True) or {}
        filter_model = payload.get("filter", "all")

        
        scores = compute_bias_scores()  

        
        if filter_model != "all" and filter_model in scores:
            filtered = {filter_model: scores[filter_model]}
        else:
            filtered = scores

        
        chart_b64 = make_bias_bar_chart_png(filtered, y_range=(-2, 2))

        return jsonify({"scores": filtered, "chart": chart_b64})
    except Exception as e:
        print("❌ Error in /analyze:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)

