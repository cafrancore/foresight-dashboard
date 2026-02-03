# Foresight Dashboard - Deployment Guide

## 🚀 Quick Deployment Options

### Option 1: Streamlit Cloud (Easiest - FREE)
1. Push code to GitHub
2. Go to https://streamlit.io/cloud
3. Click "New app" → Select your repository
4. Click "Deploy"
✅ Live in minutes, no configuration needed!

**Link format:** https://[github-username]-[repo-name]-[random].streamlit.app

---

### Option 2: Railway.app (Fast & Affordable)
1. Create account at railway.app
2. Connect GitHub repository
3. Add these environment variables:
   - PYTHON_VERSION=3.10
4. Deploy automatically on push
💰 Free tier available, paid starts at $5/month

---

### Option 3: Render (Reliable)
1. Create account at render.com
2. Create new "Web Service"
3. Connect GitHub repository
4. Build command: `pip install -r requirements.txt`
5. Start command: `streamlit run dashboard.py --logger.level=error --client.showErrorDetails=false`
💰 Free tier available

---

### Option 4: Docker + Any Cloud (Flexible)
1. Install Docker locally
2. Build: `docker build -t foresight-dashboard .`
3. Test locally: `docker run -p 8501:8501 foresight-dashboard`
4. Deploy to:
   - AWS ECS
   - Google Cloud Run
   - Azure Container Instances
   - DigitalOcean App Platform

---

### Option 5: Heroku (Deprecated but still works)
1. Install Heroku CLI
2. Run:
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   ```

---

## 📋 Pre-Deployment Checklist

- [ ] All dependencies in requirements.txt
- [ ] Data files accessible (relative paths)
- [ ] No hardcoded secrets (use environment variables)
- [ ] Test locally with: `streamlit run dashboard.py`
- [ ] Update README.md with instructions
- [ ] Add .gitignore to exclude large files
- [ ] Configure data caching for faster loads

---

## 🔐 Handling Secrets & API Keys

If your app uses API keys (e.g., HuggingFace tokens):

1. **Local development**: Create `.streamlit/secrets.toml`
   ```
   huggingface_token = "your-token"
   ```

2. **On Streamlit Cloud**: 
   - App Settings → Secrets → Add your secrets

3. **On Railway/Render**:
   - Add environment variables in dashboard

4. **With Docker**:
   ```bash
   docker run -e HF_TOKEN="your-token" foresight-dashboard
   ```

---

## 📊 Data Handling

- **Small files** (<50MB): Store in repo
- **Large files**: Use cloud storage (AWS S3, Google Cloud Storage)
- **Cached data**: Use @st.cache_data decorator

---

## ⚡ Performance Tips

1. Add caching:
   ```python
   @st.cache_data
   def load_model():
       return SentenceTransformer(...)
   ```

2. Reduce model size (quantize embeddings)
3. Pre-compute embeddings where possible
4. Lazy load components

---

## 🆘 Troubleshooting

**Port already in use:**
```bash
streamlit run dashboard.py --server.port 8502
```

**Model download takes too long:**
- Download model locally, commit, or pre-cache

**Memory issues:**
- Use smaller model: "all-MiniLM-L6-v2"
- Increase container RAM limit

---

## 📈 Recommended: Streamlit Cloud

**Why?** Easiest for Streamlit apps, free tier, auto-deploy from GitHub.

**Steps:**
1. Push code to GitHub
2. Visit https://streamlit.io/cloud
3. "New app" → Select repo
4. Deploy in 1 click

Total time: 5 minutes!

---

## 💡 Next Steps

1. Choose deployment platform
2. Follow the specific guide above
3. Test the live app
4. Monitor logs for errors
5. Collect feedback & iterate

Happy deploying! 🎉
