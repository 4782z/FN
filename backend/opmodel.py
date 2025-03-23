import pandas as pd
import joblib
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Download necessary NLTK resources
nltk.download("stopwords")
nltk.download("wordnet")

# Text Preprocessing
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)  # Remove URLs
    text = re.sub(r"[^a-zA-Z\s]", "", text)  # Remove special characters & numbers
    text = re.sub(r"\s+", " ", text)  # Remove extra whitespaces
    words = text.split()
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    return " ".join(words)

# Load dataset
df = pd.read_csv("news.csv")
df["label"] = df["label"].map({"Fake": 1, "Real": 0})  # Convert to binary labels
df["text"] = df["text"].apply(preprocess_text)  # Apply preprocessing

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(df["text"], df["label"], test_size=0.2, random_state=42, stratify=df["label"])

# Define TF-IDF Vectorizer
tfidf = TfidfVectorizer(ngram_range=(1,2), max_df=0.9, min_df=2, stop_words="english")

# Define Pipeline (TF-IDF → Scaling → Logistic Regression)
pipeline = Pipeline([
    ("tfidf", tfidf),
    ("scaler", StandardScaler(with_mean=False)),  # Scaling TF-IDF
    ("logreg", LogisticRegression(class_weight="balanced", max_iter=1000))
])

# Hyperparameter Tuning (GridSearchCV)
param_grid = {
    "logreg__C": [0.1, 1, 10],  # Regularization strength
    "logreg__penalty": ["l1", "l2"],
    "logreg__solver": ["liblinear", "saga"]
}

grid = GridSearchCV(pipeline, param_grid, cv=5, scoring="f1", n_jobs=-1)
grid.fit(X_train, y_train)

# Get Best Model
best_model = grid.best_estimator_

# Predictions
y_pred = best_model.predict(X_test)

# Evaluation Metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print("Best Parameters:", grid.best_params_)
print(f"Model Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1-Score: {f1:.4f}")

# Confusion Matrix
conf_matrix = confusion_matrix(y_test, y_pred)
sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues", xticklabels=["Real", "Fake"], yticklabels=["Real", "Fake"])
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()

# Save the best model
joblib.dump(best_model, "optimized_fake_news_model.pkl")
print("Optimized model saved as optimized_fake_news_model.pkl")
