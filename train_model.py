import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

def train_and_evaluate_model():
    print("Loading UGV combat data...")
    
    # Load the generated dataset
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ugv_combat_data.csv')
    df = pd.read_csv(data_path)
    
    # Features and Target
    # We drop 'timestamp' as it's not a predictive feature
    X = df[['speed_kmh', 'steering_angle', 'gps_lat', 'gps_long']]
    y = df['label']
    
    print(f"Dataset shape: {X.shape}")
    
    # Split data into training and testing sets (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Standardization (Very important for Logistic Regression and later FHE)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print("Training Lightweight AI Model (Logistic Regression)...")
    # Logistic Regression is highly compatible with Fully Homomorphic Encryption
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(X_train_scaled, y_train)
    
    # Evaluation
    print("\n--- Evaluation on Plaintext Data ---")
    y_pred = model.predict(X_test_scaled)
    
    acc = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {acc * 100:.2f}%")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=["Normal (0)", "Cyber Attack (1)"]))
    
    # Save the trained model and scaler for later use (Phase 3: FHE)
    joblib.dump(model, 'ugv_lr_model.pkl')
    joblib.dump(scaler, 'ugv_scaler.pkl')
    print("Model and Scaler saved successfully.")

if __name__ == "__main__":
    train_and_evaluate_model()
