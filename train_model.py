import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# dataset load
df = pd.read_csv("spam.txt", sep='\t', names=["label","message"])

# text lowercase
df['message'] = df['message'].str.lower()

# TF-IDF
tfidf = TfidfVectorizer()
X = tfidf.fit_transform(df['message'])
y = df['label']

# model train
model = MultinomialNB()
model.fit(X, y)

# save model
pickle.dump(model, open("model.pkl","wb"))
pickle.dump(tfidf, open("vectorizer.pkl","wb"))

print("Model trained and saved successfully!")