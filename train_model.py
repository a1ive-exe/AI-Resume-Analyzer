import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import joblib

# Step 1: Load dataset
df = pd.read_csv('large_resume_data.csv')

# Step 2: Features and labels
X = df['skills'].astype(str)  # Ensure all inputs are strings
y = df['predicted_role']

# Step 3: Vectorize skills
vectorizer = CountVectorizer()
X_vec = vectorizer.fit_transform(X)

# Step 4: Encode target labels
label_encoder = LabelEncoder()
y_enc = label_encoder.fit_transform(y)

# Step 5: Train/test split
X_train, X_test, y_train, y_test = train_test_split(X_vec, y_enc, test_size=0.2, random_state=42)

# Step 6: Train the model
model = MultinomialNB()
model.fit(X_train, y_train)

# Step 7: Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"✅ Model Accuracy: {accuracy*100:.2f}%")

# Step 8: Save model, vectorizer, and label encoder
joblib.dump(model, 'career_model.pkl')
joblib.dump(vectorizer, 'vectorizer.pkl')
joblib.dump(label_encoder, 'label_encoder.pkl')
print("✅ Model, Vectorizer, and Label Encoder saved successfully.")
