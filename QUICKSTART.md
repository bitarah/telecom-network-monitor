# 🚀 Quick Start Guide

## Get Everything Running in 5 Minutes

### 1. Generate Data & Train Models (2 minutes)

```bash
# Install Python dependencies
pip install pandas numpy scikit-learn joblib plotly gradio

# Generate synthetic network data
python scripts/create_synthetic_data.py

# Train all ML models
python ml/anomaly_detector.py
python ml/coverage_classifier.py

# Prepare data for frontend
python scripts/prepare_frontend_data.py
```

Expected output:
- ✅ 10,000 Ookla network samples
- ✅ 50,000 5G time-series data points
- ✅ 3 trained ML models (anomaly, coverage, predictor)
- ✅ JSON data files for React dashboard

### 2. Launch React Dashboard (1 minute)

```bash
cd frontend
npm install
npm run dev
```

Open browser to `http://localhost:5173`

You should see:
- 📊 Real-time metrics cards
- 📈 Interactive performance charts
- 🗺️ Geographic coverage map
- 🌓 Dark/light mode toggle

### 3. Launch Gradio ML App (1 minute)

```bash
cd gradio-app
pip install -r requirements.txt
python app.py
```

Open browser to `http://localhost:7860`

Try the ML features:
- 🚨 Anomaly Detection
- 📶 Coverage Classification
- 📈 Network Analysis

### 4. Verify Everything Works

**React Dashboard Checklist:**
- [ ] Metrics cards show data
- [ ] Charts are rendering
- [ ] Dark mode toggle works
- [ ] No console errors

**Gradio App Checklist:**
- [ ] All 3 tabs load
- [ ] Anomaly detection returns results
- [ ] Coverage classifier shows probabilities
- [ ] Network analysis displays chart

---

## Troubleshooting

**"Module not found" errors?**
```bash
pip install -r requirements.txt
```

**Charts not showing?**
- Check browser console for errors
- Verify JSON files exist in `frontend/public/`

**Gradio models not loading?**
```bash
# Retrain models
python ml/anomaly_detector.py
python ml/coverage_classifier.py
```

---

## Next Steps

1. ✅ Customize the data (edit `scripts/create_synthetic_data.py`)
2. ✅ Deploy to GitHub Pages (see `DEPLOYMENT.md`)
3. ✅ Deploy to HuggingFace Spaces
4. ✅ Add your real network data
5. ✅ Update README with live demo links

---

## File Structure Quick Reference

```
telecom-network-monitor/
├── 📁 ml/                  # ML models
│   ├── anomaly_detector.py
│   ├── coverage_classifier.py
│   └── models/            # Trained .pkl files
│
├── 📁 gradio-app/         # ML web app
│   └── app.py
│
├── 📁 frontend/           # React dashboard
│   ├── src/
│   │   ├── App.jsx
│   │   └── components/
│   └── public/
│       ├── ookla_data.json
│       └── 5g_timeseries.json
│
├── 📁 data/
│   ├── raw/               # Generated datasets
│   └── processed/
│
└── 📁 scripts/            # Utilities
    ├── create_synthetic_data.py
    └── prepare_frontend_data.py
```

Happy monitoring! 🛜
