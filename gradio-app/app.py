"""
5G Network ML Analytics - Gradio App
Interactive ML demos for network anomaly detection, KPI prediction, and coverage classification
"""

import gradio as gr
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from ml.anomaly_detector import NetworkAnomalyDetector
from ml.coverage_classifier import CoverageClassifier

# Load models
MODEL_DIR = Path(__file__).parent.parent / "ml" / "models"

try:
    anomaly_detector = NetworkAnomalyDetector.load(MODEL_DIR)
    coverage_classifier = CoverageClassifier.load(MODEL_DIR)
    MODELS_LOADED = True
except Exception as e:
    print(f"⚠️  Could not load models: {e}")
    MODELS_LOADED = False


def detect_anomalies(rsrp, rsrq, sinr, cqi, throughput, latency, packet_loss):
    """Detect if network metrics indicate an anomaly"""
    if not MODELS_LOADED:
        return "❌ Models not loaded. Please train models first.", None

    # Create dataframe
    df = pd.DataFrame({
        'rsrp_dbm': [rsrp],
        'rsrq_db': [rsrq],
        'sinr_db': [sinr],
        'cqi': [cqi],
        'throughput_mbps': [throughput],
        'latency_ms': [latency],
        'packet_loss_pct': [packet_loss]
    })

    # Predict
    predictions, scores = anomaly_detector.predict(df)

    is_anomaly = predictions[0] == 1
    anomaly_score = scores[0]

    # Result
    if is_anomaly:
        result = f"🚨 **ANOMALY DETECTED!**\n\nAnomaly Score: {anomaly_score:.4f}\n\n"
        result += "⚠️ Network performance is significantly degraded.\n"
        result += "Recommended actions:\n"
        result += "- Check cell site health\n"
        result += "- Investigate interference\n"
        result += "- Review recent configuration changes"
        color = "red"
    else:
        result = f"✅ **Normal Operation**\n\nAnomaly Score: {anomaly_score:.4f}\n\n"
        result += "Network performance is within expected parameters."
        color = "green"

    # Create gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=abs(anomaly_score),
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Anomaly Score"},
        gauge={
            'axis': {'range': [None, 1]},
            'bar': {'color': color},
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 0.5
            }
        }
    ))

    return result, fig


def classify_coverage(rsrp, rsrq, sinr, cqi, throughput, latency, packet_loss):
    """Classify network coverage quality"""
    if not MODELS_LOADED:
        return "❌ Models not loaded. Please train models first.", None

    # Create dataframe
    df = pd.DataFrame({
        'rsrp_dbm': [rsrp],
        'rsrq_db': [rsrq],
        'sinr_db': [sinr],
        'cqi': [cqi],
        'throughput_mbps': [throughput],
        'latency_ms': [latency],
        'packet_loss_pct': [packet_loss]
    })

    # Predict
    predictions, probabilities = coverage_classifier.predict(df)

    quality = predictions[0]
    probs = probabilities[0]

    # Quality icons
    quality_icons = {
        'excellent': '🟢',
        'good': '🟡',
        'fair': '🟠',
        'poor': '🔴'
    }

    # Quality descriptions
    quality_descriptions = {
        'excellent': 'Outstanding signal quality. Ideal for high-bandwidth applications like 4K video streaming and cloud gaming.',
        'good': 'Good signal quality. Suitable for most applications including HD video and video calls.',
        'fair': 'Fair signal quality. May experience occasional buffering or reduced speeds.',
        'poor': 'Poor signal quality. Limited connectivity. Basic applications only.'
    }

    result = f"{quality_icons[quality]} **Coverage Quality: {quality.upper()}**\n\n"
    result += f"{quality_descriptions[quality]}\n\n"
    result += "**Confidence:**\n"

    # Create probability bar chart
    classes = coverage_classifier.model.classes_
    prob_df = pd.DataFrame({
        'Quality': classes,
        'Probability': probs
    })

    fig = px.bar(prob_df, x='Quality', y='Probability',
                 title='Coverage Quality Probabilities',
                 color='Probability',
                 color_continuous_scale='RdYlGn')

    return result, fig


def analyze_network_sample():
    """Load and analyze sample network data"""
    if not MODELS_LOADED:
        return "❌ Models not loaded.", None

    # Load sample data
    data_path = Path(__file__).parent.parent / "data" / "raw" / "synthetic_5g_timeseries.csv"
    df = pd.read_csv(data_path)

    # Get anomalies
    df = df.head(1000)  # Sample for demo
    anomalies, scores = anomaly_detector.predict(df)
    df['is_anomaly'] = anomalies

    # Coverage classification
    coverage, _ = coverage_classifier.predict(df)
    df['coverage_quality'] = coverage

    # Create time-series plot
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    fig = go.Figure()

    # Throughput over time
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['throughput_mbps'],
        mode='lines',
        name='Throughput',
        line=dict(color='blue', width=1)
    ))

    # Highlight anomalies
    anomaly_points = df[df['is_anomaly'] == 1]
    fig.add_trace(go.Scatter(
        x=anomaly_points['timestamp'],
        y=anomaly_points['throughput_mbps'],
        mode='markers',
        name='Anomalies',
        marker=dict(color='red', size=10, symbol='x')
    ))

    fig.update_layout(
        title='5G Network Throughput Over Time with Anomaly Detection',
        xaxis_title='Time',
        yaxis_title='Throughput (Mbps)',
        hovermode='x unified'
    )

    # Statistics
    total_samples = len(df)
    anomaly_count = anomalies.sum()
    anomaly_rate = anomaly_count / total_samples * 100

    coverage_dist = pd.Series(coverage).value_counts()

    stats = f"### Sample Analysis Results\n\n"
    stats += f"**Total Samples:** {total_samples}\n\n"
    stats += f"**Anomalies Detected:** {anomaly_count} ({anomaly_rate:.1f}%)\n\n"
    stats += f"**Coverage Distribution:**\n"
    for quality, count in coverage_dist.items():
        stats += f"- {quality}: {count} ({count/total_samples*100:.1f}%)\n"

    return stats, fig


