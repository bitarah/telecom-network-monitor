# 5G Network ML Analytics - Gradio App

Interactive ML-powered network monitoring application for telecommunications engineers.

## Features

- **Anomaly Detection**: Real-time detection of network performance issues using Isolation Forest
- **Coverage Classification**: ML-based assessment of 5G signal quality (Excellent/Good/Fair/Poor)
- **Network Analysis**: Time-series analysis of network KPIs with automated insights

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

The app will be available at `http://localhost:7860`

## HuggingFace Spaces Deployment

This app is designed to run on HuggingFace Spaces:

1. Create a new Space on HuggingFace
2. Upload:
   - `app.py`
   - `requirements.txt`
   - `../ml/` directory (models and code)
   - `../data/` directory (sample data)
3. Set SDK to Gradio

## ML Models

- **Anomaly Detector**: Isolation Forest for outlier detection
- **Coverage Classifier**: Random Forest for quality classification
- **KPI Predictor**: LSTM for throughput/latency forecasting

## Data

Uses real-world 5G network KPIs:
- RSRP (Reference Signal Received Power)
- RSRQ (Reference Signal Received Quality)
- SINR (Signal-to-Interference-plus-Noise Ratio)
- CQI (Channel Quality Indicator)
- Throughput, Latency, Packet Loss
