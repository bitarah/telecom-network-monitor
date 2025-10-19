# Deployment Guide

## GitHub Pages Deployment (React Dashboard)

### Option 1: GitHub Actions (Automated)

1. **Enable GitHub Pages**:
   - Go to your repository → Settings → Pages
   - Source: GitHub Actions

2. **Update `vite.config.js`**:
   - Change `base: '/telecom-network-monitor/'` to match your repo name

3. **Push to main branch**:
   ```bash
   git add .
   git commit -m "Deploy React dashboard"
   git push origin main
   ```

4. **GitHub Actions will automatically**:
   - Build the React app
   - Deploy to GitHub Pages
   - Your site will be live at: `https://YOUR-USERNAME.github.io/telecom-network-monitor/`

### Option 2: Manual Deployment

```bash
cd frontend
npm run build

# Install gh-pages package
npm install -D gh-pages

# Add to package.json scripts:
# "deploy": "gh-pages -d dist"

npm run deploy
```

---

## HuggingFace Spaces Deployment (Gradio ML App)

### Step 1: Create Space

1. Go to [huggingface.co/new-space](https://huggingface.co/new-space)
2. Name: `5g-network-ml` (or your choice)
3. License: MIT
4. SDK: **Gradio**
5. Click "Create Space"

### Step 2: Prepare Files

Create a folder with these files:
```
hf-space/
├── app.py              (from gradio-app/app.py)
├── requirements.txt    (from gradio-app/requirements.txt)
├── ml/                 (copy entire folder)
│   ├── anomaly_detector.py
│   ├── coverage_classifier.py
│   └── models/
└── data/
    └── raw/
        └── synthetic_5g_timeseries.csv
```

### Step 3: Upload to HuggingFace

**Option A: Web Interface**
1. Drag and drop files to your Space
2. Wait for build to complete

**Option B: Git**
```bash
git clone https://huggingface.co/spaces/YOUR-USERNAME/5g-network-ml
cd 5g-network-ml

# Copy files
cp -r ../gradio-app/app.py .
cp -r ../gradio-app/requirements.txt .
cp -r ../ml .
cp -r ../data/raw data/

# Commit and push
git add .
git commit -m "Deploy Gradio ML app"
git push
```

### Step 4: Configure Space

Add a `README.md` to your Space:
```markdown
---
title: 5G Network ML Analytics
emoji: 🛜
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.16.0
app_file: app.py
pinned: false
---

# 5G Network ML Analytics

Interactive ML models for telecom network monitoring.
```

### Step 5: Verify Deployment

1. Space will build automatically
2. Access at: `https://huggingface.co/spaces/YOUR-USERNAME/5g-network-ml`
3. Test all three tabs (Anomaly Detection, Coverage, Analysis)

---

## Embedding Gradio in React

Once your Gradio app is live on HuggingFace, update `frontend/src/components/GradioEmbed.jsx`:

```jsx
const gradioUrl = 'https://huggingface.co/spaces/YOUR-USERNAME/5g-network-ml';

// Option 1: Direct link
<Button href={gradioUrl} target="_blank">Launch ML App</Button>

// Option 2: Iframe embed
<iframe
  src="https://YOUR-USERNAME-5g-network-ml.hf.space"
  width="100%"
  height="600px"
  frameBorder="0"
/>
```

---

## Environment Variables

### For Production

Create `.env` file (DO NOT commit to Git):
```
# HuggingFace
HF_TOKEN=your_token_here

# GitHub Pages Base URL
VITE_BASE_URL=/telecom-network-monitor/
```

---

## Troubleshooting

### React Build Fails
- Check Node.js version (18+)
- Clear node_modules: `rm -rf node_modules && npm install`
- Check vite.config.js base path

### Gradio App Won't Start
- Verify all files uploaded to HF Space
- Check requirements.txt has all dependencies
- Review HF Space build logs

### Models Not Loading
- Ensure `ml/models/` directory exists with .pkl files
- Train models locally first: `python ml/anomaly_detector.py`
- Check file paths in app.py

---

## Next Steps

1. ✅ Deploy React dashboard to GitHub Pages
2. ✅ Deploy Gradio app to HuggingFace Spaces
3. Update README with live demo links
4. Add custom domain (optional)
5. Set up analytics (optional)