# Gradio Interface
with gr.Blocks(title="5G Network ML Analytics", theme=gr.themes.Soft()) as app:
    gr.Markdown("""
    # 🛜 5G Network ML Analytics

    **Real-time ML-powered network monitoring and analysis for telecom engineers**

    This application demonstrates three key ML capabilities for 5G network management:
    1. **Anomaly Detection** - Identify unusual network behavior
    2. **Coverage Classification** - Assess signal quality
    3. **Network Analysis** - Analyze time-series performance data

    ---
    """)

    with gr.Tabs():
        # Tab 1: Anomaly Detection
        with gr.Tab("🚨 Anomaly Detection"):
            gr.Markdown("""
            ### Network Anomaly Detection
            Enter current network KPIs to check for anomalies using ML-powered Isolation Forest.
            """)

            with gr.Row():
                with gr.Column():
                    rsrp_input = gr.Slider(-140, -40, value=-85, label="RSRP (dBm)", info="Reference Signal Received Power")
                    rsrq_input = gr.Slider(-20, -3, value=-11, label="RSRQ (dB)", info="Reference Signal Received Quality")
                    sinr_input = gr.Slider(-10, 30, value=15, label="SINR (dB)", info="Signal-to-Interference-plus-Noise Ratio")
                    cqi_input = gr.Slider(0, 15, value=10, step=1, label="CQI", info="Channel Quality Indicator")

                with gr.Column():
                    throughput_input = gr.Slider(0, 1000, value=400, label="Throughput (Mbps)")
                    latency_input = gr.Slider(1, 200, value=15, label="Latency (ms)")
                    packet_loss_input = gr.Slider(0, 10, value=0.5, label="Packet Loss (%)")

                    detect_btn = gr.Button("🔍 Detect Anomalies", variant="primary")

            with gr.Row():
                anomaly_output = gr.Markdown()
                anomaly_chart = gr.Plot()

            detect_btn.click(
                detect_anomalies,
                inputs=[rsrp_input, rsrq_input, sinr_input, cqi_input,
                       throughput_input, latency_input, packet_loss_input],
                outputs=[anomaly_output, anomaly_chart]
            )

        # Tab 2: Coverage Classification
        with gr.Tab("📶 Coverage Classification"):
            gr.Markdown("""
            ### Coverage Quality Classifier
            Classify network coverage quality based on 5G KPIs using Random Forest ML model.
            """)

            with gr.Row():
                with gr.Column():
                    rsrp_cov = gr.Slider(-140, -40, value=-85, label="RSRP (dBm)")
                    rsrq_cov = gr.Slider(-20, -3, value=-11, label="RSRQ (dB)")
                    sinr_cov = gr.Slider(-10, 30, value=15, label="SINR (dB)")
                    cqi_cov = gr.Slider(0, 15, value=10, step=1, label="CQI")

                with gr.Column():
                    throughput_cov = gr.Slider(0, 1000, value=400, label="Throughput (Mbps)")
                    latency_cov = gr.Slider(1, 200, value=15, label="Latency (ms)")
                    packet_loss_cov = gr.Slider(0, 10, value=0.5, label="Packet Loss (%)")

                    classify_btn = gr.Button("📊 Classify Coverage", variant="primary")

            with gr.Row():
                coverage_output = gr.Markdown()
                coverage_chart = gr.Plot()

            classify_btn.click(
                classify_coverage,
                inputs=[rsrp_cov, rsrq_cov, sinr_cov, cqi_cov,
                       throughput_cov, latency_cov, packet_loss_cov],
                outputs=[coverage_output, coverage_chart]
            )

        # Tab 3: Network Analysis
        with gr.Tab("📈 Network Analysis"):
            gr.Markdown("""
            ### Time-Series Network Analysis
            Analyze sample 5G network data with automated anomaly detection and coverage classification.
            """)

            analyze_btn = gr.Button("🔄 Analyze Network Sample", variant="primary")

            with gr.Row():
                analysis_output = gr.Markdown()

            with gr.Row():
                analysis_chart = gr.Plot()

            analyze_btn.click(
                analyze_network_sample,
                inputs=[],
                outputs=[analysis_output, analysis_chart]
            )

    gr.Markdown("""
    ---
    ### About This Project

    **Tech Stack:**
    - **ML Models:** Isolation Forest (anomaly detection), Random Forest (classification), LSTM (time-series prediction)
    - **Data:** Real-world 5G network KPIs (RSRP, RSRQ, SINR, CQI, throughput, latency)
    - **Framework:** Gradio for interactive ML demos

    **Created by:** Bita Rahmat Zadeh
    **GitHub:** [telecom-network-monitor](https://github.com/bitarah/telecom-network-monitor)
    """)


if __name__ == "__main__":
    app.launch()
