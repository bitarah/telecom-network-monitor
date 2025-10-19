"""
LSTM-based KPI Prediction for 5G Networks
Predicts throughput and latency based on historical patterns
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
from pathlib import Path

try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import LSTM, Dense, Dropout
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    print("⚠️  TensorFlow not available. Using simple baseline model.")


class KPIPredictor:
    def __init__(self, sequence_length=50, use_lstm=True):
        """
        Initialize KPI predictor

        Args:
            sequence_length: Number of time steps to look back
            use_lstm: Use LSTM (requires TensorFlow) or simple moving average
        """
        self.sequence_length = sequence_length
        self.use_lstm = use_lstm and TENSORFLOW_AVAILABLE
        self.model = None
        self.scaler = MinMaxScaler()
        self.target_scaler = MinMaxScaler()
        self.feature_names = None

    def create_sequences(self, data, target):
        """Create sequences for time-series prediction"""
        X, y = [], []

        for i in range(len(data) - self.sequence_length):
            X.append(data[i:i + self.sequence_length])
            y.append(target[i + self.sequence_length])

        return np.array(X), np.array(y)

    def prepare_data(self, df, target_col='throughput_mbps'):
        """Prepare data for training"""
        # Select features
        feature_cols = ['rsrp_dbm', 'rsrq_db', 'sinr_db', 'cqi',
                       'throughput_mbps', 'latency_ms', 'packet_loss_pct']

        features = df[feature_cols].values
        target = df[[target_col]].values

        # Scale data
        features_scaled = self.scaler.fit_transform(features)
        target_scaled = self.target_scaler.fit_transform(target)

        # Create sequences
        X, y = self.create_sequences(features_scaled, target_scaled)

        return X, y

    def build_lstm_model(self, input_shape):
        """Build LSTM model"""
        model = Sequential([
            LSTM(64, activation='relu', input_shape=input_shape, return_sequences=True),
            Dropout(0.2),
            LSTM(32, activation='relu'),
            Dropout(0.2),
            Dense(16, activation='relu'),
            Dense(1)
        ])

        model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        return model

    def train(self, df, target_col='throughput_mbps', epochs=20, batch_size=32):
        """Train prediction model"""
        print(f"🔧 Training KPI Predictor for {target_col}...")

        # Prepare data
        X, y = self.prepare_data(df, target_col)

        # Split train/test
        split = int(0.8 * len(X))
        X_train, X_test = X[:split], X[split:]
        y_train, y_test = y[:split], y[split:]

        print(f"   Training samples: {len(X_train)}")
        print(f"   Test samples: {len(X_test)}")

        if self.use_lstm:
            # Build and train LSTM
            self.model = self.build_lstm_model((X_train.shape[1], X_train.shape[2]))

            history = self.model.fit(
                X_train, y_train,
                validation_data=(X_test, y_test),
                epochs=epochs,
                batch_size=batch_size,
                verbose=0
            )

            # Evaluate
            y_pred = self.model.predict(X_test, verbose=0)
        else:
            # Simple moving average baseline
            print("   Using moving average baseline...")
            # Average of last values
            y_pred = np.mean(X_test[:, -5:, 4], axis=1).reshape(-1, 1)  # Last 5 throughput values

        # Inverse transform predictions
        y_pred_original = self.target_scaler.inverse_transform(y_pred)
        y_test_original = self.target_scaler.inverse_transform(y_test)

        # Calculate metrics
        mae = mean_absolute_error(y_test_original, y_pred_original)
        rmse = np.sqrt(mean_squared_error(y_test_original, y_pred_original))
        r2 = r2_score(y_test_original, y_pred_original)

        print(f"✅ Model trained successfully!")
        print(f"   MAE: {mae:.2f} Mbps")
        print(f"   RMSE: {rmse:.2f} Mbps")
        print(f"   R²: {r2:.4f}")

        return {
            'mae': mae,
            'rmse': rmse,
            'r2': r2,
            'predictions': y_pred_original,
            'actual': y_test_original
        }

    def predict(self, sequence):
        """Predict next value given a sequence"""
        if self.use_lstm:
            sequence_scaled = self.scaler.transform(sequence)
            sequence_scaled = sequence_scaled.reshape(1, self.sequence_length, -1)
            prediction = self.model.predict(sequence_scaled, verbose=0)
            return self.target_scaler.inverse_transform(prediction)[0][0]
        else:
            # Simple average
            return np.mean(sequence[-5:, 4])  # Last 5 throughput values

    def save(self, model_dir, target_col='throughput'):
        """Save model"""
        model_dir = Path(model_dir)
        model_dir.mkdir(parents=True, exist_ok=True)

        if self.use_lstm:
            self.model.save(model_dir / f"kpi_{target_col}_lstm.keras")

        joblib.dump(self.scaler, model_dir / f"kpi_{target_col}_scaler.pkl")
        joblib.dump(self.target_scaler, model_dir / f"kpi_{target_col}_target_scaler.pkl")
        joblib.dump({
            'sequence_length': self.sequence_length,
            'use_lstm': self.use_lstm
        }, model_dir / f"kpi_{target_col}_config.pkl")

        print(f"💾 Model saved to {model_dir}")


if __name__ == "__main__":
    # Load data
    data_path = Path(__file__).parent.parent / "data" / "raw" / "synthetic_5g_timeseries.csv"
    print(f"📁 Loading data from {data_path}")
    df = pd.read_csv(data_path)

    # Sort by timestamp
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp').reset_index(drop=True)

    # Train throughput predictor
    predictor = KPIPredictor(sequence_length=50, use_lstm=TENSORFLOW_AVAILABLE)
    results = predictor.train(df, target_col='throughput_mbps', epochs=15)

    # Save model
    model_dir = Path(__file__).parent / "models"
    predictor.save(model_dir, target_col='throughput')

    print("\n✅ KPI Predictor training complete!")
