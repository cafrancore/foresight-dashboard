# Strategic Foresight - Social Protection Reform Analysis Dashboard

A machine learning-powered dashboard for analyzing and classifying social protection reforms across key strategic dimensions.

## 🎯 Features

- **Intelligent Classification**: AI-powered categorization of reforms using sentence embeddings
- **Interactive Dashboard**: Real-time visualizations and analytics
- **Semantic Search**: Find relevant reforms by meaning, not just keywords
- **Multi-dimensional Analysis**: View reforms across Climate, Demographics, Technology, and Work trends

## 📊 Categories

1. **Climate Change** - Environmental resilience and adaptation
2. **Demographic Change** - Ageing, migration, family structures
3. **Digital Technology** - Digital transformation & inclusion
4. **Shifting Nature of Work** - Gig economy, remote work, reskilling

## 🚀 Quick Start

### Local Development

```bash
# 1. Clone repository
git clone <your-repo-url>
cd foresight_project

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run dashboard
streamlit run dashboard.py
```

Visit `http://localhost:8501`

## 🌐 Deploy to Cloud

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions on:
- ☁️ Streamlit Cloud (Recommended - Free & Easiest)
- 🚂 Railway.app
- 🎨 Render
- 🐳 Docker
- And more...

**Fastest deployment**: Streamlit Cloud (5 minutes)

## 📦 Requirements

- Python 3.10+
- Streamlit 1.28+
- Sentence Transformers
- Scikit-learn
- Plotly
- Pandas

## 📂 Project Structure

```
.
├── dashboard.py              # Main Streamlit app
├── definitions_model.py      # ML classification model
├── classify.py              # Classification logic
├── clasify_reforms.py       # Batch processing
├── requirements.txt         # Dependencies
├── Dockerfile              # Container setup
├── docker-compose.yml      # Local testing
├── Procfile               # Deployment config
└── DEPLOYMENT_GUIDE.md    # Deployment instructions
```

## 🔧 Configuration

Edit `.streamlit/config.toml` to customize:
- Color theme
- Page layout
- Server settings

## 💡 How It Works

1. **Input Processing**: Reforms are processed as text
2. **Embedding**: Converted to semantic vectors using SentenceTransformer
3. **Classification**: Compared against category definitions
4. **Visualization**: Results displayed in interactive dashboard

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -am 'Add feature'`)
4. Push to branch (`git push origin feature/improvement`)
5. Open Pull Request

## 📋 Troubleshooting

### App runs slow
- First load downloads ML models (~400MB)
- Models are cached locally after first run
- Consider deploying on platform with persistent storage

### Data not loading
- Check relative file paths
- Ensure data files are in repository root
- Use absolute paths for cloud deployment

### Memory issues
- Streamlit Cloud: Use smaller models
- Docker: Increase container memory limit

## 📞 Support

For issues, please check:
1. [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
2. [Streamlit Docs](https://docs.streamlit.io)
3. GitHub Issues

## 📄 License

Specified in LICENSE file

## 🙏 Acknowledgments

Built with:
- [Streamlit](https://streamlit.io)
- [Sentence Transformers](https://www.sbert.net)
- [Plotly](https://plotly.com)
- [Scikit-learn](https://scikit-learn.org)

---

**Ready to deploy?** Check out [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for step-by-step instructions! 🚀
