"""
Machine Learning Training Script for Toronto Traffic Hotspot Prediction.

Trains two models:
1. RandomForestClassifier for congestion level prediction (Low/Medium/High)
2. RandomForestRegressor for vehicle count prediction

Features: hour, day_of_week, month, is_weekend, centreline_id
Targets: congestion_level (classification), total_vehicles (regression)
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import accuracy_score, classification_report, mean_absolute_error, r2_score
import joblib
import os
from datetime import datetime

def load_and_prepare_data():
    """
    Load the cleaned SVC data and prepare features and targets.
    """
    print("Loading cleaned SVC data...")
    
    # Load cleaned data
    data_path = "../data/processed/svc_clean_2022_2024.csv"
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Cleaned data not found at {data_path}. Please run clean_svc.py first.")
    
    df = pd.read_csv(data_path)
    print(f"   Loaded {len(df)} records")
    
    # Convert datetime to proper format
    df['datetime'] = pd.to_datetime(df['datetime'])
    
    # Define features and targets
    feature_columns = ['hour', 'day_of_week', 'month', 'is_weekend', 'centreline_id']
    classification_target = 'congestion_level'
    regression_target = 'total_vehicles'
    
    # Extract features and targets
    X = df[feature_columns].copy()
    y_classification = df[classification_target]
    y_regression = df[regression_target]
    
    print(f"   Features: {feature_columns}")
    print(f"   Classification target: {classification_target}")
    print(f"   Regression target: {regression_target}")
    print(f"   Unique centreline_ids: {X['centreline_id'].nunique()}")
    
    return X, y_classification, y_regression, df

def preprocess_features(X):
    """
    Preprocess features: OneHotEncode centreline_id, keep numerical features as-is.
    """
    print("Preprocessing features...")
    
    # Separate numerical and categorical features
    numerical_features = ['hour', 'day_of_week', 'month', 'is_weekend']
    categorical_features = ['centreline_id']
    
    # Extract numerical features
    X_numerical = X[numerical_features].copy()
    
    # OneHotEncode centreline_id
    encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    X_encoded = encoder.fit_transform(X[categorical_features])
    
    # Get feature names for encoded data
    encoded_feature_names = [f"centreline_{id}" for id in encoder.categories_[0]]
    X_encoded_df = pd.DataFrame(X_encoded, columns=encoded_feature_names, index=X.index)
    
    # Combine numerical and encoded features
    X_processed = pd.concat([X_numerical, X_encoded_df], axis=1)
    
    print(f"   Numerical features: {numerical_features}")
    print(f"   Encoded centreline_ids: {len(encoded_feature_names)} unique IDs")
    print(f"   Final feature matrix shape: {X_processed.shape}")
    
    return X_processed, encoder

def train_classification_model(X, y):
    """
    Train RandomForestClassifier for congestion level prediction.
    """
    print("\n" + "="*50)
    print("TRAINING CLASSIFICATION MODEL (Congestion Level)")
    print("="*50)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Training set: {X_train.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")
    
    # Train RandomForestClassifier
    print("Training RandomForestClassifier...")
    clf = RandomForestClassifier(
        n_estimators=100,
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    clf.fit(X_train, y_train)
    
    # Make predictions
    y_pred = clf.predict(X_test)
    
    # Evaluate model
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nClassification Results:")
    print(f"   Accuracy: {accuracy:.4f}")
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': clf.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print(f"\nTop 10 Most Important Features:")
    print(feature_importance.head(10))
    
    return clf, accuracy, feature_importance

def train_regression_model(X, y):
    """
    Train RandomForestRegressor for vehicle count prediction.
    """
    print("\n" + "="*50)
    print("TRAINING REGRESSION MODEL (Vehicle Count)")
    print("="*50)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"Training set: {X_train.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")
    print(f"Target range: {y.min()} to {y.max()} vehicles")
    
    # Train RandomForestRegressor
    print("Training RandomForestRegressor...")
    reg = RandomForestRegressor(
        n_estimators=100,
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    reg.fit(X_train, y_train)
    
    # Make predictions
    y_pred = reg.predict(X_test)
    
    # Evaluate model
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"\nRegression Results:")
    print(f"   Mean Absolute Error: {mae:.4f}")
    print(f"   R² Score: {r2:.4f}")
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': reg.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print(f"\nTop 10 Most Important Features:")
    print(feature_importance.head(10))
    
    return reg, mae, r2, feature_importance

def save_models_and_metadata(clf, reg, encoder, clf_accuracy, reg_mae, reg_r2, 
                           clf_importance, reg_importance, df):
    """
    Save trained models and metadata to ml/models/ directory.
    """
    print("\n" + "="*50)
    print("SAVING MODELS AND METADATA")
    print("="*50)
    
    # Create models directory if it doesn't exist
    models_dir = "models"
    os.makedirs(models_dir, exist_ok=True)
    
    # Save models
    clf_path = os.path.join(models_dir, "rf_congestion_cls.joblib")
    reg_path = os.path.join(models_dir, "rf_volume_reg.joblib")
    encoder_path = os.path.join(models_dir, "onehot_encoder.joblib")
    
    joblib.dump(clf, clf_path)
    joblib.dump(reg, reg_path)
    joblib.dump(encoder, encoder_path)
    
    print(f"SUCCESS: Models saved:")
    print(f"   Classification model: {clf_path}")
    print(f"   Regression model: {reg_path}")
    print(f"   OneHotEncoder: {encoder_path}")
    
    # Save metadata
    metadata = {
        'training_date': datetime.now().isoformat(),
        'data_shape': df.shape,
        'date_range': {
            'start': str(df['datetime'].min()),
            'end': str(df['datetime'].max())
        },
        'unique_locations': df['centreline_id'].nunique(),
        'classification_accuracy': clf_accuracy,
        'regression_mae': reg_mae,
        'regression_r2': reg_r2,
        'feature_columns': ['hour', 'day_of_week', 'month', 'is_weekend', 'centreline_id'],
        'classification_target': 'congestion_level',
        'regression_target': 'total_vehicles'
    }
    
    metadata_path = os.path.join(models_dir, "training_metadata.joblib")
    joblib.dump(metadata, metadata_path)
    print(f"   Training metadata: {metadata_path}")
    
    # Save feature importance
    clf_importance.to_csv(os.path.join(models_dir, "clf_feature_importance.csv"), index=False)
    reg_importance.to_csv(os.path.join(models_dir, "reg_feature_importance.csv"), index=False)
    print(f"   Feature importance files saved")
    
    return metadata

def main():
    """
    Main training pipeline.
    """
    print("TORONTO TRAFFIC HOTSPOT ML TRAINING")
    print("="*60)
    
    try:
        # Load and prepare data
        X, y_classification, y_regression, df = load_and_prepare_data()
        
        # Preprocess features
        X_processed, encoder = preprocess_features(X)
        
        # Train classification model
        clf, clf_accuracy, clf_importance = train_classification_model(X_processed, y_classification)
        
        # Train regression model
        reg, reg_mae, reg_r2, reg_importance = train_regression_model(X_processed, y_regression)
        
        # Save models and metadata
        metadata = save_models_and_metadata(
            clf, reg, encoder, clf_accuracy, reg_mae, reg_r2,
            clf_importance, reg_importance, df
        )
        
        print("\n" + "="*60)
        print("TRAINING COMPLETED SUCCESSFULLY!")
        print("="*60)
        print(f"Final Results:")
        print(f"   Classification Accuracy: {clf_accuracy:.4f}")
        print(f"   Regression MAE: {reg_mae:.4f}")
        print(f"   Regression R²: {reg_r2:.4f}")
        print(f"   Models saved to: ml/models/")
        print(f"   Ready for FastAPI backend integration!")
        
    except Exception as e:
        print(f"ERROR: Training failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()