import json
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)

# dataset load
df = pd.read_csv("spam.txt", sep='\t', names=["label", "message"])

# text lowercase
df['message'] = df['message'].str.lower()

# TF-IDF
tfidf = TfidfVectorizer()
X = tfidf.fit_transform(df['message'])
y = df['label']

# train/test split (stratified, reproducible) — test set is NEVER seen in training
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# model train (on train split only)
model = MultinomialNB()
model.fit(X_train, y_train)

# evaluate on unseen test split
pred = model.predict(X_test)
acc = accuracy_score(y_test, pred)
prec = precision_score(y_test, pred, pos_label="spam")
rec = recall_score(y_test, pred, pos_label="spam")
f1 = f1_score(y_test, pred, pos_label="spam")
cm = confusion_matrix(y_test, pred, labels=["ham", "spam"]).tolist()

print(classification_report(y_test, pred))
print(f"Accuracy: {acc:.4f} | Precision(spam): {prec:.4f} | "
      f"Recall(spam): {rec:.4f} | F1(spam): {f1:.4f}")
print(f"Confusion [rows=true ham/spam, cols=pred ham/spam]: {cm}")

# save model
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(tfidf, open("vectorizer.pkl", "wb"))

# save metrics for the website to display
metrics = {
    "accuracy": round(acc * 100, 1),
    "precision": round(prec * 100, 1),
    "recall": round(rec * 100, 1),
    "f1": round(f1 * 100, 1),
    "confusion": cm,
    "train_size": int(len(y_train)),
    "test_size": int(len(y_test)),
}
with open("metrics.json", "w") as f:
    json.dump(metrics, f)

print("Model trained and saved successfully! (model.pkl, vectorizer.pkl, metrics.json)")
