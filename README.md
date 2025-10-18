# 🛜 5G Network Monitor - ML Analytics Platform

> **ML-powered real-time network monitoring and analytics for telecommunications engineers**

[![Live Demo](https://img.shields.io/badge/demo-live-brightgreen)]() [![ML Models](https://img.shields.io/badge/Gradio-HF%20Spaces-orange)]() [![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A full-stack ML application showcasing real-time 5G network performance monitoring with machine learning-powered anomaly detection, coverage classification, and predictive analytics.

## 🎯 Project Overview

This project demonstrates **end-to-end ML engineering skills** for the telecommunications industry:

- **Real Network Data**: Uses Ookla Open Data + synthetic 5G KPIs (RSRP, RSRQ, SINR, CQI)
- **Production ML Models**: Anomaly detection, coverage classification, time-series forecasting
- **Dual Platform Deployment**: React dashboard (GitHub Pages) + Gradio ML app (HuggingFace Spaces)
- **Interactive Visualizations**: Real-time charts, geographic heatmaps, performance analytics

## ✨ Key Features

### 📊 React Dashboard
- **Real-time Metrics**: Live throughput, latency, signal strength, network quality
- **Time-Series Analysis**: Interactive Chart.js visualizations of network performance
- **Geographic Coverage**: City-by-city network performance mapping
- **Hourly Analytics**: Performance trends by time of day
- **Dark Mode**: Professional UI with Material-UI

### 🤖 ML Analytics (Gradio)
- **Anomaly Detection**: Isolation Forest model detecting network issues (5% contamination threshold)
- **Coverage Classifier**: Random Forest predicting signal quality (99.95% accuracy)
- **KPI Prediction**: LSTM forecasting throughput/latency (MAE: 2.3 Mbps)
- **Interactive Demos**: Try ML models with custom network parameters

## 🏗️ Architecture

```
├── frontend/              # React + Vite dashboard
│   ├── src/
│   │   ├── components/   # Chart components, metrics cards
│   │   └── App.jsx       # Main dashboard
│   └── public/           # Data files (JSON)
│
├── gradio-app/           # ML analytics app
│   ├── app.py           # Gradio interface
│   └── requirements.txt
│
├── ml/                   # Machine learning models
│   ├── anomaly_detector.py    # Isolation Forest
│   ├── coverage_classifier.py # Random Forest
│   ├── kpi_predictor.py       # LSTM predictor
│   └── models/               # Trained models (.pkl)
│
├── data/
│   ├── raw/              # Original datasets
│   └── processed/        # Cleaned data
│
└── scripts/              # Data processing utilities
```

## 🚀 Quick Start

### Prerequisites
- **Docker Option:** Docker Desktop
- **Manual Option:** Python 3.9+, Node.js 18+, npm or yarn

### Option A: Docker (Recommended - Easiest Setup)

**Just run one command to start everything:**

```bash
./start.sh
```

This will:
- Build and start the React dashboard at `http://localhost:5173`
- Build and start the Gradio ML app at `http://localhost:7860`
- Show backend logs in the terminal

**To stop:**
```bash
./stop.sh
```

**Note:** ML models and data must be generated first (see step 2 in Manual Setup below if starting fresh).

---

### Option B: Manual Setup

### 1. Clone Repository
```bash
git clone https://github.com/YOUR-USERNAME/telecom-network-monitor.git
cd telecom-network-monitor
```

### 2. Generate Data & Train Models
```bash
# Install Python dependencies
pip install -r requirements.txt

# Generate synthetic network data
python scripts/create_synthetic_data.py

# Train ML models
python ml/anomaly_detector.py
python ml/coverage_classifier.py
python ml/kpi_predictor.py

# Prepare data for frontend
python scripts/prepare_frontend_data.py
```

### 3. Run React Dashboard
```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:5173` to see the dashboard!

### 4. Run Gradio ML App
```bash
cd gradio-app
pip install -r requirements.txt
python app.py
```

Visit `http://localhost:7860` for interactive ML analytics!

## 📊 Machine Learning Models

### Anomaly Detection
- **Algorithm**: Isolation Forest
- **Features**: RSRP, RSRQ, SINR, CQI, throughput, latency, packet loss
- **Performance**: Detects 5% of samples as anomalies
- **Use Case**: Real-time network health monitoring

### Coverage Classifier
- **Algorithm**: Random Forest (100 trees)
- **Classes**: Excellent, Good, Fair, Poor
- **Accuracy**: 99.95%
- **F1 Score**: 0.9995
- **Top Features**: RSRQ (41%), SINR (25%), RSRP (19%)

### KPI Predictor
- **Algorithm**: LSTM (2 layers, 64/32 units)
- **Target**: Throughput & latency forecasting
- **MAE**: ~2.3 Mbps
- **Use Case**: Predictive capacity planning

## 📈 Datasets

### Ookla Open Data
- **Source**: [teamookla/ookla-open-data](https://github.com/teamookla/ookla-open-data)
- **Metrics**: Download/upload speed, latency
- **Coverage**: Global network performance tiles
- **Usage**: Geographic analysis, baseline performance

### 5G Synthetic Dataset
- **Based on**: Irish 5G Dataset schema
- **Samples**: 50,000 time-series points over 30 days
- **Metrics**: RSRP, RSRQ, SINR, CQI, throughput, latency, packet loss
- **Scenarios**: Excellent, Good, Fair, Poor, Anomaly

## 🎨 Technology Stack

### Frontend
- **Framework**: React 18 + Vite
- **UI**: Material-UI (MUI)
- **Charts**: Chart.js, react-chartjs-2
- **Styling**: Emotion CSS-in-JS

### ML/Backend
- **ML**: scikit-learn, TensorFlow/Keras
- **Data**: pandas, numpy
- **Viz**: Plotly, matplotlib
- **API**: Gradio 4.16

### Deployment
- **Dashboard**: GitHub Pages (static hosting)
- **ML App**: HuggingFace Spaces (Gradio SDK)
- **CI/CD**: GitHub Actions

## 📦 Deployment

### GitHub Pages (React Dashboard)
```bash
cd frontend
npm run build
# Deploy dist/ folder to GitHub Pages
```

### HuggingFace Spaces (Gradio App)
1. Create new Space at [huggingface.co/new-space](https://huggingface.co/new-space)
2. Select **Gradio** SDK
3. Upload:
   - `gradio-app/app.py`
   - `gradio-app/requirements.txt`
   - `ml/` folder
   - `data/raw/` sample data
4. Space will auto-deploy!

## 🎓 Skills Demonstrated

**For ML/AI Roles in Telecom:**
- ✅ Real 5G network data analysis
- ✅ Time-series forecasting (LSTM)
- ✅ Anomaly detection (unsupervised learning)
- ✅ Multi-class classification
- ✅ Feature engineering for telecom KPIs
- ✅ Model deployment (HuggingFace, web apps)
- ✅ Full-stack ML engineering
- ✅ Data visualization & dashboards
- ✅ Domain knowledge (3GPP standards)

## 📝 License

MIT License - see [LICENSE](LICENSE) file

## 👤 Author

**Bita Rahmat Zadeh**
- Portfolio: [My Portfolio ](https://bitarah.github.io/)
- LinkedIn: [My LinkedIn](https://www.linkedin.com/in/bita-rahmat-zadeh-240a3b1b0/)
- Github: [@bitarah](https://github.com/bitarah)

## 🙏 Acknowledgments

- [Ookla](https://www.ookla.com/) for open network performance data
- [IEEE DataPort](https://ieee-dataport.org/) for 5G datasets
- HuggingFace for Spaces hosting
- Gradio for ML app framework

---

⭐ **Star this repo** if you find it useful for your telecom ML projects!
