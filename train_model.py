import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
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
    
    # --- Model 1: Logistic Regression ---
    print("\nTraining Lightweight AI Model (Logistic Regression)...")
    lr_model = LogisticRegression(random_state=42, max_iter=1000)
    lr_model.fit(X_train_scaled, y_train)
    
    print("\n--- Logistic Regression Evaluation ---")
    y_pred_lr = lr_model.predict(X_test_scaled)
    acc_lr = accuracy_score(y_test, y_pred_lr)
    print(f"Logistic Regression Accuracy: {acc_lr * 100:.2f}%")
    print(classification_report(y_test, y_pred_lr, target_names=["Normal (0)", "Cyber Attack (1)"]))
    
    # --- Model 2: Decision Tree ---
    print("\nTraining Lightweight AI Model (Decision Tree Classifier)...")
    # Max depth is limited to prevent overfitting and reduce FHE compilation complexity
    dt_model = DecisionTreeClassifier(max_depth=5, random_state=42)
    dt_model.fit(X_train_scaled, y_train)
    
    print("\n--- Decision Tree Evaluation ---")
    y_pred_dt = dt_model.predict(X_test_scaled)
    acc_dt = accuracy_score(y_test, y_pred_dt)
    print(f"Decision Tree Accuracy: {acc_dt * 100:.2f}%")
    print(classification_report(y_test, y_pred_dt, target_names=["Normal (0)", "Cyber Attack (1)"]))
    
    # Save the trained models and scaler for later use
    joblib.dump(lr_model, 'ugv_lr_model.pkl')
    joblib.dump(dt_model, 'ugv_dt_model.pkl')
    joblib.dump(scaler, 'ugv_scaler.pkl')
    print("\nModels and Scaler saved successfully.")

if __name__ == "__main__":
    train_and_evaluate_model()
