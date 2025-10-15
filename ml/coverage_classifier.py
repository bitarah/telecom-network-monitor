"""
Coverage Quality Classifier for 5G Networks
Classifies network coverage into categories: Excellent, Good, Fair, Poor
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score, f1_score
import joblib
from pathlib import Path


class CoverageClassifier:
    def __init__(self, n_estimators=100):
        """Initialize coverage classifier"""
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            random_state=42,
            max_depth=10
        )
        self.scaler = StandardScaler()
        self.feature_names = None
        self.class_names = ['excellent', 'good', 'fair', 'poor']

    def create_labels(self, df):
        """
        Create coverage quality labels based on 5G metrics

        Rules based on 3GPP standards:
        - Excellent: RSRP > -80, RSRQ > -10, SINR > 18
        - Good: RSRP > -95, RSRQ > -12, SINR > 10
        - Fair: RSRP > -105, RSRQ > -15, SINR > 5
        - Poor: Below fair thresholds
        """
        conditions = [
            (df['rsrp_dbm'] > -80) & (df['rsrq_db'] > -10) & (df['sinr_db'] > 18),
            (df['rsrp_dbm'] > -95) & (df['rsrq_db'] > -12) & (df['sinr_db'] > 10),
            (df['rsrp_dbm'] > -105) & (df['rsrq_db'] > -15) & (df['sinr_db'] > 5),
        ]

        labels = np.select(conditions, ['excellent', 'good', 'fair'], default='poor')
        return labels

    def prepare_features(self, df):
        """Extract features for classification"""
        features = df[[
            'rsrp_dbm',
            'rsrq_db',
            'sinr_db',
            'cqi',
            'throughput_mbps',
            'latency_ms',
            'packet_loss_pct'
        ]].copy()

        return features

    def train(self, df):
        """Train coverage classifier"""
        print("🔧 Training Coverage Classifier...")

        # Create labels if not present
        if 'coverage_quality' not in df.columns:
            df['coverage_quality'] = self.create_labels(df)

        # Prepare features and labels
        features = self.prepare_features(df)
        self.feature_names = features.columns.tolist()
        labels = df['coverage_quality']

        # Split train/test
        split = int(0.8 * len(features))
        X_train, X_test = features[:split], features[split:]
        y_train, y_test = labels[:split], labels[split:]

        print(f"   Training samples: {len(X_train)}")
        print(f"   Test samples: {len(X_test)}")

        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        # Train model
        self.model.fit(X_train_scaled, y_train)

        # Predict
        y_pred = self.model.predict(X_test_scaled)

        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='weighted')

        print(f"✅ Model trained successfully!")
        print(f"   Accuracy: {accuracy:.4f}")
        print(f"   F1 Score: {f1:.4f}")

        print("\n📊 Classification Report:")
        print(classification_report(y_test, y_pred))

        # Feature importance
        importance = pd.DataFrame({
            'feature': self.feature_names,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)

        print("\n🔍 Feature Importance:")
        print(importance)

        return {
            'accuracy': accuracy,
            'f1': f1,
            'predictions': y_pred,
            'actual': y_test
        }

    def predict(self, df):
        """Predict coverage quality for new data"""
        features = self.prepare_features(df)
        X = self.scaler.transform(features)

        predictions = self.model.predict(X)
        probabilities = self.model.predict_proba(X)

        return predictions, probabilities

    def save(self, model_dir):
        """Save model and scaler"""
        model_dir = Path(model_dir)
        model_dir.mkdir(parents=True, exist_ok=True)

        joblib.dump(self.model, model_dir / "coverage_classifier.pkl")
        joblib.dump(self.scaler, model_dir / "coverage_scaler.pkl")
        joblib.dump(self.feature_names, model_dir / "coverage_features.pkl")

        print(f"💾 Model saved to {model_dir}")

    @classmethod
    def load(cls, model_dir):
        """Load trained model"""
        model_dir = Path(model_dir)

        classifier = cls()
        classifier.model = joblib.load(model_dir / "coverage_classifier.pkl")
        classifier.scaler = joblib.load(model_dir / "coverage_scaler.pkl")
        classifier.feature_names = joblib.load(model_dir / "coverage_features.pkl")

        return classifier


if __name__ == "__main__":
    # Load data
    data_path = Path(__file__).parent.parent / "data" / "raw" / "synthetic_5g_timeseries.csv"
    print(f"📁 Loading data from {data_path}")
    df = pd.read_csv(data_path)

    # Train model
    classifier = CoverageClassifier(n_estimators=100)
    results = classifier.train(df)

    # Save model
    model_dir = Path(__file__).parent / "models"
    classifier.save(model_dir)

    # Show distribution of coverage quality
    print("\n📈 Coverage Quality Distribution:")
    print(df['coverage_quality'].value_counts())

    print("\n✅ Coverage Classifier training complete!")
