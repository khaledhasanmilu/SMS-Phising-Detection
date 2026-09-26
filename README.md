# 🛡️ PhishGuard — Check If That SMS Is Safe

Got a strange SMS? Prize message? Bank warning? Unknown link?
**Paste it into PhishGuard and get a clear answer in seconds — safe or scam.**

No signup. No fees. Nothing is stored. Works on your phone.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Flask](https://img.shields.io/badge/Flask-3.x-green)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.8-orange)

---

## ✨ What you can do here

| Page | What it's for |
|------|---------------|
| **Home** | Overview, live-scan demo, safety examples |
| **Scanner** | Paste any SMS → get **Safe** or **Scam** verdict with reasons |
| **Real Cases** | 6 true scam stories (bKash fraud, lottery, bank, courier, job, loan) with photos |
| **Safety Guide** | Warning signs, what-to-do tips, FAQ — plain language, no jargon |
| **About** | Why this was built |

Plus: **day / night mode**, fully **responsive** mobile design, hover animations.

---

## 🚀 Run it

**Requirements:** Python 3.10+

```powershell
# 1. Go to the project folder
Set-Location -LiteralPath ".\Spam Detection"

# 2. Install dependencies
pip install flask pandas scikit-learn

# 3. Start the server (model is already trained)
python app.py
```

Open in browser: **http://127.0.0.1:5000**

> Want to retrain the model? Run `python train_model.py` — it rebuilds
> `model.pkl` + `vectorizer.pkl` from `spam.txt`.

---

## 📁 Project structure

```
Spam Detection/
├── app.py                 # Website routes + SMS checking logic
├── train_model.py         # Model training script
├── spam.txt               # SMS dataset (~5,500 messages)
├── model.pkl              # Trained model (ready to use)
├── vectorizer.pkl         # Trained text vectorizer
├── templates/             # Pages (base, index, scanner, scams, guide, about)
└── static/                # style.css, script.js, img/
```

---

## 🧠 How checking works (short version)

1. You paste the SMS and press **Scan**.
2. The trained model scores the text, and a rule layer double-checks
   prize-bait words (`win`, `free`, `urgent`, `verify`) and suspicious
   links (`http`, `bit.ly`).
3. You get **Safe** or **Scam** — with the exact warning signs found.

No checker is perfect: if a message rushes you, promises money, or asks
for a code — treat it as a scam, even if unsure. **Never share OTPs.**

---

## 📷 Photo credits

Card photos: Wikimedia Commons contributors (free license), used for
illustration. See the credit lines on the Home and Real Cases pages.

---

Made to save real people from real SMS fraud. Stay safe. 🛡️
