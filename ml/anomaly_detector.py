"""
Anomaly Detection for 5G Network Performance
Uses Isolation Forest to detect network anomalies
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
from pathlib import Path

class NetworkAnomalyDetector:
    def __init__(self, contamination=0.05):
        """
        Initialize anomaly detector

        Args:
            contamination: Expected proportion of outliers (default 5%)
        """
        self.model = IsolationForest(
            contamination=contamination,
            random_state=42,
            n_estimators=100
        )
        self.scaler = StandardScaler()
        self.feature_names = None

    def prepare_features(self, df):
        """Extract features for anomaly detection"""
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
        """Train anomaly detection model"""
        print("🔧 Training Anomaly Detection Model...")

        # Prepare features
        features = self.prepare_features(df)
        self.feature_names = features.columns.tolist()

        # Scale features
        X = self.scaler.fit_transform(features)

        # Train model
        self.model.fit(X)

        # Get predictions on training data
        predictions = self.model.predict(X)
        anomaly_scores = self.model.score_samples(X)

        # Convert predictions: -1 (anomaly) to 1, 1 (normal) to 0
        predictions = (predictions == -1).astype(int)

        # Calculate metrics
        n_anomalies = predictions.sum()
        anomaly_rate = n_anomalies / len(predictions) * 100

        print(f"✅ Model trained successfully!")
        print(f"   Total samples: {len(df)}")
        print(f"   Detected anomalies: {n_anomalies} ({anomaly_rate:.1f}%)")

        if 'is_anomaly' in df.columns:
            # Compare with labeled anomalies
            actual_anomalies = df['is_anomaly'].sum()
            print(f"   Actual anomalies: {actual_anomalies} ({actual_anomalies/len(df)*100:.1f}%)")

        return predictions, anomaly_scores

    def predict(self, df):
        """Detect anomalies in new data"""
        features = self.prepare_features(df)
        X = self.scaler.transform(features)

        # Get predictions and scores
        predictions = self.model.predict(X)
        anomaly_scores = self.model.score_samples(X)

        # Convert to binary (1 = anomaly, 0 = normal)
        anomalies = (predictions == -1).astype(int)

        return anomalies, anomaly_scores

    def save(self, model_dir):
        """Save model and scaler"""
        model_dir = Path(model_dir)
        model_dir.mkdir(parents=True, exist_ok=True)

        joblib.dump(self.model, model_dir / "anomaly_detector.pkl")
        joblib.dump(self.scaler, model_dir / "anomaly_scaler.pkl")
        joblib.dump(self.feature_names, model_dir / "anomaly_features.pkl")

        print(f"💾 Model saved to {model_dir}")

    @classmethod
    def load(cls, model_dir):
        """Load trained model"""
        model_dir = Path(model_dir)

        detector = cls()
        detector.model = joblib.load(model_dir / "anomaly_detector.pkl")
        detector.scaler = joblib.load(model_dir / "anomaly_scaler.pkl")
        detector.feature_names = joblib.load(model_dir / "anomaly_features.pkl")

        return detector


if __name__ == "__main__":
    # Load data
    data_path = Path(__file__).parent.parent / "data" / "raw" / "synthetic_5g_timeseries.csv"
    print(f"📁 Loading data from {data_path}")
    df = pd.read_csv(data_path)

    # Train model
    detector = NetworkAnomalyDetector(contamination=0.05)
    predictions, scores = detector.train(df)

    # Add predictions to dataframe
    df['predicted_anomaly'] = predictions
    df['anomaly_score'] = scores

    # Save model
    model_dir = Path(__file__).parent / "models"
    detector.save(model_dir)

    # Save results
    output_path = Path(__file__).parent.parent / "data" / "processed" / "5g_with_anomalies.csv"
    df.to_csv(output_path, index=False)
    print(f"📊 Results saved to {output_path}")

    # Show some anomalies
    anomalies = df[df['predicted_anomaly'] == 1].head(10)
    print("\n🚨 Sample Detected Anomalies:")
    print(anomalies[['timestamp', 'throughput_mbps', 'latency_ms', 'rsrp_dbm', 'scenario']])
