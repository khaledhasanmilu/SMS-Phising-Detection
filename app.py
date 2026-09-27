from flask import Flask, render_template, request, session
import json
import pickle

app = Flask(__name__)
app.secret_key = "phishguard-123"

model = pickle.load(open("model.pkl", "rb"))
tfidf = pickle.load(open("vectorizer.pkl", "rb"))

# test-set metrics produced by train_model.py (fallback zeros if missing)
try:
    with open("metrics.json") as f:
        METRICS = json.load(f)
except Exception:
    METRICS = {
        "accuracy": 0, "precision": 0, "recall": 0, "f1": 0,
        "confusion": [[0, 0], [0, 0]], "train_size": 0, "test_size": 0,
    }

def clean(text):
    return text.lower()

def rule_check(text):
    keywords = ["win", "urgent", "verify", "free"]
    if any(k in text for k in keywords):
        return True
    if "http" in text or "bit.ly" in text:
        return True
    return False

def init_stats():
    if "checked" not in session:
        session["checked"] = 0
        session["safe"] = 0
        session["threats"] = 0

def get_stats():
    init_stats()
    return {
        "checked": session["checked"],
        "safe": session["safe"],
        "threats": session["threats"],
    }

def scan_message(text):
    """Same detection logic as before. Returns (result, reasons, confidence)."""
    clean_text = clean(text)
    vector = tfidf.transform([clean_text])
    pred = model.predict(vector)[0]
    # model's own confidence in its prediction (0-100)
    proba = model.predict_proba(vector)[0]
    conf = round(float(proba.max()) * 100)

    if rule_check(clean_text):
        result = "Phishing 🚨"
    else:
        result = "Safe ✅" if pred == "ham" else "Phishing 🚨"

    reasons = []
    low = clean_text
    for kw in ["win", "urgent", "verify", "free"]:
        if kw in low:
            reasons.append(f"contains keyword '{kw}'")
    if "http" in low or "bit.ly" in low:
        reasons.append("contains suspicious link")
    return result, reasons, conf

@app.route("/")
def home():
    return render_template(
        "index.html", stats=get_stats(), accuracy=METRICS["accuracy"]
    )

@app.route("/scanner", methods=["GET", "POST"])
def scanner():
    result = ""
    reasons = []
    sms_text = ""
    conf = 0

    init_stats()

    if request.method == "POST":
        if "reset" in request.form:
            session["checked"] = 0
            session["safe"] = 0
            session["threats"] = 0
        else:
            sms_text = request.form.get("sms", "")
            if sms_text.strip():
                result, reasons, conf = scan_message(sms_text)
                session["checked"] += 1
                session["safe"] += 1 if result == "Safe ✅" else 0
                session["threats"] += 1 if result == "Phishing 🚨" else 0
                session.modified = True

    return render_template(
        "scanner.html", result=result, reasons=reasons, conf=conf,
        stats=get_stats(), sms_text=sms_text
    )

@app.route("/how-it-works")
def how_it_works():
    return render_template("guide.html", stats=get_stats())

@app.route("/scam-cases")
def scam_cases():
    return render_template("scams.html", stats=get_stats())

@app.route("/about")
def about():
    return render_template("about.html", stats=get_stats(), metrics=METRICS)

if __name__ == "__main__":
    app.run(debug=True)