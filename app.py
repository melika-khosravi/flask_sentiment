from flask import Flask , redirect, url_for , render_template , request
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json
from prometheus_flask_exporter import PrometheusMetrics


app = Flask(__name__)
metrics = PrometheusMetrics(app)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict" , methods=["POST","GET"])
def predict():
    if request.method=="POST":
        test = request.form['text']
        score=SentimentIntensityAnalyzer().polarity_scores(test)
        return redirect(url_for("result" , scre=json.dumps(score))) 
    else:
        return render_template("index.html")

@app.route("/result")
def result():
    scre = request.args.get('scre')
    if scre:
        try:
            scre_data = json.loads(scre.replace("'", '"'))
            compound = scre_data['compound']
            if compound >= 0.05:
                sentiment = "Positive"
            elif compound <= -0.05:
                sentiment = "Negative"
            else:
                sentiment = "Neutral"
            return f"<h1>{sentiment}</h1>"
        except json.JSONDecodeError:
            return "Invalid scre format", 400
    else:
        return "Missing scre parameter", 400
    
if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)
