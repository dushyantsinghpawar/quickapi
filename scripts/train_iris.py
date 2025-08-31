import json
import os

import joblib
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

iris = load_iris()
X, y = iris.data, iris.target
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

pipe = Pipeline(
    [("scaler", StandardScaler()), ("clf", LogisticRegression(max_iter=200))]
)
pipe.fit(Xtr, ytr)
acc = accuracy_score(yte, pipe.predict(Xte))

os.makedirs("artifacts", exist_ok=True)
bundle = {"model": pipe, "target_names": iris.target_names.tolist()}
joblib.dump(bundle, "artifacts/iris_clf.joblib")
with open("artifacts/iris_meta.json", "w") as f:
    json.dump({"test_accuracy": acc}, f)

print("Saved artifacts/iris_clf.joblib (test_acc=", round(acc, 3), ")")
